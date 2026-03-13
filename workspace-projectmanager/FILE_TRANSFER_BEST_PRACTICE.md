# 文件传输最佳实践 - 本地文件发送到飞书

## 核心原则

**发送本地文件到飞书，必须先复制到 transfers 目录**

飞书插件有安全限制：不允许从 `workspace-*` 开头的目录读取媒体文件。因此需要使用中转目录。

---

## 目录说明

| 目录 | 用途 |
|------|------|
| `~/.openclaw/transfers/` | 飞书文件传输中转目录 |
| `~/.openclaw/workspace-*/artifacts/` | 产出物存放目录（禁止直接发送） |

---

## 发送流程

### Step 1: 复制文件到中转目录

```bash
# 复制文件到 transfers 目录
cp 你的文件路径 ~/.openclaw/transfers/文件名
```

### Step 2: 使用 --media 参数发送

```bash
npx openclaw message send \
  --channel feishu \
  --account main \
  --target 用户的飞书ID \
  --message "文件发送" \
  --media ~/.openclaw/transfers/文件名
```

---

## 常见场景

### 场景1: 发送 Excel 文件

```bash
# 1. 复制文件
cp ~/Downloads/report.xlsx ~/.openclaw/transfers/report.xlsx

# 2. 发送文件
npx openclaw message send --channel feishu --account main --target ou_xxx --message "报告" --media ~/.openclaw/transfers/report.xlsx
```

### 场景2: 发送视频

```bash
# 1. 复制文件
cp ~/Videos/demo.mp4 ~/.openclaw/transfers/demo.mp4

# 2. 发送视频
npx openclaw message send --channel feishu --account main --target ou_xxx --message "视频" --media ~/.openclaw/transfers/demo.mp4
```

### 场景3: 发送图片

```bash
# 1. 复制文件
cp ~/Pictures/photo.png ~/.openclaw/transfers/photo.png

# 2. 发送图片
npx openclaw message send --channel feishu --account main --target ou_xxx --message "图片" --media ~/.openclaw/transfers/photo.png
```

---

## 错误排查

### 错误: "path-not-allowed"

**原因**: 文件在 `workspace-*` 目录下，触发了安全限制

**解决**: 先复制到 `~/.openclaw/transfers/` 目录

### 错误: "not-found"

**原因**: 文件路径不存在

**解决**: 检查文件是否已复制到 transfers 目录

---

## 记忆要点

> **重要**: 禁止直接从 `workspace-*` 目录发送文件。必须先复制到 `~/.openclaw/transfers/` 目录。

**关键词**: 飞书, 文件传输, transfers, 附件, media
