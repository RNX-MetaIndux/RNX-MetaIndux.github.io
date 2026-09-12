require 'digest'
require 'fileutils'
require 'json'
require 'net/http'
require 'nokogiri'
require 'open3'
require 'optparse'
require 'time'
require 'uri'
require 'yaml'

module IndexNow
  ENDPOINT = URI('https://www.bing.com/indexnow')

  def self.urls_from_sitemap(xml, origin)
    Nokogiri::XML(xml).xpath('//*[local-name()="loc"]').map(&:text).uniq.each do |url|
      uri = URI(url)
      unless url.start_with?(origin + '/') && uri.scheme == 'https' && uri.host == URI(origin).host && !uri.query && !uri.fragment
        raise "Refusing a sitemap URL outside the production site: #{url}"
      end
    end
  end

  def self.page_path(url, origin)
    path = URI::DEFAULT_PARSER.unescape(url.delete_prefix(origin + '/'))
    raise 'Unsafe page path' if path.include?('\\') || path.split('/').any? { |part| part == '.' || part == '..' } || path.start_with?('/')
    path += 'index.html' if path.empty? || path.end_with?('/')
    path
  end

  def self.content_hash(html)
    # The template changes these asset cache versions on every build.
    Digest::SHA256.hexdigest(html.gsub(/([?&]v=)\d+/, '\1BUILD'))
  end

  def self.changed_urls(current_urls, previous_urls, current_html, previous_html)
    (current_urls | previous_urls).select do |url|
      !current_urls.include?(url) || !previous_urls.include?(url) ||
        content_hash(current_html.call(url)) != content_hash(previous_html.call(url))
    end
  end

  def self.git_file(directory, revision, path)
    stdout, _, status = Open3.capture3('git', '-C', directory, 'show', "#{revision}:#{path}")
    status.success? ? stdout : nil
  end

  def self.request(uri, request)
    Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 20, read_timeout: 30, write_timeout: 30) do |http|
      http.request(request)
    end
  end

  def self.receipt(code, urls)
    status = case code
             when 200 then 'received'
             when 202 then 'received_key_validation_pending'
             else raise "IndexNow rejected the submission (HTTP #{code}); no success was recorded."
             end
    { endpoint: ENDPOINT.to_s, http_status: code, status: status,
      submitted_at: Time.now.utc.iso8601, url_count: urls.size, urls: urls,
      note: 'Receipt is not confirmation of crawling, indexing or search ranking.' }
  end

  def self.workflow_outputs(result)
    return unless ENV['GITHUB_OUTPUT']
    File.open(ENV['GITHUB_OUTPUT'], 'a') do |output|
      %i[http_status status url_count].each { |key| output.puts "#{key}=#{result.fetch(key)}" }
    end
  end

  def self.run(arguments)
    options = { site: '_site', dry_run: false, all: false, previous: 'HEAD^', report: 'tmp/indexnow-submission.json' }
    OptionParser.new do |parser|
      parser.on('--site DIRECTORY') { |value| options[:site] = value }
      parser.on('--previous REF') { |value| options[:previous] = value }
      parser.on('--all', 'Submit all current sitemap URLs once for initial setup') { options[:all] = true }
      parser.on('--dry-run', 'Prepare URLs without contacting Bing') { options[:dry_run] = true }
      parser.on('--report FILE') { |value| options[:report] = value }
    end.parse!(arguments)

    config = YAML.load_file('_config.yaml')
    origin = config.fetch('url').delete_suffix('/') + config.fetch('baseurl', '')
    key_file = config.fetch('indexnow').fetch('key_file')
    raise 'Invalid IndexNow key filename' unless key_file.match?(/\A[a-zA-Z0-9-]{8,128}\.txt\z/)
    key = File.read(key_file, encoding: 'UTF-8').strip
    raise 'IndexNow key does not match its filename' unless key == key_file.delete_suffix('.txt')
    directory = File.expand_path(options[:site])
    sitemap = File.read(File.join(directory, 'sitemap.xml'), encoding: 'UTF-8')
    urls = urls_from_sitemap(sitemap, origin)
    old_key = git_file(directory, options[:previous], key_file) unless options[:all]
    if !options[:all] && old_key&.strip == key
      old_sitemap = git_file(directory, options[:previous], 'sitemap.xml')
      raise 'Previous sitemap unavailable; use --all for an intentional full submission' unless old_sitemap
      old_urls = urls_from_sitemap(old_sitemap, origin)
      urls = changed_urls(urls, old_urls,
                          ->(url) { File.read(File.join(directory, page_path(url, origin)), encoding: 'UTF-8') },
                          ->(url) { git_file(directory, options[:previous], page_path(url, origin)) || '' })
    end
    raise 'Too many URLs for a single IndexNow request' if urls.size > 10_000
    if urls.empty? || options[:dry_run]
      result = { http_status: 'not_sent', status: urls.empty? ? 'no_content_changes' : 'dry_run', url_count: urls.size, urls: urls }
      workflow_outputs(result)
      puts JSON.generate(result)
      return
    end

    key_location = URI(origin + '/' + key_file)
    proof = request(key_location, Net::HTTP::Get.new(key_location))
    unless proof.code.to_i == 200 && proof.body.strip == key
      raise 'The deployed IndexNow key is not available yet; no URLs were submitted.'
    end
    payload = { host: URI(origin).host, key: key, keyLocation: key_location.to_s, urlList: urls }
    post = Net::HTTP::Post.new(ENDPOINT)
    post['Content-Type'] = 'application/json; charset=utf-8'
    post.body = JSON.generate(payload)
    response = request(ENDPOINT, post)
    if response.code.to_i == 429
      raise "IndexNow rate limit reached; retry after #{response['Retry-After'] || 'the service cooldown'}. Do not repeatedly resubmit."
    end
    result = receipt(response.code.to_i, urls)
    workflow_outputs(result)
    FileUtils.mkdir_p(File.dirname(options[:report]))
    File.write(options[:report], JSON.pretty_generate(result) + "\n")
    puts "IndexNow HTTP #{result[:http_status]}: #{result[:url_count]} URLs #{result[:status]}. This does not confirm indexing or ranking."
    if ENV['GITHUB_STEP_SUMMARY']
      File.open(ENV['GITHUB_STEP_SUMMARY'], 'a') do |summary|
        summary.puts "IndexNow HTTP #{result[:http_status]}: #{result[:url_count]} URLs #{result[:status]}."
        summary.puts "\nReceipt is not confirmation of crawling, indexing or search ranking."
        summary.puts "\nSubmitted URLs:\n" + urls.map { |url| "- #{url}" }.join("\n")
      end
    end
  end
end

IndexNow.run(ARGV) if $PROGRAM_NAME == __FILE__
