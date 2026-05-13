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
| Jarvis → Hermes | `agent:main:explicit:hermes-to-openclaw-1` | ✅ 确认 | 复用 Hermes → Jarvis 同一 channel |
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

---

## Plugin 冲突排查（2026-04-18）

- **现象**：`gateway.err.log` 每 5 秒报 `plugin tool name conflict (memory-sync): memory_search`
- **根因**：memory-sync 和 memory-core 同时启用，都注册了 `memory_search` 工具
- **影响**：仅警告日志（每 5 秒一条），不影响核心功能，但日志盘占用缓慢增长
- **解法**：禁用 memory-sync，保留 memory-core（更稳定的内置插件）
- **操作**：修改 `~/.openclaw/openclaw.json` 中 `plugins.entries.memory-sync.enabled: false`，然后 `~/.nvm/versions/node/v24.14.1/bin/openclaw gateway restart`

*Updated: 2026-04-18*

---

## 飞书发送文本消息规范（2026-04-19 固化）

**坑**：直接传原始文本给 `content` 字段会报 `230001 content is not a string in json format`

**正确格式**：
```python
payload = {
    "receive_id": "ou_c858ba4fbb03f207666daef058ede895",
    "msg_type": "text",
    "content": json.dumps({"text": text_content}, ensure_ascii=False)
}
```
飞书 text 消息的 `content` 必须是 **JSON 字符串**（`json.dumps` 后的结果），内容本身是 `{"text": "..."}` 结构。

**完整流程**：
```python
# 1. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a9f6e7b152399cc2","app_secret":"..."}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

# 2. 发消息
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"ou_...","msg_type":"text","content":"{\"text\":\"消息内容\"}"}'
```

---

## sessions.send 大消息失败教训（2026-04-19 固化）

**现象**：`stopReason: aborted`，消息根本发不出去

**根因**：
1. 2000+ 字的消息体走 gateway call 不稳定，JSON 转义链路长容易断裂
2. 超大消息 gateway 直接 `aborted`

**解法**：
- 大段文字/报告 → 先写文件，再用飞书 API 直发（不走 sessions.send）
- 文件路径共享给接收方

**降级原则**：
| 消息大小 | 推荐方式 |
|----------|----------|
| < 500 字 | `sessions.send` 或飞书 API 都行 |
| > 500 字 | 飞书 API 直接发 |
| > 2000 字 | 必须写文件 + 飞书 API |

---

## MiniMax API Key 类型区分（2026-04-19 固化）

| Key 前缀 | 类型 | 视频 | 音乐 | 搜索/图片 |
|----------|------|------|------|-----------|
| `sk-cp-` | Token Plan 专用 | ❌ 不支持 | ❌ 不支持 | ✅ 支持 |
| 普通 Key | 通用 API | ✅ 支持 | ✅ 支持 | ✅ 支持 |

**判断方法**：
- Token Plan Key：`sk-cp-` 开头，用于 MCP 联网/图片理解
- 普通 API Key：用于视频生成、音乐生成

**教训**：之前一直用 Token Plan Key 调视频生成，失败原因是 Key 类型不对，不是代码问题。

---

## Jarvis ↔ Hermes 协作协议更新（2026-04-19 修正）

### 错误记录
之前把消息发到了 `agent:main:feishu:direct:ou_c858ba4fbb03f207666daef058ede895`（这是 Jarvis 自己的飞书 session），而不是 Hermes 的 session。

### 正确 channel
- **Hermes → Jarvis**：`agent:main:explicit:hermes-to-openclaw-1` ✅
- **Jarvis → Hermes**：`agent:main:explicit:hermes-to-openclaw-1` ✅（复用同一 channel）
  - 注意：这是 OpenClaw 内部 session，不是飞书 P2P session

### 协作内容交换
通过**共享文件路径**交换大内容，避免 sessions.send 大消息丢失。

*Updated: 2026-04-19*

---

## ⚠️ MiniMax M2.7-highspeed 模型 Token Plan 过期（2026-04-22）

- **现象**：`HTTP 500 api_error: your current token plan not support model, MiniMax-M2.7-highspeed (2061)`
- **影响**：所有使用 MiniMax-M2.7-highspeed 模型 的 Cron Job 失败（早安问候等）
- **根因**：MiniMax token plan 可能不支持 M2.7-highspeed 模型，或配额已用尽
- **排查方向**：
  1. 检查 OpenClaw 配置的 model 设置
  2. 确认 MiniMax 账户配额/订阅状态
  3. 考虑切换到其他模型（如 qwen3.5 作为 fallback）
- **状态**：⏳ 待处理

*Updated: 2026-04-22*

---

## DeepSeek API Key（2026-04-27 记录）

- **Key**: `sk-4cbe644d7308470494f870f310a36a5b`
- **用途**: 可用于 deepseek/deepseek-v4-pro 模型
- **配置位置**: `~/.openclaw/openclaw.json` → `models.deepseek/deepseek-v4-pro`

## 模型切换记录（2026-04-27）

- **当前默认模型**: `minimax-cn/MiniMax-M2.7-highspeed`（所有 Agent 统一）
- **DeepSeek V4 Pro**: 曾在 2026-04-26 短暂切换，但已切回 MiniMax
- **之前 MiniMax Token Plan 过期问题（2026-04-22）**: 已在 2026-04-27 前恢复，模型正常运行

*Updated: 2026-04-27*

---

## ⚠️ Yahoo Finance 在中国大陆不可用（2026-05-09 重大教训）

- **发现**：大龙虾金融研报 cron 连续失败，`curl -s "https://query1.finance.yahoo.com"` 被 GFW 墙
- **影响**：所有使用 Yahoo Finance 的 Cron Job 全部失败
- **解决**：必须切换到国内数据源
  - **首选**：东方财富 API（`push2.eastmoney.com` 或 `push2his.eastmoney.com`，无需 key，免费）
  - **备选**：新浪财经 API（`hq.sinajs.cn`）
  - **备选**：AKShare + FastAPI 本地缓存（Python 库，聚合多个国内源）
- **原则**：中国大陆环境优先使用国内数据源，不假设境外服务可用
- **教训**：从一开始就不应该用 Yahoo Finance

*Updated: 2026-05-09*

---

## Provider 超时容错策略（2026-05-10 固化）

- **现象**：晚间 20:03-20:33 MiniMax 模型大规模连接超时，约 18 次心跳轮询全部失败
- **教训**：Provider 超时不应触发重复快速尝试，应等待下一个心跳周期（约5分钟）
- **原因**：Provider 在晚间高负载期间，重复调用会雪崩式加重负担
- **策略**：
  1. 单次超时 → 不重试，等待下次心跳（5分钟后）
  2. 连续 3 次超时 → 在状态文件中标记 provider 降级
  3. 安静时段（23:00-08:00）→ 超时直接跳过，不记录

---

## 安静时段预判机制（2026-05-10 固化）

- **现象**：接近 23:00 时反复判断是否要写状态文件，逻辑分散
- **教训**：应提前一个时段窗口（如 22:00 起）就停止状态写入
- **策略**：
  - 22:00 之前 → 按 30 分钟间隔维护
  - 22:00-23:00 → 最后一次写入后不再写
  - 23:00-08:00 → 仅记录必要的异常，不做维护写入

*Updated: 2026-05-10*
