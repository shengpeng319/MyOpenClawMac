# Phase 3：运行时记忆同步系统

**设计日期：** 2026-04-15
**目标：** 解决"会话过程中记忆丢失"的核心问题

---

## 问题分析

### 当前架构问题

```
会话启动 → MEMORY.md 注入 → 会话中 → 记忆全靠 prompt 回传
                              ↓
                    memory/ 文件更新了
                              ↓
                    但当前会话看不到（Frozen Snapshot）
```

### HermesAgent 的解法

HermesAgent 有 `skill_manage` 工具让 Agent **在会话中主动更新记忆**，但当前会话也不生效（设计选择）。

**核心 insight：** Hermes 没有解决"当前会话记忆同步"，它解决的是"跨会话记忆积累"。

### OpenClaw 的真正需求

1. **会话中**：Agent 能感知到最近的上下文（不被遗忘）
2. **跨会话**：重要记忆能持久化
3. **按需召回**：能搜索历史记忆片段

---

## 解决方案：Memory Sync Plugin

### 架构设计

```
memory-sync plugin/
├── index.ts           # Plugin entry，提供 3 个工具
├── memory-store.ts     # 记忆存储逻辑
└── snapshot.ts        # 增量快照机制

memory 文件结构：
~/.openclaw/
├── MEMORY.md              # 主记忆（已精简，~2,200 chars）
├── USER.md                # 用户画像（~1,375 chars）
├── memory/
│   ├── YYYY-MM-DD.md      # 每日记忆片段
│   ├── pending.json        # 待注入的增量更新 ← 关键！
│   └── heartbeat-state.json
└── memory-sync/
    └── .last-inject       # 上次注入的时间戳
```

### 核心工具

#### 1. `memory_update` — 记忆更新

```typescript
registerTool({
  name: "memory_update",
  description: "将重要信息写入持久记忆。会话中更新不重新注入当前会话，但会在下次会话生效。",
  parameters: Type.Object({
    content: Type.String(),      // 要记忆的内容
    priority: Type.Union([      // 优先级
      Type.Literal("critical"), // 立即可见（存 pending）
      Type.Literal("normal"),   // 下次会话可见
      Type.Literal("context")   // 仅当前上下文参考
    ]),
    tags: Type.Array(Type.String())  // 标签，方便搜索
  }),
  async execute(_id, params) {
    // 1. 写入 memory/YYYY-MM-DD.md
    // 2. 如果 priority=critical，写入 memory/pending.json
    // 3. 如果是 critical 且当前会话，返回注入提示
  }
});
```

#### 2. `memory_search` — 记忆搜索

```typescript
registerTool({
  name: "memory_search",
  description: "搜索所有记忆文件，返回相关内容片段。",
  parameters: Type.Object({
    query: Type.String(),
    limit: Type.Optional(Type.Number()),
    files: Type.Optional(Type.Array(Type.String()))
  }),
  async execute(_id, params) {
    // 搜索 memory/*.md + pending.json
    // 返回匹配片段 + 文件来源
  }
});
```

#### 3. `memory_snapshot` — 获取当前记忆状态

```typescript
registerTool({
  name: "memory_snapshot",
  description: "获取当前记忆状态（已注入 + 待注入 + pending）",
  parameters: Type.Object({}),
  async execute(_id, _params) {
    // 返回 MEMORY.md + pending.json 内容
    // 让 Agent 知道当前"记忆全景"
  }
});
```

---

## 关键机制：Pending Inject

### 为什么需要 pending.json？

MEMORY.md 是在会话启动时**一次性注入**的，运行时修改不会更新当前会话 prompt。

**解决方案**：创建 `pending.json`，下次会话启动时先注入 pending 内容。

```json
// memory/pending.json 格式
{
  "updates": [
    {
      "id": "uuid",
      "content": "今天发现 progressive-disclosure 插件有 3 个问题...",
      "tags": ["phase2", "plugin"],
      "created": "2026-04-15T09:00:00Z",
      "priority": "critical"
    }
  ],
  "lastSession": "2026-04-15T09:00:00Z"
}
```

### 注入流程

```
会话启动
    ↓
读取 pending.json
    ↓
将 updates 格式化注入到 system prompt
    ↓
清空 pending.json（或保留 24h 内的 critical）
    ↓
正常加载 MEMORY.md + USER.md
```

### Agent 行为指南

```
1. 重要发现 → 调用 memory_update(priority="critical")
2. 当前会话想参考 → 调用 memory_search
3. 想确认当前记忆状态 → 调用 memory_snapshot
4. 每次心跳后 → 自动检查是否需要 memory_update
```

---

## 实施计划

### Step 1: 创建 memory-sync plugin (2026-04-15)

```
memory-sync/
├── index.ts          # 3 个工具注册
├── memory-store.ts   # 读写逻辑
├── pending.ts         # pending.json 管理
└── openclaw.plugin.json
```

### Step 2: 实现 memory_update 工具

- 写入 `memory/YYYY-MM-DD.md`
- 写入 `memory/pending.json` (priority=critical)
- 返回确认 + 提示下次会话可见

### Step 3: 实现 memory_search 工具

- 搜索 `memory/*.md` + `pending.json`
- 支持 tag 过滤
- 返回片段 + 来源

### Step 4: 实现 memory_snapshot 工具

- 读取 MEMORY.md + pending.json
- 返回"当前记忆全景"

### Step 5: 修改会话启动逻辑（如果可能）

在 AGENTS.md 中添加规则：
```
每次会话启动时，检查 pending.json，
如果有更新，先注入，再加载 MEMORY.md
```

### Step 6: heartbeat 整合

修改 HEARTBEAT.md：
```
每次心跳检查：
1. pending.json 是否有未处理的 critical 更新
2. 如果有，返回提示给用户
3. 如果没有，静默
```

---

## 验证方法

### Test 1: memory_update 写入
```bash
# 调用 memory_update(priority="critical", content="Phase 2 完成")
# 检查 memory/pending.json 是否有内容
```

### Test 2: 跨会话记忆持久化
```bash
# 会话 A: memory_update("重要信息")
# 会话 B: 检查是否能看到"重要信息"
```

### Test 3: memory_search 搜索
```bash
# memory_search("Phase 2")
# 验证能返回相关记忆片段
```

---

## Phase 3 vs Phase 1/2 关系

| Phase | 关注点 | 解决的问题 |
|-------|--------|-----------|
| Phase 1 | 记忆容量 + Frozen Snapshot | 记忆文件膨胀、格式规范 |
| Phase 2 | Skills 管理（Progressive Disclosure） | Skills 加载效率 |
| **Phase 3** | **运行时记忆同步** | **会话中记忆丢失** |

Phase 3 依赖 Phase 1 的 MEMORY.md 精简（不然注入太多）。

---

## 风险与限制

1. **pending.json 注入需要修改会话启动逻辑** — 可能需要 OpenClaw 核心支持
2. **Agent 可能过度依赖 memory_update** — 需要 guidelines
3. **pending.json 可能膨胀** — 需要清理机制（72h 自动删除）

---

*设计完成，等待实现*
