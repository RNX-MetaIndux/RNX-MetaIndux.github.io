# 搜索收录维护

正式站点：https://rnx-metaindux.github.io/

成员页会直接输出中英文姓名、身份、单位与相关论文，不依赖 JavaScript。
`_members/*.md` 中维护姓名、aliases（论文英文作者名）、职务、单位和已核实的外链；
有详细简介时直接写在 front matter 下方。不要为同名作者添加未经核实的论文或链接。

`_includes/meta.html` 为每页输出独立 canonical、描述和 JSON-LD；成员采用
ProfilePage / Person。`jekyll-sitemap` 自动生成 sitemap，robots.txt 提供其地址。

## 必应：IndexNow 主动通知

本站已接入必应支持的 IndexNow。根目录的验证文本文件证明本站控制权，
它不等同于 Bing Webmaster Tools 的账号凭据，不需要先登录站长账号才能提交 URL。

GitHub Pages 成功部署后，`on-pages` 工作流会对比这次和上次实际发布的页面：
首次启用时提交站点地图内的全部 URL，之后仅通知新增、内容变化或已删除的 URL。
脚本会忽略每次构建自动变化的资源缓存版本，避免无内容更新时重复提交。
提交前会核对线上验证文件。失败的部署不会触发提交。

接口为 `https://www.bing.com/indexnow`，无需再向 `cn.bing.com` 重复发送。
HTTP 200 表示收到通知；202 表示收到通知、验证尚未完成。
两者均不表示已抓取、已收录或姓名查询排名已提高；400、403、422、429 等不计为成功。
429 应根据服务返回的 Retry-After 等待，不要密集重发。

查看 GitHub Actions 中 `on pages deploy` → `indexnow` 的运行结果与摘要。
若本地需要核对待提交 URL 或在排除故障后手动提交一次：

```sh
bundle exec ruby scripts/submit-indexnow.rb --all --dry-run
bundle exec ruby scripts/submit-indexnow.rb --all
```

实际提交回执存入 `tmp/indexnow-submission.json`，不包含 key，也不会发布到网站。
`--all` 用于首次启用或人工排错，不应设置为每日无变化重复提交。

要查看必应对某个 URL 的具体收录原因和查询表现，仍需在
[Bing Webmaster Tools](https://www.bing.com/webmasters/)登录并验证站点。
IndexNow 验证文件不会自动授予站长后台账号访问权限。

官方依据：[必应接入说明](https://www.bing.com/indexnow/getstarted)、
[IndexNow 协议与回执含义](https://www.indexnow.org/documentation)。

## 站长平台提交

上述主动通知不会自动完成站长后台的账号验证，也不能保证收录时间或姓名搜索排名。
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

## 姓名与论文标题搜索

北航成员页的标题包含“北航 + 中文姓名”，正文同时保留学校全称与英文姓名。
首页以“北航任磊教授团队”为主标题。

6 篇重点论文有独立的介绍页面，包含完整题名、作者、中文研究介绍、原文来源与 DOI，
从首页、研究列表和相应成员页进入。结构化数据与 citation 标签方便识别书目信息，
不代表 Google Scholar 已收录；Scholar 对摘要/全文有额外要求。

| 查询或论文 | 优先提交 URL |
| --- | --- |
| 北航任磊 | https://rnx-metaindux.github.io/members/lei-ren.html |
| 北航王海腾 | https://rnx-metaindux.github.io/members/haiteng-wang.html |
| Industrial Foundation Model | https://rnx-metaindux.github.io/research/industrial-foundation-model/ |
| Foundation Models for the Process Industry | https://rnx-metaindux.github.io/research/foundation-models-process-industry/ |
| AI Control Scientist | https://rnx-metaindux.github.io/research/ai-control-scientist/ |
| PhysDGM | https://rnx-metaindux.github.io/research/physdgm/ |
| VLT | https://rnx-metaindux.github.io/research/vlt/ |
| TS-MLLM | https://rnx-metaindux.github.io/research/ts-mllm/ |

在 [Google Search Console](https://search.google.com/search-console) 中添加网址前缀资源
`https://rnx-metaindux.github.io/`，验证后提交 sitemap，并通过 URL 检查查看索引状态。
在[百度搜索资源平台](https://ziyuan.baidu.com/)验证站点后，检查抓取诊断及普通收录入口。
若抓取失败，先看诊断中的连接与响应信息；不能仅凭 `github.io` 域名断定平台屏蔽。

对于排名与身份区分，另一个实际步骤是由有权限的作者/学校管理员，在任磊等人的
北航教师主页增加“RNX-MetaIndux 团队主页”链接，成员自己的学术资料也可链接本站个人页。
这些是指向本站的真实外部链接；本站链接回学校不能替代这个步骤。
本仓库不会自动修改学校网站或未经授权的其他账号。

建议在平台中保留提交日期、索引状态、查询词、展示次数、点击次数和平均位置，
观察真实变化。提交抓取与页面优化均不能承诺首页排名或固定生效时间。

新增论文介绍时维护 `_data/publication_details.yaml`：使用已在 `citations.yaml` 中核实的 DOI，
固定 slug，填写有来源的 summary、key_points、sources。仅提供确切的发表日期；
`editorial_note` 供维护者记录证据，不在网页展示。

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
