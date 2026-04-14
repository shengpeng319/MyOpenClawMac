# HermesAgent vs OpenClaw 研究报告

**研究日期：** 2026-04-14
**报告目的：** 审查 HermesAgent 核心机制 → 提出蒸馏方案 → 决定是否集成到 OpenClaw

---

## 一、HermesAgent 核心机制详解

### 1.1 定位与背景

HermesAgent 是 **Nous Research** 出品的开源 Agent 框架（MIT License），核心理念是"让 Agent 与你共同成长"——强调**学习循环**、**跨平台消息网关**、**200+ 模型路由**。

### 1.2 核心架构

```
HermesAgent 架构
├── Agent Loop (Agent Runtime)
│   ├── Tool Calls + Tool Results
│   ├── Session Memory (frozen snapshot at session start)
│   └── Progressive Disclosure (L0/L1/L2)
├── Skills System (~/.hermes/skills/)
│   ├── Bundled Skills (内置)
│   ├── Agent-Managed Skills (自动创建/更新/删除)
│   └── Skills Hub (clawhub / skills.sh / well-known / github / lobehub)
├── Memory System (持久记忆)
│   ├── MEMORY.md (~2,200 chars, Agent 个人笔记)
│   ├── USER.md (~1,375 chars, 用户画像)
│   └── Session Search (SQLite FTS5, 全量历史)
└── Skills Hub Ecosystem (7+ 市场支持)
```

---

## 二、关键创新机制（Hermes 强于 OpenClaw 的地方）

### 🔬 机制 1：渐进式披露 (Progressive Disclosure)

**核心：** Agent 不全量加载 skill，按需渐进加载。

```
L0: skills_list()      → [{name, description, category}] (~3k tokens 全量)
L1: skill_view(name)   → 完整 SKILL.md (按需)
L2: skill_view(name, path) → references/ 子目录 (按需)
```

**OpenClaw 现状：** 全量注入所有 SKILL.md → token 浪费

---

### 🧠 机制 2：Agent 自主管理 Skills (skill_manage tool)

**触发时机：**
- 完成复杂任务（5+ tool calls）后
- 遇到错误并找到解决路径时
- 用户纠正了 Agent 行为时

**操作：** create / patch / edit / delete / write_file / remove_file

**OpenClaw 现状：** skill-creator 依赖手动触发，不能自动创建

---

### 💾 机制 3：双层持久记忆 + 容量限制

| 文件 | 容量 | 用途 |
|------|------|------|
| MEMORY.md | 2,200 chars | Agent 个人笔记（环境事实、项目约定、工具怪癖） |
| USER.md | 1,375 chars | 用户画像（偏好、沟通风格、技术水平） |

**Frozen Snapshot：** 会话启动时注入一次，**会话中修改不更新当前 session prompt**，持久化到磁盘供下次使用。

**OpenClaw 现状：** 无容量硬限制，无 Frozen Snapshot，session history 功能弱

---

### 🛡️ 机制 4：Skills Hub + 安全扫描

**支持 7+ 市场：**
| Source | 说明 | 信任级别 |
|--------|------|---------|
| official | Hermes 内置可选技能 | builtin |
| skills-sh | Vercel 官方技能目录 | trusted |
| clawhub | 第三方社区市场 | community |
| lobehub | 聊天 Agent 转换为技能 | community |
| well-known | URL-based discovery | community |
| github | openai/anthropics skills | trusted |
| claude-marketplace | Claude 风格市场 | community |

**安全扫描：** 所有 Hub skill 安装前扫描数据泄露、prompt injection、破坏性命令。

**OpenClaw 现状：** clawhub 无 trust levels、无自动安全扫描

---

### ⚙️ 机制 5：Skills 条件激活 (fallback)

```yaml
metadata:
  hermes:
    fallback_for_tools: [web_search]  # 没有 web_search 时显示
    requires_tools: [terminal]          # 有 terminal 时显示
```

**典型案例：** `duckduckgo-search` 在没有 Firecrawl API key 时自动作为 fallback 显示。

**OpenClaw 现状：** 无此机制，skills 永远是 active

---

### 🔧 机制 6：Skills 配置管理

```yaml
metadata:
  hermes:
    config:
      - key: wiki.path
        description: Path to the wiki directory
        default: "~/wiki"
        prompt: Wiki directory path
```

Skills 可声明 required_environment_variables，加载时安全请求，不消失于 discovery。

---

### 📁 机制 7：External Skill Directories

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
```

外部目录只读，Agent 创建写入 ~/.hermes/skills/，本地优先。

---

## 三、功能对比总结

| 功能 | HermesAgent | OpenClaw | 优势 |
|------|------------|---------|------|
| 多平台消息 | ✅ | ✅ | 平手 |
| Skills 系统 | ✅ 完整 | ✅ 基础 | **Hermes** |
| Progressive Disclosure | ✅ L0/L1/L2 | ❌ | **Hermes** |
| Agent 自主创建 skill | ✅ | ❌ | **Hermes** |
| Memory 容量限制 | ✅ 硬限制 | ❌ | **Hermes** |
| Frozen Snapshot | ✅ | ❌ | **Hermes** |
| Session Search | ✅ FTS5+LLM | ⚠️ 简单 jq | **Hermes** |
| Skills Hub 多源 | ✅ 7+ sources | ⚠️ clawhub 为主 | **Hermes** |
| 安全扫描 | ✅ 自动 | ❌ | **Hermes** |
| Trust levels | ✅ | ❌ | **Hermes** |
| Conditional activation | ✅ | ❌ | **Hermes** |
| External dirs | ✅ | ❌ | **Hermes** |
| 模型路由 | 200+ | 35+ | 平手 |
| 模型 Failover | ⚠️ | ✅ | **OpenClaw** |
| 移动节点 | ❌ | ✅ iOS/Android | **OpenClaw** |
| macOS companion | ❌ | ✅ | **OpenClaw** |

---

## 四、蒸馏方案（移植到 OpenClaw）

### 优先级矩阵

| 优先级 | 机制 | 难度 | 价值 | 推荐 |
|--------|------|------|------|------|
| P0 | Progressive Disclosure | 中 | 极高（省 token） | ⭐⭐⭐⭐⭐ |
| P0 | Memory 容量限制 + Frozen Snapshot | 低 | 高 | ⭐⭐⭐⭐⭐ |
| P1 | Agent 自主创建 skill | 高 | 极高 | ⭐⭐⭐⭐ |
| P1 | Skills Hub 多源整合 | 中 | 高 | ⭐⭐⭐⭐ |
| P1 | 安全扫描流程 | 中 | 高 | ⭐⭐⭐⭐ |
| P2 | Conditional Activation | 低 | 中 | ⭐⭐⭐ |
| P2 | External Skill Directories | 低 | 中 | ⭐⭐⭐ |
| P2 | Skills 配置管理 | 低 | 中 | ⭐⭐⭐ |
| P3 | Session Search (FTS5) | 高 | 高 | ⭐⭐⭐ |

---

### 🚀 P0 - 必须实施

#### P0-1：Progressive Disclosure

```
Step 1: 修改 available_skills 注入 → 只注入 L0 索引
Step 2: 新增 tools: skills_list() + skill_view(name, path?)
Step 3: L0 只含 {name, description, category} (~100 chars/skill)
```

#### P0-2：Memory 容量限制 + Frozen Snapshot

```
MEMORY.md 硬限制: 2,200 chars
USER.md 硬限制: 1,375 chars
超限 → 返回错误 + 引导整理
Frozen Snapshot: 会话启动注入，会话中修改不下发
```

---

### 🎯 P1 - 推荐实施

#### P1-1：Agent 自主创建 skill（难度高）

```typescript
// 新增 tool: skill_manage
// 触发：任务 > 5 tool calls / 用户纠正 / 失败后重试成功
// 保存: ~/.openclaw/skills/[category]/[name]/
```

#### P1-2：Skills Hub 多源整合

```bash
# 扩展 clawhub CLI
npx clawhub search <q> --source skills-sh   # Vercel
npx clawhub search <q> --source github      # openai/anthropics
# 实现 trust levels + 安全扫描
```

---

### 🔄 P2 - 条件实施

#### P2-1：Conditional Activation

SKILL.md 新增：
```yaml
metadata:
  openclaw:
    fallback_for_tools: [web_search]
    requires_tools: [terminal]
```

#### P2-2：External Skill Directories

config 新增：
```yaml
skills:
  external_dirs:
    - ~/.agents/skills
```

---

## 五、实施路径

```
Phase 1: 快速胜利 (1-2 天)
├── P0-2: Memory 容量限制 + Frozen Snapshot
├── P2-1: Conditional Activation
└── P2-2: External Skill Directories

Phase 2: 核心价值 (1 周)
├── P0-1: Progressive Disclosure
├── P1-2: Skills Hub 多源整合
└── P1-3: 安全扫描流程

Phase 3: 高级特性 (2-3 周)
├── P1-1: Agent 自主创建 skill
└── P3-1: Session Search (可选)
```

---

## 六、审查清单

- [ ] **Token 节省重要吗？** Progressive Disclosure 可省 30-50% skill token
- [ ] **MEMORY.md 有膨胀问题吗？** 当前是否越来越长？
- [ ] **担心 skill 安全吗？** 是否需要安装前扫描？
- [ ] **需要更多 skill 市场吗？** skills.sh 等
- [ ] **希望 Agent 自动学习吗？** skill_manage

---

## 七、参考资料

- HermesAgent Docs: https://hermes-agent.nousresearch.com/docs/
- HermesAgent GitHub: https://github.com/NousResearch/hermes-agent
- ClawHub: https://clawhub.ai

*报告生成：2026-04-14*
