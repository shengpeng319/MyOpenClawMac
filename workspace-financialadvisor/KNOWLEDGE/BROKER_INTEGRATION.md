# Broker对接与实盘交易

*Emily执行交易的技术配置*

---

## 支持的Broker

| Broker | 市场 | API | 特点 |
|--------|------|-----|------|
| Interactive Brokers | 全球 | IB API | 机构级，全球覆盖 |
| Alpaca | 美股 | REST+WebSocket | 免费数据，API友好 |
| 富途证券 | 港美股 | Open API | 港美股 |
| 老虎证券 | 港美股 | Tiger API | 港美股 |
| Polygon | 美股 | REST+WebSocket | 实时数据+交易 |

---

## 基本下单流程

### 1. 获取实时行情
```python
import yfinance as yf
stock = yf.Ticker("AAPL")
data = stock.history(period="1mo")
```

### 2. 仓位计算
```python
def calculate_position(account_value, risk_per_trade, atr):
    return (account_value * risk_per_trade) / atr
```

### 3. 下单执行
```python
# Alpaca示例
import alpaca_trade_api as alpaca
api = alpaca.REST()
api.submit_order(symbol='AAPL', qty=100, side='buy', type='market')
```

---

## 订单类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| Market | 市价单 | 快速成交 |
| Limit | 限价单 | 指定价格 |
| Stop | 止损单 | 自动止损 |
| Trailing Stop | 追踪止损 | 锁定利润 |

---

## ⚠️ 重要提醒

1. **模拟盘优先**: 新策略先用模拟盘测试
2. **小资金开始**: 不要一上来就重仓
3. **记录一切**: 每次交易都要记录决策原因
4. **定期复盘**: 分析亏损交易的原因
