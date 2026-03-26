# 待改进文档 (2026-03-26)

## ACP 配置修复

### 问题描述
- researcher agent 的 ACP runtime 未配置，导致 agent 间无法协作
- sessions_send 超时失败

### 根因
- ❌ 之前以为是 cron isolated session 无法向 direct session 发消息
- ✅ 实际是 ACP runtime 未配置，agent 间通信基础设施有问题

### 修复方案
为所有 agent 配置 `acp.defaultAgent=main`：

| Agent | 状态 |
|-------|------|
| main | 不需要（本身就是主节点） |
| coder | ✅ 已配置 |
| researcher | ✅ 已配置 |
| projectmanager | ✅ 已配置 |
| educationexpert | ✅ 已配置 |
| financialadvisor | ✅ 已配置 |

### 验证
- 明天 6:50 Emily cron 触发，验证 sessions_send 直发是否成功

---

## 调试经验总结

1. 遇到问题 → 先猜根因 → 验证假设 → 修正理解
2. 本质是基础设施层问题（ACP），不是业务逻辑问题
3. 验证后再下结论，避免基于错误假设修复

---

## 明日验证点

- [ ] Emily cron 6:50 → sessions_send → Claire 直接送达
- [ ] RSI bug 修复（P0）

---

*Created: 2026-03-26*
