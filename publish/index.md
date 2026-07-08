---
title: Publish
description: Books and teaching publications by Professor Lei Ren and the RNX-MetaIndux team.
nav:
  order: 4
  tooltip: Books and publications
---

<div class="content-page publish-page">
  <div class="page-heading">
    <h1>出版物 <span lang="en">Books & Publications</span></h1>
    <p>展示任磊教授及团队围绕工业人工智能、工业互联网与智能制造出版的专著和教材。</p>
    <p class="page-intro-en" lang="en">Books and textbooks by Professor Lei Ren and the team on industrial artificial intelligence, the industrial Internet, and intelligent manufacturing.</p>
  </div>

  <div class="publication-books">
    {% for book in site.data.books %}
    <article class="publication-book">
      <a class="book-cover-link" href="{{ book.link }}" aria-label="View {{ book.title | xml_escape }}">
        {% if book.image %}
        <img src="{{ book.image | relative_url }}" alt="Cover of {{ book.title | xml_escape }}" loading="lazy">
        {% else %}
        <span class="book-cover-typeset" aria-hidden="true">
          <span>SPRINGER</span>
          <strong>{{ book.title }}</strong>
          <small>{{ book.subtitle }}</small>
          <em>{{ book.authors }}</em>
        </span>
        {% endif %}
      </a>

      <div class="book-content">
        <div class="book-meta">
          <span>{{ book.year }}</span>
          <span>{{ book.type }}</span>
          <span>{{ book.language }}</span>
        </div>
        <h2><a href="{{ book.link }}">{{ book.title }}</a></h2>
        {% if book.subtitle %}<p class="book-subtitle">{{ book.subtitle }}</p>{% endif %}
        <p class="book-authors">{{ book.authors }}</p>
        <p class="book-description">{{ book.description }}</p>
        <dl class="book-details">
          <div><dt>出版社</dt><dd>{{ book.publisher }}</dd></div>
          <div><dt>ISBN</dt><dd>{{ book.isbn }}</dd></div>
        </dl>
        <a class="book-source" href="{{ book.link }}">
          出版社页面 {% include icon.html icon="fa-solid fa-arrow-up-right-from-square" %}
        </a>
      </div>
    </article>
    {% endfor %}
  </div>
</div>
