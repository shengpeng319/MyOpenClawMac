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

---

## Agent 开发课程（2026-03-26）

### 课程概述
- **课程名称**：Agent 开发自学课程
- **学习对象**：Peng Sheng（盛鹏）
- **教学方式**：Diana（educationexpert agent）编写课件 + IMA 在线文档
- **目标**：系统学习 Agent 开发知识体系

### 课件清单（IMA 文档）

| 课 | 名称 | Doc ID | 状态 |
|----|------|--------|------|
| 1 | 什么是 Agent | 7442848899167446 | ✅ 完成 |
| 2 | 核心架构（v3） | 7442898391955752 | ✅ 完成 |
| 3 | 架构模式（v3） | 7442898823970598 | ✅ 完成 |
| 4 | 主流开发框架（v3） | 7442899163683647 | ✅ 完成 |
| 5 | Function Calling 实战（v3） | 7442899469867686 | ✅ 完成 |
| 6 | 记忆系统实战 | 7442902519124115 | ✅ 完成 |
| 7 | 评估与优化 | 7442905752959933 | ✅ 完成 |
| 8 | 安全与防护 | 7442907019639875 | ✅ 完成 |
| 9 | 入门项目 | 7442907476817884 | ✅ 完成 |
| 10 | 常见陷阱 | 7442907787196995 | ✅ 完成 |
| 11 | Agent 的局限性 | 7442930323190905 | ✅ 完成 |


### 课程特点
- v3 版本：重写后保留完整文字讲解 + 代码示例（各约250行）
- 风格：老师讲解式，大量类比和原理说明
- 课件链接格式：`https://ima.qq.com/docx/{doc_id}`

### 学习路径
```
Week 1: LangChain 入门
Week 2: LangGraph 进阶
Week 3: CrewAI 多 Agent
Week 4: 深入一个框架
```

### 相关 Session
- **main session**：agent:main:feishu:direct:ou_c858ba4fbb03f207666daef058ede895
- **educationexpert session**：agent:educationexpert:feishu:direct:ou_fddf58b3579afe9168ad38eea080294f
- **researcher review session**（已完成）：
  - agent:educationexpert:subagent:a0355072-c92e-4db0-9068-ae7a37af6c71
  - agent:educationexpert:subagent:5d0e5ac6-9d1d-41dc-abb2-0b4cced37251

### 经验教训
- **课程改进**：代码量够了但文字说明消失 → v3 版本平衡文字和代码
- **Review 要点**：代码示例需配合文字讲解才是合格课程
- **IMA 上传**：返回 doc_id 为 None 时需重新请求完整响应
