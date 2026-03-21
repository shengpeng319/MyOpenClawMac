# 股票跌破阈值告警 - 技术实现方案

*Created: 2026-03-21*

---

## 方案一：OpenClaw Cron 轮询（最简单）

### 架构
```
OpenClaw Cron (每5分钟) → Python脚本 → Feishu告警
```

### 代码
```python
import yfinance as yf
import requests

STOCK = "NVDA"
THRESHOLD = 120.0
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK"

ticker = yf.Ticker(STOCK)
price = ticker.fast_info.last_price

if price < THRESHOLD:
    message = f"🚨 {STOCK} 当前价 ${price:.2f}，跌破阈值 ${THRESHOLD}！"
    requests.post(WEBHOOK_URL, json={"msg_type": "text", "content": {"text": message}})
```

### 配置 Cron
```bash
openclaw cron add --name "NVDA跌破告警" --cron "*/5 * * * *" --message "python3 ~/scripts/stock_alert.py"
```

---

## 方案二：后台守护进程（推荐，最实用）

### 架构
```
macOS launchd (系统级常驻) → stock_monitor.py → Feishu告警
                   ↓
            每60秒轮询检查
```

### 完整代码
```python
#!/usr/bin/env python3
import yfinance as yf
import requests
import time
import json
from datetime import datetime

FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR-WEBHOOK-ID"
STOCKS = [
    {"symbol": "NVDA", "threshold": 120.0, "name": "英伟达"},
    {"symbol": "TSLA", "threshold": 180.0, "name": "特斯拉"},
]

def get_price(symbol):
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info.last_price
    prev_close = ticker.fast_info.previous_close
    return {"price": price, "change": ((price - prev_close) / prev_close) * 100}

def send_alert(stock, data):
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "🚨 股价告警"}, "template": "red"},
            "elements": [{"tag": "div", "content": {"tag": "lark_md", "content": f"🚨 {stock['name']} 跌破阈值！"}}]
        }
    }
    requests.post(FEISHU_WEBHOOK, json=payload)

while True:
    for stock in STOCKS:
        data = get_price(stock["symbol"])
        if data["price"] < stock["threshold"]:
            send_alert(stock, data)
    time.sleep(60)  # 每60秒检查一次
```

### launchd 服务配置
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>Label</key><string>ai.openclaw.stock-monitor</string>
    <key>ProgramArguments</key>
    <array><string>/usr/bin/python3</string><string>/Users/shengpeng319/scripts/stock_monitor.py</string></array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>StandardOutPath</key><string>/Users/shengpeng319/scripts/stock_monitor.log</string>
</dict>
</plist>
```

### 部署命令
```bash
# 创建 LaunchAgent
ln -sf ~/Library/LaunchAgents/ai.openclaw.stock-monitor.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/ai.openclaw.stock-monitor.plist

# 查看状态
launchctl list | grep stock-monitor
```

---

## 方案对比

| 维度 | Cron轮询 | 守护进程 |
|------|---------|---------|
| 实时性 | ⭐⭐ 1分钟级 | ⭐⭐⭐ 秒级可控 |
| 可靠性 | ⭐⭐ Gateway挂了就没 | ⭐⭐⭐ 系统级保活 |
| 复杂度 | ⭐⭐⭐ 简单 | ⭐⭐ 中等 |
| 资源占用 | ⭐⭐⭐ 低 | ⭐⭐ 持续 |

---

## 推荐架构：混合方案

```
系统层 launchd (主监控，60秒) + OpenClaw Cron (兜底，5分钟)
```

---

## 数据来源

- **Yahoo Finance (yfinance)**: 免费，无需 API Key
- **Alpaca**: WebSocket 实时行情（需注册）
- **经纪商 API**: 富途/老虎证券（需账户）

---

## 注意事项

1. Yahoo Finance 有速率限制，避免秒级轮询
2. 美股非交易时间数据可能延迟
3. 建议配合券商条件单使用，不要纯依赖告警
