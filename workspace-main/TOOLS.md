# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## OpenClaw 一键重启

```bash
~/.nvm/versions/node/v24.14.1/bin/openclaw gateway restart
```

**路径速查：**
- 二进制：`~/.nvm/versions/node/v24.14.1/bin/openclaw`
- 配置：`~/.openclaw/openclaw.json`
- Gateway 日志：`~/.openclaw/gateway.log` / `gateway.err.log`
- Workspace：`~/.openclaw/workspace-main/`
- Agents：`~/.openclaw/agents/*/agent/`

## 智谱 MCP 优先级规则（2026-05-25）

**视觉处理、网络搜索、网页读取 → 优先使用智谱 MCP**

| 场景 | 优先工具 | 命令 |
|------|----------|------|
| 网络搜索 | `web-search-prime.web_search_prime` | `mcporter call web-search-prime.web_search_prime search_query="..."` |
| 网页读取 | `web-reader.webReader` | `mcporter call web-reader.webReader url="..."` |
| 开源仓库 | `zread.search_doc` / `read_file` / `get_repo_structure` | `mcporter call zread.search_doc repo_name="..." query="..."` |
| 视觉理解 | `zai-vision.*` | `mcporter call zai-vision.image_analysis ...` |

**配置文件**：`~/.mcporter/mcporter.json`
**API Key**：智谱 zai key（已配置在 MCP env/headers 中）
**降级**：智谱 MCP 不可用时 → tavily → agent-reach → curl

*Updated: 2026-05-25*

## 模型使用规范（2026-05-26 用户明确要求）

**所有任务统一用 GLM-5.1，禁止使用 GLM-4.6v-flash**

| 场景 | 模型 | 备注 |
|------|------|------|
| 对话/Cron/所有 Agent | `zai/glm-5.1` | 默认模型，不再用 4.6v-flash |
| 视觉理解 | 智谱 MCP `zai-vision.*` | 走 MCP 不走模型原生视觉 |

**原因**：4.6v-flash 下午频繁 429 限流，5.1 更稳定

*Updated: 2026-05-26*
