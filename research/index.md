---
title: Research
description: Publications by the RNX-MetaIndux team, maintained in the committed citation dataset.
nav:
  order: 1
  tooltip: Publications and research topics
---

<div class="research-page">
  <div class="research-heading page-heading">
    <h1>研究成果 <span lang="en">Research & Publications</span></h1>
    <p>研究方向涵盖工业大模型与工业智能体、工业互联网与工业软件、工业时序智能、具身智能。</p>
    <p class="page-intro-en" lang="en">Our research spans industrial foundation models and agents, industrial Internet and software, industrial time-series intelligence, and embodied intelligence.</p>

    <div class="publication-sources" aria-label="学术主页">
      <a href="https://scholar.google.com/citations?hl=en&user={{ site.links.google-scholar }}">
        {% include icon.html icon="fa-brands fa-google-scholar" %} Google Scholar
      </a>
      <a href="https://dblp.org/pid/01/1313-1.html">
        {% include icon.html icon="fa-solid fa-database" %} DBLP
      </a>
      <a href="https://orcid.org/{{ site.links.orcid }}">
        {% include icon.html icon="fa-brands fa-orcid" %} ORCID
      </a>
    </div>
  </div>

  <section class="publication-tools" aria-label="论文筛选">
    {% include search-box.html %}
    <div class="publication-filter-tags">
      {% assign filters = "Journal,Conference,Preprint,Foundation Models,Industrial Agents,Industrial Time Series,Industrial Internet & Edge,Industrial Software & Control,Knowledge & Decision Intelligence,Smart Manufacturing" | split: "," %}
      {% for filter in filters %}
      <a href="{{ page.dir | relative_url }}?search=&quot;tag: {{ filter }}&quot;" class="tag">{{ filter }}</a>
      {% endfor %}
    </div>
    {% include search-info.html %}
  </section>

  {% assign featured_publications = site.data.featured_publications %}
  {% if featured_publications and featured_publications.size > 0 %}
  <section class="featured-publications" aria-label="Featured publications">
    <div class="featured-publications-heading">
      <h2>置顶论文 <span lang="en">Featured Publications</span></h2>
    </div>

    <div class="featured-publication-list">
      {% for publication in featured_publications %}
      <article class="publication-item featured-publication">
        <div class="publication-meta">
          <span>{{ publication.type }}</span>
          <span>{{ publication.year }}</span>
        </div>

        <h3><a href="{{ publication.link }}">{{ publication.title }}</a></h3>
        {% if publication.title_en %}
        <p class="publication-title-en">{{ publication.title_en }}</p>
        {% endif %}

        {% if publication.authors.first %}
          <p class="publication-authors">{{ publication.authors | join: ", " }}</p>
        {% else %}
          <p class="publication-authors">{{ publication.authors }}</p>
        {% endif %}

        <p class="publication-venue">{{ publication.venue | default: publication.publisher }}</p>

        {% if publication.tags %}
        <div class="publication-tags tags">
          {% for tag in publication.tags %}
          <a href="{{ page.dir | relative_url }}?search=&quot;tag: {{ tag }}&quot;" class="tag">{{ tag }}</a>
          {% endfor %}
        </div>
        {% endif %}

        <div class="publication-records">
          {% if publication.doi %}
          <a href="https://doi.org/{{ publication.doi }}">DOI</a>
          {% endif %}
          <a href="{{ publication.link }}">Record</a>
        </div>
      </article>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  {% assign publications = site.data.citations %}
  {% if publications == empty %}
    {% assign publications = site.data.publications %}
  {% endif %}
  {% assign publications_by_year = publications | group_by: "year" %}

  <div class="publication-results" data-pagination="research-publications" data-page-size="10">
    {% for year in publications_by_year %}
    <section class="publication-year" data-pagination-group>
      <h2>{{ year.name }} <span>{{ year.items.size }} publications</span></h2>

      <div class="publication-list">
        {% for publication in year.items %}
        <article class="publication-item" data-pagination-item data-search="{{ publication.title | xml_escape }} {{ publication.publisher | xml_escape }} {{ publication.venue | xml_escape }}">
          <div class="publication-meta">
            <span>{{ publication.type }}</span>
            <span>{{ publication.year }}</span>
            {% if publication.citation_count %}
              <span>{{ publication.citation_count }} citations</span>
            {% endif %}
          </div>

          <h3><a href="{{ publication.link }}">{{ publication.title }}</a></h3>

          {% if publication.authors.first %}
            <p class="publication-authors">{{ publication.authors | join: ", " }}</p>
          {% else %}
            <p class="publication-authors">{{ publication.authors }}</p>
          {% endif %}

          <p class="publication-venue">{{ publication.publisher | default: publication.venue }}</p>

          {% if publication.tags %}
          <div class="publication-tags tags">
            {% for tag in publication.tags %}
            <a href="{{ page.dir | relative_url }}?search=&quot;tag: {{ tag }}&quot;" class="tag">{{ tag }}</a>
            {% endfor %}
          </div>
          {% endif %}

          <div class="publication-records">
            {% if publication.doi %}
            <a href="https://doi.org/{{ publication.doi }}">DOI</a>
            {% endif %}
            {% if publication.dblp %}
            <a href="{{ publication.dblp }}">DBLP</a>
            {% endif %}
            {% if publication.scholar_link %}
            <a href="{{ publication.scholar_link }}">Scholar</a>
            {% endif %}
            {% unless publication.doi or publication.dblp or publication.scholar_link %}
            <a href="{{ publication.link }}">Record</a>
            {% endunless %}
          </div>
        </article>
        {% endfor %}
      </div>
    </section>
    {% endfor %}
  </div>

  <div class="pagination" data-pagination-controls="research-publications" aria-label="Research pagination"></div>

  <p class="publication-note">Publication metadata is maintained in the committed citation dataset. Topic labels are assigned from publication metadata and can be refined manually.</p>
</div>
