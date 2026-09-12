# 搜索收录维护

正式站点：https://rnx-metaindux.github.io/

成员页会直接输出中英文姓名、身份、单位与相关论文，不依赖 JavaScript。
`_members/*.md` 中维护姓名、aliases（论文英文作者名）、职务、单位和已核实的外链；
有详细简介时直接写在 front matter 下方。不要为同名作者添加未经核实的论文或链接。

`_includes/meta.html` 为每页输出独立 canonical、描述和 JSON-LD；成员采用
ProfilePage / Person。`jekyll-sitemap` 自动生成 sitemap，robots.txt 提供其地址。

## 站长平台提交

代码部署不会自动完成站长账号验证，也不能保证收录时间或姓名搜索排名。
网站所有者可在 Google Search Console、Bing Webmaster Tools、百度搜索资源平台中
添加本站，完成各平台要求的所有权验证，再提交站点地图：

https://rnx-metaindux.github.io/sitemap.xml

若平台提供 HTML meta 验证码，在 `_config.yaml` 中加入平台实际给出的 token：

```yaml
webmaster_verifications:
  google: "平台提供的真实 token"
  bing: "平台提供的真实 token"
  baidu: "平台提供的真实 token"
```

不要把整个 meta 标签或账号密码填入配置。当前没有配置任何验证 token。
若平台要求上传验证文件，应按平台原样提供文件，不能自行生成验证码。

完成验证后优先检查并请求抓取首页、团队页，以及以下成员页：

- https://rnx-metaindux.github.io/members/lei-ren.html
- https://rnx-metaindux.github.io/members/haiteng-wang.html
- https://rnx-metaindux.github.io/members/yunfei-zhu.html

使用平台的 URL 检查报告确认实际索引状态；公开搜索没有结果不能单独证明未收录。
有权编辑的学校个人主页或学术主页也可以增加本站成员页链接，帮助发现并区分同名作者。
首页 Search 是 Google 站内查询，结果依赖 Google 的收录。

## 本地与发布检查

```sh
JEKYLL_ENV=production bundle exec jekyll build
bundle exec ruby scripts/check-site.rb
```

发布工作流会在上传前检查全部成员页的可见姓名、图片、独立网址、JSON-LD 和站点地图。
部署后还应检查正式网址返回 200，且关键成员页已显示新正文。

官方说明：[请求重新抓取](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)、
[ProfilePage](https://developers.google.com/search/docs/appearance/structured-data/profile-page)、
[规范网址](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)。
