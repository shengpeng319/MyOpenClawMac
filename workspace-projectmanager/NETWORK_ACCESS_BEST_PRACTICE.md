# 网络访问最佳实践 - OpenClaw 访问受限网站指南

## 核心原则

**优先使用 Chrome DevTools（MCP），其次 Browser Relay Extension**

当需要访问动态渲染或有访问限制的网站时：
1. **首选 Chrome DevTools** - 通过 MCP 连接本地 Chrome，功能更强
2. **备选 Browser Relay Extension** - 如果 Chrome DevTools 不可用

---

## 访问方法优先级

| 优先级 | 方法 | 适用场景 |
|--------|------|----------|
| 1️⃣ | **Chrome DevTools (MCP)** | 动态渲染网站、需要登录的网站、有反爬虫的网站 |
| 2️⃣ | **Browser Relay Extension** | Chrome DevTools 不可用时的备选方案 |
| 3️⃣ | `web_fetch` | 静态网页，简单内容抓取 |
| 4️⃣ | `curl` + 请求头伪装 | API 端点，无反爬虫的简单页面 |
| ❌ | `agent-browser` | **WSL 环境下无法使用**（需要 X server） |

---

## 🔧 经验学习

### 2026-03-02: Chrome DevTools 优先
- **规则**: 所有 agent 和 subagent 抓新闻必须优先使用 Chrome DevTools
- **原因**: Chrome DevTools (MCP) 功能更强，支持 CDP 协议
- **备选**: 如果 Chrome DevTools 不可用，再使用 Browser Relay

### 工具失败时立即记录原则
- **原则**：「当一种工具失败但另一种成功时 → 立即记录到 best practice」
- **原因**：避免重复同样的错误
- **行动**：解决问题后，更新对应的 best practice 文件

### Cron 任务自动启用
- **问题**：`openclaw cron add` 默认创建 disabled 状态
- **解决**：使用 `~/bin/cron-add-auto` 脚本
- **示例**：`~/bin/cron-add-auto "每日热点新闻" "1770604800000" "# message"`

---

## Chrome DevTools 使用步骤

### 1. 确保 Chrome DevTools MCP 已配置
- 检查 `~/.config/opencode/mcp_servers.json` 是否包含 chrome-devtools
- 或使用 `mcporter` 工具管理 MCP 服务器

### 2. 使用 Chrome DevTools Skill
```bash
# 先读取 skill 文件
~/.agents/skills/chrome-devtools/SKILL.md
```

### 3. 常用操作
- 导航到目标页面
- 获取页面内容
- 截图
- 执行 JavaScript
- 网络请求分析

---

## Browser Relay Extension 使用步骤（备选）

### 1. 确保 Extension 已开启
- 用户需要在 Chrome 浏览器上打开 Browser Relay extension
- Extension 图标显示 "ON" 或已连接状态

### 2. 使用 `browser` 工具
```bash
# 导航到目标页面
browser action=navigate profile=chrome targetUrl="https://www.zhihu.com/billboard"

# 获取页面快照（交互元素）
browser action=snapshot profile=chrome compact=true

# 截图
browser action=screenshot profile=chrome

# 滚动页面
browser action=act kind=scroll targetId=xxx
```

### 3. 关键参数
- `profile="chrome"` - **必须指定**，告诉 OpenClaw 使用用户的 Chrome 浏览器
- 不要使用 `host="sandbox"` 或其他选项

---

## 常见网站访问策略

### ✅ Chrome DevTools / Browser Relay 适用
- **知乎** (zhihu.com) - 需要登录，有反爬虫
- **B站** (bilibili.com) - 动态渲染，API 限制
- **微博** - 动态内容，需要登录
- **虎嗅** - 深度商业科技
- **36氪** - 科技创投
- **需要登录的任何网站**

### ⚠️ 可尝试 curl/api
- 纯静态页面
- 有公开 API 的网站
- 没有严格反爬虫的网站

### ❌ 不适用
- `agent-browser` - WSL 环境无法启动（需要 X server）
- `web_fetch` - 只能获取静态 HTML，动态内容无效

---

## 失败时的排查

1. **优先使用 Chrome DevTools** - 检查 MCP 配置
2. **备选 Browser Relay** - 检查 Extension 是否开启
3. **使用正确的 profile** - 必须用 `profile="chrome"`
4. **尝试不同的方法** - API → web_fetch → Chrome DevTools → Browser Relay
5. **检查网络连接** - 某些网站可能区域性限制

---

## 记忆要点

> **重要**: Chrome DevTools (MCP) 是访问动态/受限网站的首选方法。Browser Relay 是备选方案。在 WSL 环境下，`agent-browser` 无法使用，必须通过 OpenClaw 的 `browser` 工具连接用户的 Chrome 浏览器。

**关键词**: chrome devtools, mcp, browser relay, profile=chrome, 动态渲染, 登录限制, 反爬虫

---

## 📌 飞书文件获取最佳实践

### 问题
用户通过飞书发送视频/文件，机器人无法直接下载。

### 原因
飞书机器人没有云盘根目录访问权限，需要用户手动分享文件。

### 解决方案
1. **询问用户文件来源**：云盘分享 / 直接拖入
2. **用户操作**：将文件分享给机器人（分享到对话或云盘共享）
3. **获取文件 token**：从消息中提取 file_key
4. **使用 feishu_drive**：下载文件

### 文件类型处理

| 文件类型 | 处理方式 |
|---------|---------|
| 视频 (mp4) | ffmpeg 提取帧 → image 模型分析 |
| 图片 | 直接用 image 模型分析 |
| 文档 | 用 feishu_doc 读取 |
| Excel | 下载后用 Python 处理 |

### 注意事项
- 飞书机器人权限有限，优先让用户分享文件
- 视频分析需要先提取关键帧
- 检查 `feishu_app_scopes` 确认权限

---

# 研究与信息搜集方法论

## 核心原则

**多源验证 vs 单源依赖**

- ❌ **不要只从一个 APP/网站搜集信息**
- ✅ **先研究口碑好的信息源**
- ✅ **选出多个可靠源进行交叉验证**
- ✅ **综合总结，形成全面视角**

---

## 好的中文新闻源分类

### 科技商业类
| 新闻源 | 特点 | 适用场景 |
|--------|------|----------|
| **虎嗅** | 深度评论，商业洞察 | 深度分析，社会现象解读 |
| **36氪** | 科技创投，前沿资讯 | AI科技、创业融资、IPO |
| **知乎热榜** | 社会热点，民间讨论 | 热门话题、民生讨论 |

### 综合类
| 新闻源 | 特点 | 适用场景 |
|--------|------|----------|
| 微博热搜 | 实时热点，娱乐八卦 | 突发事件、舆情监测 |
| 豆瓣讨论 | 文化深度，小众兴趣 | 影视、书籍，文化话题 |

---

## 信息搜集标准流程

### Step 1: 定义需求
- 明确要搜集什么类型的信息
- 确定需要几个维度的观点

### Step 2: 选择信息源
- 根据需求选择合适的新闻源
- 优先选择口碑好、专业度高的平台

### Step 3: 多源搜集
- 从每个源获取关键信息
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

### 2. 信息源选择
- [ ] 列出潜在信息源
- [ ] 评估可靠性
- [ ] 选择 2-3 个优质源

### 3. 执行搜集
- [ ] 源1: [平台名] - [关键发现]
- [ ] 源2: [平台名] - [关键发现]
- [ ] 源3: [平台名] - [关键发现]

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
