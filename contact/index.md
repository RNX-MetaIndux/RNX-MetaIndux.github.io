---
title: Contact
nav:
  order: 5
  tooltip: Email, address, and admissions
---

<div class="contact-page">
  <header class="contact-heading">
    <h1>Contact</h1>
    <p>欢迎就科研合作、学术交流与人才培养联系我们。</p>
  </header>

  <div class="contact-grid">
    <section>
      <h2>Email</h2>
      <p><a href="mailto:{{ site.links.email }}">{{ site.links.email }}</a></p>
    </section>

    <section>
      <h2>Address</h2>
      <p>{{ site.data.contact.address }}</p>
    </section>
  </div>

  <section class="contact-laboratories">
    <h2>实验室平台</h2>
    <ul>
      {% for laboratory in site.data.contact.laboratories %}
      <li>{{ laboratory }}</li>
      {% endfor %}
    </ul>
  </section>

  <section class="contact-admissions">
    <span>JOIN US</span>
    <h2>实验室招生</h2>
    <p class="contact-admissions-lead">每年招收硕士生、直博生</p>
    <p>{{ site.data.contact.admissions.summary }}</p>
    <p>招生咨询：<a href="mailto:{{ site.links.email }}">{{ site.links.email }}</a></p>
  </section>
</div>
