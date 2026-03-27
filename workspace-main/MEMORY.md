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

## Token 过长主动管理 (2026-03-19)

**规则：发现 token 过长时主动提醒并优化**

### 触发条件
- 对话轮次过多（通常 > 30 轮）
- 单次回复过长
- 上下文包含大量历史记录

### 处理流程
1. **提醒主人**：告知 token 即将/已经过长
2. **分析原因**：检查是什么导致增长（长任务？多次迭代？历史堆积？）
3. **提出方案**：
   - 新开会话承接后续任务
   - 清理/压缩历史记录
   - 拆分任务到子会话

### 预防措施
- 复杂任务 → 拆分子任务，使用子 agent
- 长对话 → 适时建议开启新会话
- 定期提醒会话长度


## 金融投资辅助最佳实践 (2026-03-21)

**文档位置：**
- `INVESTMENT_WITH_OPENCLAW_BEST_PRACTICE.md` - 投资辅助最佳实践
- `STOCK_ALERT_TECHNICAL.md` - 股票告警技术实现

**核心结论：**
- OpenClaw = 投资秘书（持续监控、消息触达）
- Claude Code = 量化工程师（构建工具、复杂分析）
- 两者配合使用效果最佳

**OpenClaw 投资功能：**
- 每日定时研报（cron 任务）
- 股价跌破阈值告警（飞书推送）
- 事件驱动分析（地缘政治、财报等）

*Updated: 2026-03-21*

---

## Memory Search 配置要点 (2026-03-25)

**QMD vs Memory Search 区别**
- QMD 只是 Memory Search 的一个可选后端（本地方案）
- 远程 API（OpenAI/Gemini）方案更简单，不需要安装 QMD
- 如配置 Memory Search，优先考虑远程 API

---

## Emily-Claire 多 Agent 协作模式 (2026-03-25)

**Agent 分工**
- **Emily**：financial advisor agent，生成投资研报
- **Claire**：researcher agent，review 并提供反馈

**协作流程**：Emily 发报告 → Claire review → 追踪改进

---

## Emily 量化交易项目 Review 要点 (2026-03-25)

**Claire 发现的核心问题**
- 风控漏洞（跨策略仓位叠加、隔夜跳空、单点故障）
- 策略太简单（需 ADX/成交量确认/ETF 代理）
- 遗漏模块（订单队列、崩溃恢复、性能监控）
- 技术选型错误（Python 3.14 太新、alpaca-trade-api 已废弃）

**详细 checklist**（目录结构、新增模块、依赖、路线图、测试、安全）已存到 `workspace-financialadvisor/MEMORY.md`

*Updated: 2026-03-25*

---

## IMA Skill 使用要点 (2026-03-26)

**IMA Skill 位置**
- 路径: `~/.openclaw/workspace/skills/ima/`
- 注意: 系统 skill 列表不包含它，但 import_doc API 可用

**IMA 笔记上传 Doc IDs**
- Agent 开发课程第一课 (什么是 Agent): 7442848899167446
- Agent 开发课程第二课 (核心架构): 7442850757243064
- Agent 局限性第十一课: 7442930323190905

---

## 网络搜索 Fallback 技巧 (2026-03-26)

**问题**: SearXNG 返回非标准 JSON
**解决方案**: 换用 DuckDuckGo HTML

---

## Subagent 设计原则 (2026-03-26)

**关键**: 设计 subagent 任务方案时要确保方案完整可执行
- coder subagent 产出了完整可执行的重构方案
- 方案包含具体步骤和执行路径

---

## GitHub 备份配置 (2026-03-26)

**备份目标**: shengpeng319/MyOpenClawMac
**备份内容**: AGENT_DEVELOPMENT_GUIDE.md + 各 workspace 配置
**命令**: git push

---

## 多 Agent Workspace 重构效果 (2026-03-26)

**成果**: 6 个 agent workspace 重构
**操作**:
- 删除冗长的 MEMORY_ARCHITECTURE.md → 替换为简洁的 MEMORY_GUIDE.md
- 删除 NETWORK_ACCESS_BEST_PRACTICE.md → 替换为简洁的 NETWORK_GUIDE.md
- 精简 AGENTS.md（340行 → ~120行）
- 保留专业文件

**效果**: 预估节省启动 token 约 50%

*Updated: 2026-03-26*
