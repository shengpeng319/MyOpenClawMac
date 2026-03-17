# 长期记忆

## 课程提醒功能

### 配置信息
- **定时任务**：每天早上 7:05 自动发送课程提醒
- **群聊 ID**：oc_49bd38a7e7152bafbb125392b40e2939
- **Cron Job ID**：042e920d-1dd9-48e3-809b-a39cd1f37998

### 提醒内容
1. 日期和天气情况
2. 两个孩子的课程安排 + 出发时间
3. 关怀提醒：
   - 连续上课时间冲突 → 提醒提前点餐
   - 天气变化 → 提醒带伞/穿衣
   - 其他暖心提示

### 数据存储
- 课程表：USER.md（长期）+ memory/日期.md（日常）
- 地点路程：USER.md 中记录

### 维护方式
- 课程有变化 → 更新 USER.md 中的课程表
- 需要新日历 → 生成 .ics 文件导入手机

---

## 飞书文件传输 (2026-03-16)

### 经验教训
- 通过飞书发送文件时，文件必须放在允许的目录
- **允许的目录列表**：
  - `~/.openclaw/media/`
  - `~/.openclaw/agents/`
  - `~/.openclaw/workspace/`
  - `~/.openclaw/sandboxes/`
- **不在允许列表**：`~/.openclaw/transfers/` ❌

### 操作步骤
1. 把文件复制到 `~/.openclaw/media/` 目录
2. 使用 `--media ~/.openclaw/media/文件名` 发送

### 课程表Excel
- 已发送到用户
- 文件位置：`~/.openclaw/media/课外班课程表.xlsx`
