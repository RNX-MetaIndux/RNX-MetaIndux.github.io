require 'liquid'

module Jekyll
  module PublicationFilters
    # Match whole author names, never a substring such as "Lei Ren" in "Xiaolei Ren".
    def publications_by_member(publications, name, aliases = [])
      names = ([name] + Array(aliases)).map { |value| normalize_author(value) }
      Array(publications).select do |publication|
        authors = publication['authors']
        authors = authors.split(/,|;|\band\b/) if authors.is_a?(String)
        Array(authors).any? { |author| names.include?(normalize_author(author)) }
      end.sort_by { |publication| [publication['year'].to_i, publication['date'].to_s] }.reverse
    end

    private

    def normalize_author(value)
      value.to_s.sub(/\s+\d{4}\z/, '').strip.downcase.gsub(/\s+/, ' ')
    end
  end
end

Liquid::Template.register_filter(Jekyll::PublicationFilters)
