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

---

## IMA API 集成 (2026-03-26)

**凭证已配置**
- client_id: `d3f4e56d8d9494225d0c84d75f679989`
- API Key: 已保存到 `~/.config/ima/api_key`
- Base URL: `https://ima.qq.com/openapi/note/v1/`

**认证方式（重要）**
- 需要用 header 格式: `ima-openapi-clientid` + `ima-openapi-apikey`
- JSON body 格式不工作
- endpoint `search_note_book` 需要参数: `{"search_type": 0, "query_info": {...}, "start": 0, "end": 20}`

**经验教训**
- 调试 IMA API 时，先用 -v 看详细响应
- "skill auth failed" = header 格式正确但凭证无效
- "clientID or apiKey is empty" = JSON body 格式（错误）

---

## 记忆系统架构 (2026-03-26)

**三层记忆架构**
| 层级 | 位置 | 状态 |
|-----|------|------|
| Session logs | ~/.openclaw/agents/<agent>/sessions/*.jsonl | ✅ 正常 |
| Daily memory | memory/YYYY-MM-DD.md | ✅ 今日已创建 |
| Long-term | MEMORY.md | ⚠️ 需更新 |

**注意**: 需要定期将每日重要内容提炼到 MEMORY.md


---

---

## PM 主动追进度机制

### 核心原则
- PM 是主动追进度的角色，不等对方来报
- 5 分钟心跳驱动，直接发消息询问 Task Agent 进度
- Task Agent 只管回复，不需要任何额外操作

### 机制规则

| 条件 | 动作 |
|------|------|
| 心跳触发（每 5 分钟） | 读取活跃 Task Agent 列表，向每个 Agent 发消息询问进度 |
| 发消息后 5 分钟内回复 | 正常，继续监控 |
| 5 分钟无回复 | 再发一条消息催促 |
| 10 分钟仍无回复 | 通知 Peng 介入 |

### Task Agent 列表
文件位置：`~/.openclaw/workspace/active_tasks_sessions.json`

格式：
```json
{
  "agents": [
    {
      "name": "Emily",
      "role": "financialadvisor",
      "sessionKey": "agent:financialadvisor:feishu:direct:ou_cd9dabe38e7378c0eef8b7a6c048591e",
      "currentTask": "Lesson 3 MACD v1.2 修复"
    },
    {
      "name": "Diana",
      "role": "educationexpert",
      "sessionKey": "agent:educationexpert:feishu:direct:ou_fddf58b3579afe9168ad38eea080294f",
      "currentTask": "Lesson 3 MACD QA 审核"
    },
    {
      "name": "Claire",
      "role": "researcher",
      "sessionKey": "agent:researcher:feishu:direct:ou_cf1a1ee3279590e248bcfed4d0838c22",
      "currentTask": "MACD 课程内容研究"
    }
  ]
}
```

**每次 Peng 派发新任务时，将对应的 session key 和任务描述追加到此文件。**

### 心跳执行步骤

1. 读取 `~/.openclaw/workspace/active_tasks_sessions.json`
2. 遍历 `agents` 数组，对每个 sessionKey 执行：
   ```
   sessions_send(sessionKey, "任务 [{currentTask}] 进度如何？请汇报当前状态")
   ```
3. 记录每个 Agent 的最后回复时间
4. 下次心跳时：超过 5 分钟无回复 → 再催；超过 10 分钟无回复 → 通知 Peng

### 通知 Peng 的格式
```
⚠️ 任务卡住升级
Agent: {name}
任务: {currentTask}
无响应时长: {X} 分钟
请介入处理。
```

### 配置位置
- 心跳配置：`~/.openclaw/openclaw.json` → `agents.projectmanager.heartbeat`
- Agent 列表：`~/.openclaw/workspace/active_tasks_sessions.json`

---

*Updated: 2026-03-28*
