# Phase 2 实施方案 (2026-04-14)

## 当前状态

### OpenClaw 已有的机制
1. **Skills List**: `formatSkillsForPrompt` 在 system prompt 中注入 skills 列表，包含 name/description/location
2. **按需加载**: agent 被指导使用 `read` 工具加载 SKILL.md（location 路径）
3. **安全扫描**: `dangerous-code scanner` 在 skill install 时运行
4. **Session Snapshot**: skills 在会话启动时快照，复用整个会话

### 差距分析
| 机制 | HermesAgent | OpenClaw | 差距 |
|------|------------|---------|------|
| skills_list() | ✅ L0 索引 | ❌ 无独立工具 | 需插件 |
| skill_view(name) | ✅ 完整内容 | ❌ 靠 read | 需插件 |
| skill_view(name,path) | ✅ references | ❌ 无 | 需插件 |
| 分类 (category) | ✅ 有 | ❌ 无 | 可选 |
| 显式按需加载工具 | ✅ | ❌ 隐式 | 需插件 |

---

## 实施方案

### 方案 A：Plugin 实现 Progressive Disclosure（推荐）

**原理：** 创建一个 OpenClaw plugin，提供 `skills_list` 和 `skill_view` 工具

```typescript
// skills_list: 返回 L0 索引
// skill_view(name): 返回完整 SKILL.md
// skill_view(name, path): 返回 references/ 子目录文件
```

**优势：**
- 不修改 OpenClaw 核心代码
- 可通过 plugin 系统分发
- 与现有机制兼容

**工作量：** 约 1-2 周

### 方案 B：修改 Context Engine

**原理：** 创建自定义 Context Engine plugin，修改 system prompt assembly

**工作量：** 约 2-3 周（更复杂）

---

## 实施计划

### Step 1: 创建 Progressive Disclosure Plugin (openclaw-pd)

```
openclaw-pd/
├── openclaw.plugin.json
├── SKILL.md
├── src/
│   └── index.ts      # Plugin entry, 注册 skills_list/skill_view 工具
│   └── skills.ts     # Skill 读取逻辑
└── package.json
```

**工具定义：**

```typescript
// skills_list: L0 索引
registerTool({
  name: "skills_list",
  description: "List all available skills (L0). Returns name, description, category for each skill.",
  parameters: Type.Object({}),
  async execute(_id, _params) {
    return { content: [{ type: "text", text: JSON.stringify(getL0Skills()) }] };
  }
});

// skill_view: L1/L2 完整内容
registerTool({
  name: "skill_view",
  description: "Load full skill content (L1) or specific file (L2).",
  parameters: Type.Object({
    name: Type.String(),
    path: Type.Optional(Type.String())  // 无 path = L1, 有 = L2
  }),
  async execute(_id, params) {
    return { content: [{ type: "text", text: loadSkill(params.name, params.path) }] };
  }
});
```

### Step 2: 扩展 clawhub CLI 多源支持

```bash
# 支持的源：
clawhub search <q> --source clawhub    # 默认
clawhub search <q> --source skills-sh  # Vercel skills.sh
clawhub search <q> --source github      # GitHub openai/anthropics skills
```

### Step 3: 增强 skill-vetter（自动化扫描）

将 manual vetting 流程部分自动化：
- 文件模式检测（curl/wget/exec）
- 外部网络请求检测
- credential 访问检测

---

## 参考资料

- OpenClaw Plugin: https://docs.openclaw.ai/plugins/building-plugins
- Plugin SDK: https://docs.openclaw.ai/plugins/sdk-overview
- Context Engine: https://docs.openclaw.ai/concepts/context-engine

---

*Created: 2026-04-14*

---

## Status Update: 2026-04-15

### Step 1: Progressive Disclosure Plugin
- **Status**: ✅ COMPLETED
- **Verification**: Plugin loaded, provides skills_list/skill_view tools
- **Issues Fixed**: Missing yaml/typebox deps, removed api.logInfo call

### Step 2: clawhub Multi-Source Support  
- **Status**: ❌ NOT FEASIBLE
- **Reason**: clawhub CLI doesn't support --source flag, no public API for skills.sh, GitHub repos don't exist

### Step 3: skill-vetter Automated Scanning
- **Status**: ✅ COMPLETED
- **Created**: `references/vet-scan.sh` - automated pattern scanner
- **Detects**: curl/wget, exec/eval, credential access, suspicious encoding
- **Verified**: All local skills pass (agent-reach, stock-market-pro, humanizer, summarize, proactive-agent)
