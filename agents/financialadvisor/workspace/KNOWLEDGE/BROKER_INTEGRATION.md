# Broker对接与实盘交易

*Emily执行交易的技术配置*

---

## 支持的Broker

### Interactive Brokers (IB)
- **优势**: 全球市场覆盖，机构级执行
- **API**: IB API (Python)
- **官网**: interactivebrokers.com

### Alpaca
- **优势**: 美股，API友好，免费数据
- **API**: REST API + WebSocket
- **官网**: alpaca.markets
- **注意**: 只能做多，没有融资融券

### 富途证券
- **优势**: 港美股，界面友好
- **API**: Open API
- **官网**: futu.com

### 老虎证券
- **优势**: 港美股
- **API**: Tiger API
- **官网**: tigerbrokers.com

### Polygon
- **优势**: 实时数据+交易，API设计好
- **API**: REST + WebSocket
- **官网**: polygon.io

---

## 基本下单流程

### 1. 获取实时行情
```python
import yfinance as yf

# 获取股票数据
stock = yf.Ticker("AAPL")
data = stock.history(period="1mo")
```

### 2. 信号生成
```python
# 示例：简单MACD信号
def get_macd_signal(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    return macd > signal_line  # True=买入信号
```

### 3. 仓位计算
```python
def calculate_position(account_value, risk_per_trade, atr):
    """根据ATR和风险容忍计算仓位"""
    return (account_value * risk_per_trade) / atr
```

### 4. 下单执行
```python
# Alpaca示例
import alpaca_trade_api as alpaca

api = alpaca.REST()
api.submit_order(
    symbol='AAPL',
    qty=100,
    side='buy',
    type='market',
    time_in_force='day'
)
```

---

## 订单类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| Market | 市价单 | 快速成交 |
| Limit | 限价单 | 指定价格成交 |
| Stop | 止损单 | 自动止损 |
| Stop-Limit | 止损限价单 | 止损+限价 |
| Trailing Stop | 追踪止损 | 锁定利润 |

---

## 执行注意事项

### 滑点控制
- 大额订单要分批执行
- 使用限价单减少滑点
- 避开流动性低的时段

### 手续费
- 高频交易手续费是最大敌人
- 计算净利润要扣除手续费
- 考虑卖空成本（如果有）

### 风控集成
```python
def place_order_with_risk(symbol, qty, side):
    # 下单前检查
    current_exposure = get_total_exposure()
    if current_exposure > MAX_EXPOSURE:
        return "拒绝: 仓位超限"
    
    # 下单
    order = api.submit_order(symbol=symbol, qty=qty, side=side)
    return order
```

---

## 飞书交易机器人

参考视频分析中up主的方案：
- OpenClaw定时任务触发
- Hermes作为交易纪律总监
- 飞书接收下单指令

### 关键配置
- QMT: 量化交易平台（用于下单执行）
- gson文件: 每日行情数据存储格式
- Opt函数: 参数优化工具

---

## ⚠️ 重要提醒

1. **模拟盘优先**: 新策略先用模拟盘测试
2. **小资金开始**: 不要一上来就重仓
3. **记录一切**: 每次交易都要记录决策原因
4. **定期复盘**: 分析亏损交易的原因

---

## 相关页面

- [[QUANT_TOOLCHAIN]] — 量化工具链
- [[RISK_MANAGEMENT]] — 风险管理
