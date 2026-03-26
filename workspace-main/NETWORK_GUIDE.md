# 网络访问指南

_按需读取。启动不加载。_

## 工具优先级

```
CDP > Playwright > scrapling > SearXNG > curl
```

## 平台访问

| 平台 | 推荐方式 | 说明 |
|------|---------|------|
| Twitter/X | CDP | 无需 cookie，绕过 GraphQL |
| 小红书 | CDP | 无需登录 |
| 微信公众号 | CDP | 需要登录态 |
| 微博 | CDP 或 SearXNG | 视情况 |
| 通用搜索 | SearXNG（中文）、tavily（英文） | 聚合引擎 |

## 可用工具

| 工具 | 用途 |
|------|------|
| CDP | 复杂平台、登录态页面 |
| Playwright | 独立浏览器、截图、批量操作 |
| SearXNG | 中文聚合搜索（localhost:12613） |
| tavily | 英文搜索 |
| yt-dlp | YouTube/Bilibili 视频 |
| Jina AI | 网页转 Markdown（`r.jina.ai/url`） |

## 中文 RSS

| 来源 | 地址 |
|------|------|
| 虎嗅 | https://www.huxiu.com/rss/0.xml |
| 36氪 | https://36kr.com/feed |

## 站点知识积累

成功访问新网站后，将经验写入：
```
~/.openclaw/skills/web-access/references/site-patterns/[站点名].md
```

---

_Last Updated: 2026-03-26_
