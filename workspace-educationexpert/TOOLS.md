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

## IMA 文档 API 凭证 (from Claire, 2026-03-28)

### 凭证
- IMA_OPENAPI_CLIENTID: 8f7c7807145b50a8961dcb039ecb582c
- IMA_OPENAPI_APIKEY: 1qXFcb8DynB3ssIlZzPuQFFrYpYswW3pJvfX0uBvHbdJcQC/wUs2y2ShKDCl25Ew2K/ezv3FJA==

### 用途
- IMA 在线文档读写（Agent 开发课程课件）
- 用于上传审核笔记到 IMA

### 备注
- 凭证有效期未知
- 如遇 API 错误，检查凭证是否过期
