---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# Team

Our team develops industrial AI, foundation models, embodied intelligence, digital twins, and intelligent manufacturing systems.

{% assign team_groups = "researcher,phd,master" | split: "," %}
{% assign team_titles = "Research Staff,Ph.D. Students,Master Students" | split: "," %}

{% for group in team_groups %}
{% assign members = site.members | where: "group", group | sort: "order" %}
{% if members.size > 0 %}
<section class="team-portrait-group">
  <h2>{{ team_titles[forloop.index0] }}</h2>
  <div class="team-portraits">
    {% for member in members %}
      {% include portrait.html lookup=member.slug %}
    {% endfor %}
  </div>
</section>
{% endif %}
{% endfor %}
