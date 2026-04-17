# MEMORY.md - Long-term Memory

*Curated knowledge from past sessions*

---

## OpenClaw 核心规则

- **编程任务 → OpenCode** (`~/.opencode/bin/opencode`)
- **分解思考 → 执行 → 迭代 (3轮) → 求助**
- **跨 agent 通知 → 发绝对路径，不依赖对方搜索**

## 飞书配置

- App ID: `cli_a9f6e7b152399cc2`
- 发送图片: `/im/v1/images` → `image_type=message`
- 发送文件: `/im/v1/files`
- token 有效期 2 小时

## sessions_send CLI Workaround

```bash
MSG=$(echo "消息" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
openclaw gateway call sessions.send --params "{\"key\":\"<key>\",\"message\":$MSG}" --timeout 300000
```

## GitHub Token

- Token: （已迁移到 TOOLS.md 或凭证管理器）
- Repo: shengpeng319/MyOpenClawMac

## Skills

- clawhub CLI: `npx clawhub`
- 重要 skill: agent-reach, stock-market-pro, proactive-agent, humanizer

## Agent Session Keys

- researcher: `ou_cf1a1ee3279590e248bcfed4d0838c22`
- financialadvisor: `ou_cd9dabe38e7378c0eef8b7a6c048591e`

---

*Updated: 2026-04-14*

---

## classmgr Service (2026-04-15)

**用途**：课程管理前后端服务
**Frontend**（H5）：`http://localhost:5173/classmgr/`，局域网 `http://192.168.101.50:5173/classmgr/`
**Server**：`http://localhost:3000`

**启动方式**：launchd（~/Library/LaunchAgents/）
- `com.shengpeng319.classmgr-frontend.plist`（H5）
- `com.shengpeng319.classmgr-server.plist`（Server）

**vite.config.ts 修改**：加 `server: { host: '0.0.0.0', port: 5173 }` 使局域网可访问
**命令**：`npm run dev:h5` / `npm run dev`

*Updated: 2026-04-15*

---

## 飞书音频发送方式（已验证，2026-04-15）

**上传**：`POST /im/v1/files` → `file_type=opus`
**发送**：`POST /im/v1/messages` → `msg_type=audio`，content 为 `{"file_key":"..."}`
注意：MP3/音频文件上传时必须用 `opus` 类型，不是 `audio` 不是 `mp3`

## MiniMax music-2.6 模型（2026-04-15）

- 直接 POST 到 `https://api.minimaxi.com/v1/music_generation`（不走 OpenClaw 对话模型）
- 生成音频示例：`/tmp/test_music.mp3`

---

## 三虾鼎立架构 (2026-04-17)

**核心原则：各司其职，不要多个实例同时跑同样的 Cron**

| 实例 | 角色 | 职责 |
|------|------|------|
| 🫡 Jarvis（小虾/我） | 战略 + 协调 | 新任务快速上手、深度研究、长程规划、实验性工作 |
| 🦞 大龙虾 | 主运行实例 | 所有 Cron 定时任务：量化研报、教育提醒、每日进化报告 |
| 🦎 Hermès | 外部邻居 | 独立运作，不合并不同步，跨实例协作时再说 |

**Sub-agent 归属**：financialadvisor、educationexpert 等全部挂在大龙虾下

**跨实例通信**：
- Hermes → Jarvis：`sessions_send` 到 `agent:main:explicit:hermes-to-openclaw-1`
- 大龙虾 → Jarvis：通过飞书或 Hermes 中转

**长期协作可能性**：
- 知识共享：研报分析逻辑、教育提醒配置可互相借鉴
- 踩坑互助：发现新坑及时互通

*Updated: 2026-04-17*

---

## Hermes 协作协议（双向通道，2026-04-17 固化）

### 通道现状

| 方向 | Session Key | 状态 | 备注 |
|------|-------------|------|------|
| Hermes → Jarvis | `agent:main:explicit:hermes-to-openclaw-1` | ✅ 稳定 | 长期不变 session key |
| Jarvis → Hermes | `agent:main:feishu:direct:ou_c858ba4fbb03f207666daef058ede895` | ✅ 确认 | Hermes 在本飞书 app 的 user session |
| 大龙虾 → Jarvis | 通过 Hermes 中转 | ⏳ 待建 | 需 Hermes 配合 |

### 发送命令（Jarvis → Hermes）

```bash
MSG=$(echo "消息内容" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
openclaw gateway call sessions.send \
  --params "{\"key\":\"agent:main:feishu:direct:ou_c858ba4fbb03f207666daef058ede895\",\"message\":$MSG}" \
  --timeout 300000
```

### 注意事项
- Hermes 是**外部独立实例**，session key 可能因重启改变，以 sessions_list 查询结果为准
- Hermes 的飞书 open_id 不与本 app 共享，不可跨 app 发 Feishu 消息
- 建议协作内容通过**共享文件路径**交换（减少大消息丢失风险）

*Updated: 2026-04-17*

---

## 新技术点记录（2026-04-17）

### 1. Skills 条件激活（metadata.openclaw）

```yaml
metadata:
  openclaw:
    fallback_for_tools: [web_search]  # 没有这些工具时技能显示（兜底）
    requires_tools: [terminal]         # 有这些工具时技能才显示（增强）
```
两个字段**叠加**：必须同时满足才显示。不支持动态检测，依赖 OpenClaw 启动时扫描。

### 2. TaskFlow 解耦记忆共享机制

TaskFlow subagent **不共享 session 内存**，靠**状态文件**传递：
- `memory/taskflow/{flowId}.json` → 共享 stateJson（结构化状态袋）
- `memory/taskflow/{subTaskId}.json` → 子任务 output（文件路径/结果）
- 父任务通过读子任务 output 文件实现跨 subagent 数据获取

### 3. 飞书发文件/音频坑（file_type=opus）

- 音频/MP3 文件上传时 `file_type` **必须**用 `opus`，不能用 `audio` 或 `mp3`
- 第一次发送空内容后会触发重新上传（已知问题）
- 所有非图片文件走 `/im/v1/files` → `file_type=opus`

### 4. Cron 超时参数（timeout vs enforce_timeout）

| 参数 | 作用 | 默认值 |
|------|------|--------|
| `--timeout` | 单次 cron job 执行超时 | 30000ms |
| `agents.defaults.timeoutSeconds` | agent 运行时长硬上限 | 172800s（48h）|
| `enforce_timeout`（cron config）| 维护模式：超 disk budget 是否强制清理 | - |

### 5. Session Key 格式规范

```
agent:<agentId>:<channel>:<sessionLabel>
```
- `<agentId>`: 实例名（如 `main`、`hermes`）
- `<channel>`: `explicit`（显式创建）、`feishu`（飞书 P2P）、`subagent`（子任务）
- `<sessionLabel>`: 描述性名称，建议用 `{方向}-{序号}` 格式

飞书 P2P session key: `agent:main:feishu:direct:ou_{openid}`

*Updated: 2026-04-17*
