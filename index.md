---
title: Home
seo_title: 北航任磊教授团队 · 工业大模型与工业智能体
description: 北航（北京航空航天大学）任磊教授 RNX-MetaIndux 团队主页，介绍工业大模型、工业智能体、工业人工智能与智能制造研究，以及团队成员、论文与招生信息。
---

<div class="home-shell">
  <div class="home-introduction">
    <h1>北航任磊教授团队 <span lang="en">RNX-MetaIndux</span></h1>
    <p>北京航空航天大学 · 工业大模型、工业智能体与智能制造</p>
  </div>
  <figure class="home-hero">
    <img src="{{ "/images/home-hero-cncc.jpg" | relative_url }}" alt="CNCC 2025 工业大模型产业应用研讨会现场 / CNCC 2025 Industrial Foundation Model Industry Application Symposium">
    <figcaption>Industrial Foundation Model | MetaIndux</figcaption>
  </figure>

  <div class="home-layout">
    <div class="home-main">
      <article class="home-article">
      <h2>
        <a href="https://adg.csdn.net/69523ae75b9f5f31781b3e46.html">
          北航李伯虎院士任磊教授团队 | 工业大模型IFMsys架构，打造智能制造新范式
        </a>
        <a class="home-title-en" lang="en" href="https://adg.csdn.net/69523ae75b9f5f31781b3e46.html">Academician Bohu Li and Professor Lei Ren's Team: IFMsys Architecture for a New Paradigm of Intelligent Manufacturing</a>
      </h2>

      <p>
        工业大模型并非通用大语言模型在工业场景中的简单迁移。面向高可信输出、多模态协同、多场景泛化和复杂流程关联等关键挑战，任磊教授团队提出工业大模型系统架构 IFMsys，并构建原型系统 MetaIndux。
      </p>

      <p>
        IFMsys 由模型训练、模型适配和模型应用三个层次组成：通过多模态工业数据与机理知识训练基础模型，针对任务和行业进行适配，并以工业智能体协作方式支持产品研发、生产制造、试验测试、经营管理和运维服务。
      </p>

      <p>
        MetaIndux 展示了智能问答、研发设计、过程决策、终端控制、工业内容生成和科学发现等能力，为工业大模型服务智能制造提供了系统化路径。
      </p>

      <figure class="home-news-figure">
        <img
          src="{{ "/images/industrial-foundation-model-process.png" | relative_url }}"
          alt="工业大模型从数据制备、基座模型训练、任务与行业模型适配到工业场景交互应用的构建流程"
        >
      </figure>

      <p>
        <a href="https://adg.csdn.net/69523ae75b9f5f31781b3e46.html">
          阅读原文 {% include icon.html icon="fa-solid fa-arrow-up-right-from-square" %}
        </a>
      </p>
      </article>

      <div class="home-news-list">
        {% for news in site.data.news %}
          {% unless news.featured %}
          <article class="home-article home-article--news">
            <h2>
              <a href="{{ news.link }}">
                {{ news.title }}
                <span class="home-title-en" lang="en">{{ news.title_en }}</span>
              </a>
            </h2>
            {% for paragraph in news.paragraphs %}
            <p>{{ paragraph }}</p>
            {% endfor %}
            <figure class="home-news-figure">
              <img src="{{ news.image | relative_url }}" alt="{{ news.image_alt }}" loading="lazy">
            </figure>
            <p>
              <a href="{{ news.link }}">
                阅读原文 {% include icon.html icon="fa-solid fa-arrow-up-right-from-square" %}
              </a>
            </p>
          </article>
          {% endunless %}
        {% endfor %}
      </div>
    </div>

    <aside class="home-sidebar" aria-label="Homepage sidebar">
      <section class="home-panel">
        <h2>团队成员 <span class="home-heading-en" lang="en">Team</span></h2>
        <p>北京航空航天大学任磊教授 RNX-MetaIndux 团队，围绕工业人工智能、工业大模型与智能制造开展研究。</p>
        <ul>
          {% assign research_staff = site.members | where: "group", "researcher" | sort: "order" %}
          {% for member in research_staff %}
          <li><a href="{{ member.url | relative_url }}">{{ member.name }}</a> · {{ member.description }}</li>
          {% endfor %}
        </ul>
        <a href="{{ '/team/' | relative_url }}">查看全部成员与个人主页</a>
      </section>

      <section class="home-panel">
        <h2>联系我们 <span class="home-heading-en" lang="en">Contact</span></h2>
        <p>
          <strong>Address</strong><br>
          {{ site.data.contact.address }}
        </p>
        <p>
          <strong>Group Email</strong><br>
          <a href="mailto:{{ site.links.email }}">{{ site.links.email }}</a>
        </p>
      </section>

      <section class="home-panel home-laboratories">
        <h2>实验室平台 <span class="home-heading-en" lang="en">Laboratory Affiliations</span></h2>
        <ul>
          {% for laboratory in site.data.contact.laboratories %}
          <li>{{ laboratory }}</li>
          {% endfor %}
        </ul>
      </section>

      <section class="home-panel home-admissions">
        <span class="home-admissions-label">JOIN US</span>
        <h2>实验室招生 <span class="home-heading-en" lang="en">Admissions</span></h2>
        <p>
          <strong>每年招收硕士生、博士生、直博生</strong>
        </p>
        <p>
          招生单位：北航自动化学院、北航软件学院、中关村实验室
        </p>
        <a href="{{ "/contact/" | relative_url }}">查看招生与联系方式</a>
      </section>

      <section class="home-panel">
        <h2>Search</h2>
        <form class="home-search" onsubmit="onSiteSearchSubmit(event)">
          <input type="text" name="query" placeholder="SEARCH ...">
          <button type="submit" aria-label="search site">
            {% include icon.html icon="fa-solid fa-magnifying-glass" %}
          </button>
        </form>
      </section>

      <section class="home-panel home-publications">
        <h2>最新论文 <span class="home-heading-en" lang="en">Latest Publications</span></h2>
        {% for publication in site.data.home_publications %}
        <article>
          <span>{{ publication.year }} · {{ publication.type }}</span>
          <h3>{% include publication-link.html publication=publication %}</h3>
          <p>{{ publication.venue }}</p>
        </article>
        {% endfor %}
        <a class="home-publications-all" href="{{ "/research/" | relative_url }}">View all publications</a>
      </section>
    </aside>
  </div>
</div>
