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

---

## 场景4: 发送音频/音乐文件（API直发）

当 --media 方式无法发送音频时，使用飞书 API 直接上传发送。

### 关键发现

| 步骤 | file_type | msg_type | 说明 |
|------|-----------|----------|------|
| 上传 | `opus` | - | MP3/音频文件必须用 opus 类型上传 |
| 发送 | - | `audio` | 消息类型用 audio，不是 file |

### API 流程

```bash
# 1. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"你的AppID","app_secret":"你的AppSecret"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

# 2. 上传文件 (file_type=opus)
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=文件名.mp3" \
  -F "file=@/path/to/file.mp3" \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('file_key',''))")

# 3. 发送音频消息 (msg_type=audio)
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"用户的open_id\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

### 重要说明

- **上传时 file_type=opus**，不是 audio，不是 mp3
- **发送时 msg_type=audio**，不是 file
- **content 只有 file_key**，不需要 duration 等字段
- token 有效期 2 小时，超时需要重新获取

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 230055 | file_type 和 msg_type 不匹配 | 上传用 opus，发送用 audio |
| 234001 | file_type 参数错误 | 确认用 opus，不是 audio/file/mp3 |
| 2200 | content 格式错误 | content 应该是纯 JSON 的 file_key 对象 |

