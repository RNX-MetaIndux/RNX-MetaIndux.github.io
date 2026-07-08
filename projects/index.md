---
title: Projects
description: National and ministerial research projects led or undertaken by the RNX-MetaIndux team.
nav:
  order: 2
  tooltip: Research projects and funding
---

<div class="projects-page">
  <div class="projects-heading page-heading">
    <h1>科研项目与基金 <span lang="en">Projects & Funding</span></h1>
    <p>团队长期承担国家级和省部级重大重点项目，围绕工业互联网、工业软件、工业大模型、工业智能体与智能制造开展基础研究、关键技术攻关和产业应用。</p>
    <p class="page-intro-en" lang="en">The team undertakes major national and ministerial projects spanning fundamental research, key technologies, and industrial applications in the industrial Internet, industrial software, foundation models, agents, and intelligent manufacturing.</p>
  </div>

  <section class="project-metrics" aria-label="项目概览">
    <div><strong>30+</strong><span>国家级和省部级项目与课题</span></div>
    <div><strong>1</strong><span>亿级重大项目</span></div>
    <div><strong>3</strong><span>千万级重大项目</span></div>
    <div><strong>17</strong><span>官网公开项目与课题条目</span></div>
  </section>

  <section class="projects-section">
    <h2>重点项目 <span lang="en">Featured Projects</span></h2>
    <div class="featured-projects">
      {% for project in site.data.projects %}
        {% if project.priority == "S" %}
        <article class="featured-project">
          <div class="project-meta">
            <span>{{ project.year }}</span>
            <span>{{ project.category }}</span>
          </div>
          <h3><a href="{{ project.source }}">{{ project.title }}</a></h3>
          <p>{{ project.summary }}</p>
          <p class="project-role"><strong>公开情况</strong>{{ project.role }}</p>
          <a class="project-source" href="{{ project.source }}">
            公开来源 {% include icon.html icon="fa-solid fa-arrow-up-right-from-square" %}
          </a>
        </article>
        {% endif %}
      {% endfor %}
    </div>
  </section>

  {% assign section_keys = "national,nsfc,miit,education" | split: "," %}
  {% assign section_titles = "国家重大任务与重点研发计划,国家自然科学基金项目,工信部专项,人才培养项目" | split: "," %}
  {% assign section_titles_en = "National Research Programs,NSFC Projects,MIIT Programs,Education & Talent Programs" | split: "," %}

  <section class="projects-section projects-portfolio" data-pagination="project-portfolio" data-page-size="8">
    <h2>项目列表 <span lang="en">Project Portfolio</span></h2>

    {% for section_key in section_keys %}
    {% assign section_projects = site.data.projects | where: "section", section_key %}
    <div class="project-group" data-pagination-group>
      <h3>{{ section_titles[forloop.index0] }} <span lang="en">{{ section_titles_en[forloop.index0] }}</span></h3>

      {% for project in section_projects %}
        {% unless project.priority == "S" %}
        <article class="project-row" data-pagination-item>
          <div class="project-year">{{ project.year }}</div>
          <div class="project-row-content">
            <div class="project-meta">
              <span>{{ project.category }}</span>
              <span>{{ project.subtype }}</span>
            </div>
            <h4><a href="{{ project.source }}">{{ project.title }}</a></h4>
            <p>{{ project.summary }}</p>
            <p class="project-role"><strong>承担情况</strong>{{ project.role }}</p>
            <a class="project-source" href="{{ project.source }}">
              公开来源 {% include icon.html icon="fa-solid fa-arrow-up-right-from-square" %}
            </a>
          </div>
        </article>
        {% endunless %}
      {% endfor %}
    </div>
    {% endfor %}

    <div class="pagination" data-pagination-controls="project-portfolio" aria-label="Projects pagination"></div>
  </section>

</div>
