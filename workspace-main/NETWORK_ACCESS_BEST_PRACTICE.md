# 网络访问最佳实践

## 平台访问优先级

### Twitter/X 和 小红书 - CDP 优先

**规则**: Twitter/X 和 小红书（Xiaohongshu）优先使用 CDP 浏览器方式访问。

**原因**:
- xreach 需要 Twitter cookies（需要手动配置）
- xiaohongshu MCP 需要 cookies（需要登录）
- CDP 使用用户已有的浏览器 session，无需额外认证

**CDP 访问方式**:
```bash
# 启动 CDP（如果未运行）
bash ~/.openclaw/skills/web-access/scripts/check-deps.sh
# 或
node ~/.openclaw/skills/web-access/scripts/cdp-proxy.js &

# 通过 web-access skill 访问
# 使用 CDP 模式读取页面，绕过反爬限制
```

**适用场景**:
| 平台 | 推荐方式 | 原因 |
|------|---------|------|
| Twitter/X | CDP | 无需 cookie，绕过 GraphQL 限制 |
| 小红书 | CDP | 无需 cookie，绕过登录墙 |
| 微信公众号 | CDP | 需要登录态 |
| 微博 | CDP 或 SearXNG | 视情况选择 |

---

## 浏览器自动化工具栈

### 优先级：CDP > Playwright > scrapling

| 工具 | 用途 | 状态 | 说明 |
|------|------|------|------|
| **CDP** | 复杂平台、登录态页面 | ✅ 运行中 | 使用用户 Chrome，已有 session |
| **Playwright** | 独立浏览器自动化 | ✅ 已安装 | Chromium 已缓存，独立环境 |
| **scrapling** | 轻量快速抓取 | ⚠️ 需 patchright | 简单页面可用 |

**Playwright 使用方式**:
```bash
# 打开页面
playwright open https://example.com

# 截图
playwright screenshot https://example.com output.png

# Python 脚本示例
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    print(page.title())
    browser.close()
"
```

**何时用 Playwright vs CDP**:
- CDP: 已有登录态、复杂平台（小红书/Twitter/微信）
- Playwright: 需要独立环境、批量操作、需要截图/PDF

---

## 可用工具

| 工具 | 用途 | 状态 |
|------|------|------|
| SearXNG | 中文搜索、聚合 | ✅ localhost:12613 |
| tavily MCP | 英文搜索 | ✅ 已配置（6 tools） |
| yt-dlp | YouTube/Bilibili 视频 | ✅ 已安装 |
| Jina AI | 网页转 Markdown | `r.jina.ai/url` |
| curl | 简单 HTTP 请求 | ✅ 系统自带 |

### SearXNG 中文引擎

已启用: 百度、搜狗、Bilibili

```bash
# 搜索示例
curl -X POST "http://localhost:12613/search" \
  --data-urlencode "q=人工智能" \
  --data-urlencode "engines=baidu,google" \
  --data-urlencode "format=json"
```

---

## 中文 RSS 源

| 来源 | 地址 | 状态 |
|------|------|------|
| 虎嗅 | https://www.huxiu.com/rss/0.xml | ✅ |
| 36氪 | https://36kr.com/feed | ✅ |
| 澎湃新闻 | https://www.thepaper.cn/list_25431.rss | ⚠️ |

---

## MCP 插件状态

| 插件 | 用途 | 状态 |
|------|------|------|
| tavily | 英文搜索 API | ✅ 启用 |
| exa | Web 搜索 | ❌ 已移除（损坏） |
| xiaohongshu | 小红书 API | ❌ 需要 cookies |

---

*最后更新: 2026-03-26*
