---
title: Team
seo_title: 团队成员与个人主页
description: 北京航空航天大学 RNX-MetaIndux 团队成员，包括任磊、王海腾、祝云飞等研究人员与研究生的中英文姓名、学术主页和论文。
nav:
  order: 3
  tooltip: About our team
---

<div class="content-page team-page">
  <div class="page-heading">
    <h1>团队成员 <span lang="en">Team</span></h1>
    <p>团队围绕工业人工智能、工业大模型、工业智能体、具身智能开展研究。</p>
    <p class="page-intro-en" lang="en">Our team studies industrial AI, industrial foundation models, industrial agents, and embodied intelligence.</p>
  </div>

{% assign team_groups = "researcher,phd,master" | split: "," %}
{% assign team_titles = "Research Staff,Ph.D. Students,Master Students" | split: "," %}

{% for group in team_groups %}
{% assign members = site.members | where: "group", group | sort: "order" %}
{% if members.size > 0 %}
<div class="team-portrait-group">
  <h2>{{ team_titles[forloop.index0] }}</h2>
  <div class="team-portraits">
    {% for member in members %}
      {% include portrait.html lookup=member.slug %}
    {% endfor %}
  </div>
</div>
{% endif %}
{% endfor %}
</div>
