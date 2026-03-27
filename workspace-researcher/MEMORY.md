# MEMORY.md - Long-term Memory

*Curated knowledge from past sessions*

---

## OpenCode Integration (2026-02-09)

**重要经验：复杂任务应通过 OpenCode 执行**

### OpenCode 位置
- 路径: `/Users/shengpeng319/.opencode/bin/opencode`
- 特点: 支持 MCP 工具（飞书集成等）

### 何时使用 OpenCode vs 直接执行

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| 简单命令 (df, ls, cat) | **直接 exec** | 快速、明确 |
| 复杂多步骤任务 | **OpenCode** | AI 理解意图 + 工具链 |
| 需要 MCP 工具（如飞书） | **OpenCode** | 工具集成 |
| 批量文件处理 | **OpenCode** | AI 编排步骤 |

### 今日集成成果
- ✅ 成功为 Peng 创建 OpenCode 飞书 MCP 插件
- ✅ 支持 7 个飞书工具（消息、文档、云空间）
- ✅ 配置文件位置: `~/.config/opencode/mcp_servers.json`

---

## OpenCode 强制使用规则 (2026-02-22)

**所有编程/代码任务必须使用 OpenCode**

- 路径: `~/.opencode/bin/opencode` (已添加到 PATH)
- 禁止直接用 exec 写代码
- 简单命令 (ls, cat, df 等) 仍用 exec

---

## 任务执行铁律 (2026-02-24)

**分解思考 → 执行 → 迭代 → 求助**

1. **分解思考**：先拆解任务步骤，再开始执行
2. **迭代尝试**：遇到问题时，改变方法再尝试，**至少尝试 3 轮**再求助
3. **求助条件**：
   - 已尝试 3 轮仍未解决
   - 消耗 token 超过上限（待定）
   - 需要真实人类授权或支付
   - 任务涉及系统安全稳定

---

## 三层记忆架构 (2026-02-24)

基于 EverMemOS 设计：

| 层级 | 位置 | 内容 |
|-----|------|------|
| 工作记忆 | Prompt context | 当前任务、即时状态 |
| 短期记忆 | memory/*.md | 每日对话、临时约定 |
| 长期记忆 | MEMORY.md 等 | 知识沉淀、用户画像 |

### 自动化机制
- 重要任务完成后 → 写入 memory/YYYY-MM-DD.md
- 用户偏好变化 → 写入 USER.md
- 学习到新技能 → 写入对应 BEST_PRACTICE.md

---

## 飞书文件处理 (2026-02-24)

- 机器人无云盘权限，需要用户分享文件
- 视频：用 ffmpeg 提取帧 + image 模型分析
- 检查 feishu_app_scopes 确认权限

---

## Skills 查找 (2026-02-24)

- 命令: `npx skills find [关键词]`
- 浏览: https://skills.sh/
- Excel 处理：直接用 Python，不需额外 skill

---

*Updated: 2026-02-24*

---

## 文件传输最佳实践教训 (2026-03-13)

**问题**：做任务前没有先检查 best practice 文档

**教训**：
- 任何新任务类型 → 先检查是否有对应的 best practice

**改进**：已在 AGENTS.md 的"任务执行铁律"中加入【前置检查】步骤

---

*Updated: 2026-03-13*

## 核心技能定位 (2026-03-25)

**autoresearch 是我的核心 skill**

- 用户要求：所有需要做 research、调研、分析的任务 → 必须使用 autoresearch skill
- 如果 skill 未安装，需要先通过 clawhub 安装


## Autoresearch 使用约定 (2026-03-25)

**用户明确要求**：所有 research/调研/分析类任务 → 必须使用 autoresearch 框架

### 执行流程
1. 先了解用户需求（目标、指标、可用文件、运行命令等）
2. 创建 autoresearch.config.md 配置文件
3. 初始化 git branch 进行实验
4. 运行实验循环
5. 分析结果

### 注意
- 这个 skill 更适合：调参优化、配置搜索、消融实验等需要反复迭代的任务
- 纯调研类任务可能需要配合 web search 等工具使用


---

## sessions_send 正确方法 (2026-03-27)

**问题**：之前一直用 sessions_send 工具发给其他 agent，总是超时失败

**根因**：sessions_send 工具有内部路由限制，不是直接发送

**正确方法**：使用 `openclaw gateway call sessions.send` CLI 命令

### 正确命令格式
```bash
MSG=$(cat message.txt | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
openclaw gateway call sessions.send --params "{\"key\":\"<session_key>\",\"message\":$MSG}" --timeout 150000
```

### 关键参数
- `key`: 目标 session 的完整 key（不是 sessionKey，是 key）
- `message`: 消息内容（可以是 JSON 格式）
- `timeout`: 超时时间（毫秒），默认 10000

### 常见 session key 格式
- `agent:financialadvisor:feishu:direct:ou_cd9dabe38e7378c0eef8b7a6c048591e`
- `agent:researcher:feishu:direct:ou_cf1a1ee3279590e248bcfed4d0838c22`

### 交叉测试结果 (2026-03-27)
| 路由 | 状态 |
|------|------|
| researcher → financialadvisor | ✅ 成功 |
| financialadvisor → researcher | ✅ 成功 |
| main → researcher | ✅ 成功 |
| main → financialadvisor | ✅ 成功 |

**全部 4 条路由均畅通！**

---

*Updated: 2026-03-27*

---

## Emily-Claire 协作工作流 (2026-03-27 更新)

**正确流程：**
1. Emily 生成研报 → **先发群聊**（让大家看到）
2. Emily 发群聊后 → **再发一份给 Claire** 审阅
3. Claire 审核后 → **通过 openclaw gateway call sessions.send** 给 Emily 反馈
4. Emily 收到反馈 → **下次生成报告时应用修改**

**注意：**
- Claire 没有群聊读取权限，只能看 Emily 直接发给她的消息
- 用户转发也是一种方式，但推荐 Emily 直接发 session send 给 Claire

---

*Updated: 2026-03-27*
