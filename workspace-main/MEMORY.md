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
