---
name: course-reminder-cron
description: 课程提醒 Cron 任务系统。每早 07:05 发送当日课程安排，并动态为每门课程创建课程开始前 20 分钟的出发提醒 Cron（one-shot，执行后自动删除）。当用户要求创建、修复、重建课程提醒 Cron 时触发。
---

# 课程提醒 Cron 任务系统

## 架构

```
每日 07:05 主 Cron
    ↓ 执行
1. 发送当日课程安排到飞书群
2. 读取 USER.md 获取当天课程
3. 为每门课创建 one-shot 子 Cron（课程前20分钟触发）
    ↓
子 Cron（课程前20分钟）
    ↓ 执行
发送出发提醒到飞书群
执行后自动删除
```

## 主 Cron 创建命令

```bash
openclaw cron add \
  --name "课程提醒" \
  --agent educationexpert \
  --announce \
  --channel oc_49bd38a7e7152bafbb125392b40e2939 \
  --cron "5 7 * * *" \
  --timeout-seconds 180 \
  --message "今天的课程安排已发送。现在请为每门课程创建单独的出发提醒 Cron 任务（课程开始前20分钟触发，执行后自动删除）。

课程表在 USER.md 中，格式如下：
- 蛋蛋/妞妞 | 课程名 | 星期X | 出发时间 | 课程时间 | 地点

步骤：
1. 读取 USER.md 获取今天的课程列表
2. 计算每门课的开始时间对应的出发提醒时间（课程开始前20分钟）
3. 用 exec 工具调用 openclaw cron add 为每门课创建单独的 Cron：
   - 使用 --at 选项指定具体触发时间（用 ISO 格式，如 2026-04-15T18:20:00+08:00）
   - 使用 --delete-after-run 确保执行后自动删除
   - 使用 --message 指定出发提醒内容
4. 创建完成后输出已创建的子 Cron 数量"
  --description "每日课程提醒"
```

## 子 Cron 创建逻辑（Agent 在运行时执行）

当主 Cron 触发时，Agent 需要：

1. **读取 USER.md** 获取课程表
2. **判断今天是星期几**，筛选出今天的课程
3. **计算出发时间**：课程开始时间 - 20 分钟
4. **为每门课创建 one-shot Cron**：
   ```bash
   openclaw cron add \
     --name "{学生昵称}-{课程名}-出发提醒-{日期}" \
     --agent educationexpert \
     --announce \
     --channel oc_49bd38a7e7152bafbb125392b40e2939 \
     --at "{ISO时间}" \
     --delete-after-run \
     --message "🎉 出发提醒！{学生昵称}，{课程名} 即将开始！
   
   ⏰ 出发时间：{出发时间}
   📍 地点：{地点}
   🕐 课程时间：{课程时间}
   
   记得带：{必带物品}"
   ```
5. **输出创建的子 Cron 数量**

## 关键参数

| 参数 | 值 |
|------|-----|
| 主 Cron ID | `691ef0dd-7238-4c00-aefb-4433bc7e3af4` |
| 群聊 ID | `oc_49bd38a7e7152bafbb125392b40e2939` |
| Agent | `educationexpert` |
| 触发时间 | 每天 07:05 |
| 子 Cron 超时 | 180 秒（主 Cron 需要时间创建多个子任务）|

## 常见问题

**Q: 子 Cron 没有创建成功？**
A: 检查主 Cron 的 --timeout-seconds 是否足够（建议 180s）

**Q: 出发提醒没有发送到群聊？**
A: 检查 --channel 和 --to 参数，ID 格式应为 `oc_xxx`（无前缀）

**Q: 如何手动测试？**
```bash
# 触发主 Cron
openclaw cron run 691ef0dd-7238-4c00-aefb-4433bc7e3af4

# 查看运行历史
openclaw cron runs --id 691ef0dd-7238-4c00-aefb-4433bc7e3af4
```
