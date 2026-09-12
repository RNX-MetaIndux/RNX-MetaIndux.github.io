require 'jekyll'

module Jekyll
  # Only create pages with curated, sourced research descriptions.
  class PublicationPages < Generator
    safe true
    priority :normal

    def generate(site)
      details = site.data['publication_details'] || []
      citations = site.data['citations'] || []
      seen_slugs = []
      seen_dois = []

      details.each do |detail|
        slug = detail.fetch('slug')
        doi = detail.fetch('doi').downcase
        unless slug.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/) && !seen_slugs.include?(slug) && !seen_dois.include?(doi)
          raise Errors::FatalException, "Duplicate or invalid publication page: #{slug}"
        end
        if detail['summary'].to_s.empty? || Array(detail['key_points']).empty? || Array(detail['sources']).empty?
          raise Errors::FatalException, "Publication page needs a sourced research description: #{slug}"
        end
        seen_slugs << slug
        seen_dois << doi
        citation = citations.find { |record| record['doi'].to_s.downcase == doi }
        raise Errors::FatalException, "No citation found for #{doi}" unless citation

        publication = citation.dup
        featured = Array(site.data['featured_publications']).find { |record| record['doi'].to_s.downcase == doi }
        publication['venue'] = featured['venue'] if featured && featured['venue']
        route = "/research/#{slug}/"
        authors = Array(publication['authors']).map do |name|
          member = site.collections.fetch('members').docs.find do |candidate|
            ([candidate.data['name']] + Array(candidate.data['aliases'])).any? do |alias_name|
              normalize_author(alias_name) == normalize_author(name)
            end
          end
          { 'name' => name, 'member_name' => member&.data&.fetch('name'), 'member_url' => member&.url }
        end

        page = PageWithoutAFile.new(site, site.source, "research/#{slug}", 'index.html')
        page.data.merge!(
          'layout' => 'publication',
          'lang' => 'zh-CN',
          'title' => publication.fetch('title'),
          'description' => detail.fetch('summary'),
          # There is no source HTML file for jekyll-last-modified-at to inspect.
          'last_modified_at' => nil,
          'scholarly_article' => true,
          'publication' => publication,
          'publication_authors' => authors,
          'detail' => detail
        )
        site.pages << page

        %w[citations publications featured_publications home_publications].each do |source|
          Array(site.data[source]).each do |record|
            matches = if record['doi']
                        record['doi'].downcase == doi
                      else
                        record['title'] == publication['title']
                      end
            record['detail_url'] = route if matches
          end
        end
      end
    end

    private

    def normalize_author(value)
      value.to_s.sub(/\s+\d{4}\z/, '').strip.downcase.gsub(/\s+/, ' ')
    end
  end
end
