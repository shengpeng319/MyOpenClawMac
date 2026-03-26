# HEARTBEAT.md - Memory Maintenance Task

# 每小时执行: 检查每日 memory 文件，把重要内容提炼到 MEMORY.md

## 任务步骤
1. 读取 `memory/YYYY-MM-DD.md` (今天和昨天)
2. 检查是否有新的重要内容（API集成、经验教训、配置变更等）
3. 如果有重要更新，提炼并写入 `MEMORY.md`
4. 更新 `memory/heartbeat-state.json` 的 lastChecks.memory_maintenance

## 重要规则
- 只提炼真正值得长期记忆的内容
- 保留具体命令、路径、配置值等实用信息
- 避免与 MEMORY.md 已有内容重复
- 状态文件: `memory/heartbeat-state.json`

## 触发条件
- 每次心跳时检查
- 两次维护间隔至少 30 分钟 (检查状态文件)
