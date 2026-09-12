require 'date'
require 'json'
require 'nokogiri'
require 'uri'
require 'yaml'

root = Dir.pwd
destination = File.expand_path(ARGV.fetch(0, '_site'), root)
config = YAML.load_file(File.join(root, '_config.yaml'))
origin = config.fetch('url') + config.fetch('baseurl', '')
failures = []
check = ->(condition, message) { failures << message unless condition }
read_page = ->(path) { Nokogiri::HTML(File.read(File.join(destination, path), encoding: 'UTF-8')) }
sitemap = Nokogiri::XML(File.read(File.join(destination, 'sitemap.xml')))
locations = sitemap.xpath('//*[local-name()="loc"]').map(&:text)
team = read_page.call('team/index.html')
titles = []

Dir.glob(File.join(root, '_members', '*.md')).each do |source|
  member = YAML.safe_load(File.read(source, encoding: 'UTF-8').split(/^---\s*$\n?/)[1])
  slug = File.basename(source, '.md')
  route = "/members/#{slug}.html"
  document = read_page.call(route.delete_prefix('/'))
  name = member.fetch('name')
  main = document.at_css('main')&.text.to_s
  title = document.at_css('title')&.text.to_s
  description = document.at_css('meta[name="description"]')&.[]('content').to_s
  canonical = document.css('link[rel="canonical"]')
  expected_url = origin + route

  check.call(document.at_css('html')&.[]('lang') == 'zh-CN', "#{slug}: wrong language")
  check.call(document.css('main h1').size == 1 && document.at_css('main h1').text.include?(name), "#{slug}: missing name heading")
  check.call(main.include?(member.fetch('description')) && main.include?(member.fetch('affiliation')), "#{slug}: missing visible identity")
  Array(member['aliases']).each { |alias_name| check.call(main.include?(alias_name), "#{slug}: missing English name") }
  check.call(title.include?(name) && description.include?(name) && description.include?(config.fetch('title')), "#{slug}: incomplete metadata")
  check.call(canonical.size == 1 && canonical.first['href'] == expected_url, "#{slug}: incorrect canonical")
  check.call(document.at_css('meta[property="og:url"]')&.[]('content') == expected_url, "#{slug}: incorrect social URL")
  check.call(!document.at_css('meta[name="robots"]')&.[]('content').to_s.include?('noindex'), "#{slug}: indexing blocked")
  check.call(locations.include?(expected_url), "#{slug}: absent from sitemap")
  check.call(team.css('a[href]').any? { |link| link['href'] == config.fetch('baseurl', '') + route }, "#{slug}: missing team link")

  structured = document.css('script[type="application/ld+json"]').map { |script| JSON.parse(script.text) }
  profile = structured.find { |item| item['@type'] == 'ProfilePage' }
  check.call(profile && profile.dig('mainEntity', '@type') == 'Person' && profile.dig('mainEntity', 'name') == name && profile['url'] == expected_url, "#{slug}: incorrect person schema")
  document.css('main img[src]').each do |img|
    image_path = URI::DEFAULT_PARSER.unescape(img['src']).delete_prefix(config.fetch('baseurl', '')).delete_prefix('/')
    check.call(File.file?(File.join(destination, image_path)), "#{slug}: missing portrait #{image_path}")
  end
  titles << title
end

check.call(titles.uniq.size == titles.size, 'Member page titles are not unique')
locations.each do |location|
  check.call(location.start_with?(origin + '/'), "Non-production sitemap URL: #{location}")
end
%w[index.html team/index.html research/index.html].each do |path|
  document = read_page.call(path)
  expected = origin + '/' + path.delete_suffix('index.html')
  check.call(document.at_css('link[rel="canonical"]')&.[]('href') == expected, "#{path}: incorrect canonical")
  document.css('script[type="application/ld+json"]').each { |script| JSON.parse(script.text) }
end
check.call(File.read(File.join(destination, 'robots.txt')).include?("Sitemap: #{origin}/sitemap.xml"), 'Missing robots sitemap URL')
check.call(!locations.include?(origin + '/404.html'), '404 must not appear in sitemap')
check.call(!File.exist?(File.join(destination, 'tmp')), 'Temporary research files must not be published')

abort(failures.join("\n")) unless failures.empty?
puts "Verified #{titles.size} member pages: visible names, portraits, canonical URLs, JSON-LD, team links and sitemap."
