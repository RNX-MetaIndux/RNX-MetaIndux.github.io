---
title: Research
nav:
  order: 1
  tooltip: Published works
---

# {% include icon.html icon="fa-solid fa-microscope" %}Research

Our research focuses on industrial foundation models, embodied intelligence, digital twins, industrial time-series learning, and intelligent manufacturing systems.

<div class="publication-sources">
  <a href="https://scholar.google.com/citations?hl=en&user=BcSIgFEAAAAJ">
    {% include icon.html icon="fa-brands fa-google-scholar" %} Google Scholar
  </a>
  <a href="https://dblp.org/pid/01/1313-1.html">
    {% include icon.html icon="fa-solid fa-database" %} DBLP
  </a>
  <a href="https://orcid.org/0000-0001-6346-6930">
    {% include icon.html icon="fa-brands fa-orcid" %} ORCID
  </a>
</div>

{% assign publications_by_year = site.data.publications | group_by: "year" %}

{% for year in publications_by_year %}
## {{ year.name }}

<div class="publication-list">
  {% for publication in year.items %}
  <article class="publication-item">
    <div class="publication-meta">
      <span>{{ publication.type }}</span>
      <span>{{ publication.year }}</span>
    </div>
    <h3>
      <a href="{{ publication.link }}">{{ publication.title }}</a>
    </h3>
    <p class="publication-authors">{{ publication.authors }}</p>
    <p class="publication-venue">{{ publication.venue }}</p>
    <a class="publication-record" href="{{ publication.link }}">
      DBLP {% include icon.html icon="fa-solid fa-arrow-up-right-from-square" %}
    </a>
  </article>
  {% endfor %}
</div>
{% endfor %}

<p class="publication-note">Publication metadata verified against DBLP on 8 July 2026.</p>
