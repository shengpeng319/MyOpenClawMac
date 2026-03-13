# 网络访问最佳实践 - OpenClaw 信息获取工具指南

## 核心原则

**优先使用专用搜索 Skills，其次浏览器自动化**

**复杂调研原则**：如果是复杂调研任务，应综合使用多个搜索工具进行交叉验证，不要只用单一工具。

当需要获取信息时，按以下优先级：
1. **SearXNG** - 本地元搜索引擎，适合快速搜索
2. **Playwright** - 浏览器自动化，访问动态网页
3. **Tavily Search** - AI 优化的专业搜索 MCP 工具
4. **last30days** - 研究过去30天内的社交媒体讨论
5. **news-summary** - 获取国际新闻 RSS 摘要
6. **web_fetch** - 静态网页，简单内容抓取 

---

## 🔧 工具详细说明

### 1. SearXNG - 本地元搜索引擎

**位置**: `~/.openclaw/workspace/skills/searxng/`

**使用方法**:
```bash
cd ~/.openclaw/workspace/skills/searxng
source .venv/bin/activate
python scripts/searxng.py search "搜索关键词" -n 10
```

**参数**:
- `-n, --num_results` - 返回结果数量（默认10）
- 不指定引擎时使用 SearXNG 默认引擎（会自动选择可用的引擎）

**可用引擎**（部分）:
- ✅ google, brave, yahoo, github, stackoverflow, youtube
- ✅ bilibili, sogou, wikipedia
- ❌ 部分需要翻墙的引擎可能超时

**适用场景**:
- 快速搜索任何主题
- 多引擎结果聚合
- 本地无需额外配置

---

### 2. Tavily Search - AI 搜索 MCP

**位置**: `~/.openclaw/workspace/skills/tavily-search/`

**MCP 配置**:
```json
{
  "mcpServers": {
    "tavily": {
      "baseUrl": "https://mcp.tavily.com/mcp/?tavilyApiKey=你的APIKey"
    }
  }
}
```

**使用方法**（通过 mcporter）:
```bash
# 查看可用工具
mcporter tools list tavily
```

**可用工具**:
- `tavily_search` - 搜索相关结果
- `tavily_extract` - 提取页面内容
- `tavily_crawl` - 爬取网站
- `tavily_map` - 映射主题
- `tavily_research` - 深度研究

**适用场景**:
- AI 优化的搜索结果
- 深度研究主题
- 内容提取和分析

---

### 3. last30days - 社交媒体研究

**位置**: `~/.openclaw/workspace/skills/last30days/`

**使用方法**:
```bash
cd ~/.openclaw/workspace/skills/last30days
python3 scripts/last30days.py "研究主题" --quick
```

**参数**:
- `--quick` - 快速模式，较少来源
- `--deep` - 深度模式，更多来源
- 默认 - 平衡模式

**工作模式**:
1. **Full Mode** (有 API Key) - Reddit + X + Web
2. **Partial Mode** - Reddit 或 X 单一平台 + Web
3. **Web-Only Mode** (无 API Key) - 仅 Web 搜索

**API Key 配置**（可选）:
```bash
mkdir -p ~/.config/last30days
cat > ~/.config/last30days/.env << 'ENVEOF'
OPENAI_API_KEY=
XAI_API_KEY=
ENVEOF
```

**适用场景**:
- 研究特定话题的社交媒体讨论
- 获取 Reddit/X 上的热门观点
- 发现最新趋势和讨论

---

### 4. news-summary - 新闻 RSS 摘要

**位置**: `~/.openclaw/workspace/skills/news-summary/`

**使用方法**:
```python
import xml.etree.ElementTree as ET
import urllib.request

# BBC World News
url = "https://feeds.bbci.co.uk/news/world/rss.xml"

# NPR News
url = "https://feeds.npr.org/1001/rss.xml"

with urllib.request.urlopen(url, timeout=10) as response:
    data = response.read()
    root = ET.fromstring(data)
    items = root.findall('.//item')
    for item in items[:10]:
        title = item.find('title')
        if title:
            print(title.text)
```

**可用 RSS 源**:
- ✅ BBC World News - `https://feeds.bbci.co.uk/news/world/rss.xml`
- ✅ NPR News - `https://feeds.npr.org/1001/rss.xml`
- ❌ Reuters - 需要备用 URL
- ❌ Al Jazeera - 可能被屏蔽

**适用场景**:
- 获取国际新闻摘要
- 了解全球热点事件
- 语音合成新闻简报

---

### 5. Playwright - 浏览器自动化

**位置**: `~/.openclaw/workspace/skills/playwright/`

**使用方法**:
```bash
# 运行 Playwright skill
cd ~/.openclaw/workspace/skills/playwright
python -m playwright [...]
```

**常用操作**:
- 导航到网页
- 截图
- 点击元素
- 填写表单
- 滚动页面

**适用场景**:
- 访问需要登录的网站
- 抓取动态渲染的内容
- 自动化网页交互

**文档**:
- `scraping.md` - 爬虫用法
- `selectors.md` - 选择器指南
- `testing.md` - 测试用法

---

## 工具对比

| 工具 | 速度 | 可靠性 | 适用场景 |
|------|------|--------|----------|
| **SearXNG** | 快 | 高 | 日常搜索、多引擎聚合 |
| **Tavily** | 中 | 高 | AI 研究、深度内容 |
| **last30days** | 中 | 中 | 社交媒体趋势研究 |
| **news-summary** | 快 | 高 | 新闻摘要获取 |
| **Playwright** | 慢 | 中 | 动态网页、登录需求 |
| **web_fetch** | 快 | 低 | 静态简单页面 |

---

## 常见场景用法

### 场景1: 搜索最新新闻
```bash
# 使用 SearXNG
cd ~/.openclaw/workspace/skills/searxng
source .venv/bin/activate
python scripts/searxng.py search "美股今天走势" -n 5
```

### 场景2: 研究特定话题（过去30天）
```bash
# 使用 last30days
cd ~/.openclaw/workspace/skills/last30days
python3 scripts/last30days.py "AI 投资趋势" --quick
```

### 场景3: 获取国际新闻
```python
# 使用 news-summary
import xml.etree.ElementTree as ET
import urllib.request

url = "https://feeds.bbci.co.uk/news/world/rss.xml"
with urllib.request.urlopen(url) as response:
    root = ET.fromstring(response.read())
    for item in root.findall('.//item')[:5]:
        print(item.find('title').text)
```

### 场景4: 深度内容提取
```bash
# 使用 Tavily MCP
# 通过 mcporter 调用 tavily_extract 工具
```

### 场景5: 访问需要登录的网站
```bash
# 使用 Playwright
cd ~/.openclaw/workspace/skills/playwright
python -m playwright navigate "https://zhihu.com"
```

---

## 失败时的排查

1. **SearXNG 超时** - 尝试指定可用引擎（google, brave, bilibili）
2. **Tavily 失败** - 检查 MCP 配置和网络
3. **last30days 无数据** - 添加 API Key 增强功能，或使用 web-only 模式
4. **news-summary 失败** - 尝试备用 RSS 源
5. **Playwright 失败** - 检查浏览器安装和依赖

---

## 记忆要点

> **重要**: 优先使用专用搜索 Skills（SearXNG、Tavily、last30days、news-summary），它们比传统浏览器工具更稳定、更高效。Playwright 仅用于需要浏览器交互的场景。

**关键词**: searxng, tavily, last30days, news-summary, playwright, 搜索工具, 信息获取

---

# 研究与信息搜集方法论

## 核心原则

**多源验证 vs 单源依赖**

- ❌ **不要只从一个来源搜集信息**
- ✅ **先研究口碑好的信息源**
- ✅ **选出多个可靠源进行交叉验证**
- ✅ **综合总结，形成全面视角**

---

## 推荐信息源

### 搜索引擎
| 来源 | 特点 | 适用场景 |
|------|------|----------|
| **SearXNG** | 本地多引擎聚合 | 日常快速搜索 |
| **Tavily** | AI 优化搜索 | 深度研究分析 |

### 社交媒体研究
| 来源 | 特点 | 适用场景 |
|------|------|----------|
| **last30days** | Reddit/X/网页聚合 | 热门话题讨论 |

### 新闻资讯
| 来源 | 特点 | 适用场景 |
|------|------|----------|
| **news-summary** | BBC/NPR RSS | 国际新闻摘要 |
| **SearXNG** | 多引擎新闻搜索 | 特定主题新闻 |

---

## 信息搜集标准流程

### Step 1: 定义需求
- 明确要搜集什么类型的信息
- 确定需要几个维度的观点

### Step 2: 选择工具/信息源
- 快速搜索 → SearXNG
- 深度研究 → Tavily + last30days
- 新闻获取 → news-summary + SearXNG
- 动态网页 → Playwright

### Step 3: 多源搜集
- 从每个工具/源获取关键信息
- 记录不同视角的观点

### Step 4: 综合总结
- 提炼热点话题
- 分类整理
- 提供洞察

---

## 通用模板：信息搜集检查清单

```markdown
## 信息搜集计划

### 1. 需求定义
- [ ] 明确搜集目标
- [ ] 确定需要的信息类型

### 2. 工具/信息源选择
- [ ] 主要搜索: [SearXNG / Tavily / last30days]
- [ ] 新闻获取: [news-summary / SearXNG]
- [ ] 备用工具: [Playwright]

### 3. 执行搜集
- [ ] 工具1: [工具名] - [关键发现]
- [ ] 工具2: [工具名] - [关键发现]
- [ ] 工具3: [工具名] - [关键发现]

### 4. 综合分析
- [ ] 提取热点话题
- [ ] 分类整理
- [ ] 提供洞察

### 5. 总结输出
- [ ] 按热度排序
- [ ] 按类别分组
- [ ] 附上来源标签
```

---

## 核心学习

> **当工具失败时，记录最佳实践**
> **当方法不对时，改进研究流程**

**持续进化 = 每次都比上次更好**
