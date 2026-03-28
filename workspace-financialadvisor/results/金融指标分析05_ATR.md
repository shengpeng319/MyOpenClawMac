# 金融指标分析系列课程

## 📙 第五课：真实波动幅度与止损——ATR

*Emily 老师出品 | 2026-03-28 | v1.1（Diana P1 修复版）*

---

## 🎯 学习目标

学完这课后，你能：
- ✅ 理解 ATR（Average True Range）的概念——为什么只看价格变化是不够的
- ✅ 掌握 ATR 的计算方法，特别是真实波幅（True Range）的三种情况
- ✅ 用 Python 计算并使用 ATR
- ✅ 理解 ATR 作为"波动性体温计"的作用
- ✅ 用 ATR 设置止损——不只是固定百分比止损
- ✅ 用 ATR 进行仓位管理——根据波动率调整持仓
- ✅ 结合 ATR + 布林带进行动态止盈止损

---

## 🌅 开篇：为什么你需要 ATR？

想象你在开车。

你知道车子每小时开 100 公里——但这告诉你路况了吗？没有。

一条泥泞的山路和一条高速路，都是 100 公里/小时，但**风险完全不同**。

**股票市场也是一样。**

你知道某股票价格是 $100——但这告诉你它的波动有多大了吗？没有。

$100 的股票可能每天波动 $1（1%），也可能每天波动 $10（10%）。

> 💡 **生活中的类比——波动性体温计：** 想象你用体温计量体温。37°C 是正常，38°C 是低烧，39°C 是高烧。ATR 就是股票的"体温计"——告诉你当前波动是"正常"还是"发烧"了。如果某股票的 ATR 突然从 $2 飙升到 $8，说明它的"体温"急剧升高，市场在剧烈波动。如果你用**固定止损**（比如 -5%），在低波动股票上可能过于保守，在高波动股票上可能过于激进。

**ATR 就是解决这个问题的。**

ATR 告诉你：这只股票每天平均波动多少钱？然后你根据这个"波动幅度"来设置止损和仓位，而不是用一个固定的百分比。

> 💡 **生活中的类比：** 想象你在赌博。你有两种游戏：
> - 游戏 A：每天赢 $10 或输 $10
> - 游戏 B：每天赢 $100 或输 $100
> 
> 如果你用"亏光就离场"的策略，游戏 A 和游戏 B 的止损点完全不同。ATR 就是帮你计算这个"每天可能亏多少"的工具。

---

## 📊 什么是 ATR？

### ATR 的全称

**ATR = Average True Range**，即"平均真实波幅"。

- **True Range（真实波幅）**：今天的价格波动范围，考虑了跳空
- **Average**：对一段时间的 TR 取平均

### 为什么 ATR 很重要？

| 指标 | 告诉你什么 | 不告诉你什么 |
|------|-----------|------------|
| **价格** | 股票值多少钱 | 波动有多大 |
| **RSI** | 是否超买超卖 | 波动幅度 |
| **ATR** | 每天平均波动多少钱 | 趋势方向 |

### ATR 的核心用途

1. **止损设置**：根据波动率动态调整止损
2. **仓位管理**：波动大的股票少买，波动小的股票可以多买
3. **突破确认**：ATR 放大可能意味着趋势启动

---

## 🔢 计算方法

### 第一步：计算真实波幅（True Range）

True Range 有三种情况，取最大值：

```
TR = max(今日高点 - 今日低点, |今日高点 - 昨日收盘|, |今日低点 - 昨日收盘|)
```

| 情况 | 条件 | True Range |
|------|------|-----------|
| 情况 1 | 今日无跳空 | 今日高点 - 今日低点 |
| 情况 2 | 今日高开 | 今日高点 - 昨日收盘 |
| 情况 3 | 今日低开 | 今日收盘 - 今日低点 |

> 💡 **为什么考虑跳空？**
> 如果一只股票昨天收盘 $100，今天开盘直接跳空到 $110（利好消息），那么今天的高点和低点可能都在 $110-$115 之间。
> 
> 用"今日高点-今日低点"=$5 会错过跳空的影响。
> 
> 用"|今日高点-昨日收盘"|=$10 才能反映今天真实的波动。

**手算示例：**

假设：
- 昨日收盘 = $100
- 今日开盘 = $98（低开）
- 今日高点 = $102
- 今日低点 = $97

```
情况1：今日高点 - 今日低点 = $102 - $97 = $5
情况2：|今日高点 - 昨日收盘| = |$102 - $100| = $2
情况3：|今日低点 - 昨日收盘| = |$97 - $100| = $3

TR = max($5, $2, $3) = $5
```

### 第二步：计算 ATR（平均真实波幅）

```
ATR = TR 的 14 日指数移动平均（默认参数）
```

> ⚠️ **前置知识提醒——EMA vs SMA：** ATR 用的是 EMA（指数移动平均），不是 SMA。两者区别：
> - **SMA（简单移动平均）**：所有历史数据权重相同
> - **EMA（指数移动平均）**：近期数据权重更大
> 
> 举例：10 日 EMA 比 10 日 SMA 对近期价格变化更敏感。ATR 需要快速反映波动变化，所以用 EMA。

**为什么用 14 作为默认参数？**
- Welles Wilder 在 1978 年测试了多种参数，发现 14 日效果最好
- 这是**经验值**，没有数学证明
- 你可以根据股票特性调整（高波动股票用 7 日，低波动股票用 21 日）

### Python 代码

```python
import yfinance as yf
import pandas as pd
import numpy as np

# 获取数据
stock = yf.Ticker('AAPL')
hist = stock.history(period='3mo')

# 计算 True Range
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))  # High - Previous Close
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))   # Low - Previous Close
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)

# 计算 ATR（14日 EMA）
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

# 查看结果
print(hist[['Close', 'H-L', 'H-PC', 'L-PC', 'TR', 'ATR']].tail(10))
```

---

## 📈 ATR 的核心应用

### 应用 1：动态止损——不止损固定百分比

**固定百分比止损的问题：**
- $100 的股票，跌 5% 止损 = $95
- $10 的股票，跌 5% 止损 = $9.50
- 但 $100 的股票可能每天波动 $3（3%），$10 的股票可能每天波动 $0.5（5%）

如果用 ATR 止损：
```
止损位 = 入场价 - 1.5 × ATR
```

| 股票 | 入场价 | ATR(14) | 1.5×ATR | 止损位 | 止损% |
|------|--------|---------|---------|--------|-------|
| AAPL ($100) | $100 | $2.50 | $3.75 | $96.25 | -3.75% |
| NVDA ($400) | $400 | $15.00 | $22.50 | $377.50 | -5.6% |
| TSLA ($250) | $250 | $12.00 | $18.00 | $232.00 | -7.2% |

> 💡 **为什么这样设计？**
> - 如果 ATR = $2.5，说明这只股票每天平均波动 $2.5
> - 1.5×ATR = $3.75，给了 1.5 天的"呼吸空间"
> - 如果股票跌破 $96.25，说明波动超过了正常范围，可能趋势变了

### 应用 2：仓位管理——根据波动率调整持仓

**核心思想：** 同样的钱，波动大的股票少买，波动小的股票可以多买。

```
仓位 = 风险金额 / (2 × ATR)
```

其中"风险金额"是你愿意在一只股票上亏损的最大金额。

**示例：**
- 你每只股票最多亏 $1000
- AAPL ATR = $2.50 → 仓位 = $1000 / (2 × $2.50) = 200 股
- NVDA ATR = $15.00 → 仓位 = $1000 / (2 × $15) = 33 股

| 股票 | ATR | 2×ATR | 仓位（$1000风险）| 持仓市值 | 风险% |
|------|-----|-------|-----------------|---------|-------|
| AAPL ($100) | $2.50 | $5.00 | 200 股 | $20,000 | 5% |
| NVDA ($400) | $15.00 | $30.00 | 33 股 | $13,200 | 7.6% |

> ⚠️ **注意：** 这里的"风险%"是指如果触发止损，会亏多少钱。不是简单的持仓市值百分比。

### 应用 3：ATR 突破策略——识别趋势启动

**核心思想：** 当 ATR 突然放大，可能是趋势启动的信号。

**传统做法：** 价格突破阻力位就买
**ATR 做法：** 价格突破阻力位 + ATR 放大 = 趋势可能启动

```python
# 计算 ATR
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

# ATR 突破信号：ATR 创 20 天新高
hist['ATR_breakout'] = hist['ATR'] > hist['ATR'].rolling(20).max()

# 价格突破阻力位
hist['Price_breakout'] = hist['Close'] > hist['Close'].rolling(20).max()

# 双重确认：价格突破 + ATR 放大
hist['Signal'] = hist['Price_breakout'] & hist['ATR_breakout']

print("ATR 突破信号：")
print(hist[hist['Signal']][['Close', 'ATR', 'ATR_breakout', 'Price_breakout']])
```

---

## 🖥️ 实战应用

### 案例 1：完整 ATR 分析代码

```python
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取 NVDA 数据（高波动股票，ATR 经典案例）
nvda = yf.Ticker('NVDA')
hist = nvda.history(period='6mo')

# 计算 True Range
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)

# 计算 ATR
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

# 绘制
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# 上图：股价
ax1.plot(hist.index, hist['Close'], label='NVDA 收盘价', color='black')
ax1.set_title('NVDA 股价与 ATR 分析', fontsize=16)
ax1.set_ylabel('价格 (USD)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 下图：ATR
ax2.plot(hist.index, hist['ATR'], label='ATR (14日)', color='blue')
ax2.fill_between(hist.index, 0, hist['ATR'], alpha=0.3, color='blue')
ax2.set_ylabel('ATR')
ax2.set_title('NVDA 平均真实波幅 (ATR)', fontsize=16)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 打印最新状态
print(f"\nNVDA 当前状态：")
print(f"收盘价: ${hist['Close'].iloc[-1]:.2f}")
print(f"ATR(14): ${hist['ATR'].iloc[-1]:.2f}")
print(f"ATR 占价格比例: {hist['ATR'].iloc[-1]/hist['Close'].iloc[-1]*100:.2f}%")
```

**📊 案例结果解读：**
- ATR 越高，股票波动越大
- ATR 占价格比例（ATR%）可以标准化比较不同价格的股票
- NVDA 作为高波动股票，ATR 通常在 $10-$20 之间

---

### 案例 2：用 ATR 设置止损

```python
# 获取数据
stock = yf.Ticker('AAPL')
hist = stock.history(period='3mo')

# 计算 ATR
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

# 假设你在最近的低点买入
entry_price = hist['Close'].iloc[-20]  # 20天前的价格作为入场价
atr = hist['ATR'].iloc[-20]  # 入场时的 ATR

# ATR 止损（1.5 倍 ATR）
stop_loss = entry_price - 1.5 * atr

# 固定百分比止损（5%）
stop_loss_pct = entry_price * 0.95

print(f"入场价: ${entry_price:.2f}")
print(f"ATR(入场时): ${atr:.2f}")
print(f"ATR 止损位 (1.5×ATR): ${stop_loss:.2f} ({-1.5*atr/entry_price*100:.2f}%)")
print(f"固定止损位 (5%): ${stop_loss_pct:.2f} (-5.00%)")
print(f"\n差异: ${abs(stop_loss - stop_loss_pct):.2f}")
```

**📊 案例结果解读：**
- ATR 止损比固定百分比更"聪明"——波动大的股票止损更宽
- 1.5×ATR 给了一天半的"呼吸空间"
- 如果你想更保守，可以用 2×ATR

---

### 案例 3：ATR 仓位管理

```python
# 仓位管理计算
def calculate_position_size(entry_price, atr, risk_amount=1000, atr_multiplier=2):
    """
    根据 ATR 计算仓位
    
    entry_price: 入场价
    atr: 当前 ATR
    risk_amount: 愿意亏损的最大金额
    atr_multiplier: ATR 倍数（默认 2）
    
    返回：建议仓位（股数）
    """
    risk_per_share = atr_multiplier * atr
    shares = risk_amount / risk_per_share
    return int(shares)  # 取整

# 示例
stock = yf.Ticker('AAPL')
hist = stock.history(period='1mo')
current_price = hist['Close'].iloc[-1]

# 计算 ATR
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()
atr = hist['ATR'].iloc[-1]

# 计算不同风险金额下的仓位
risk_amounts = [500, 1000, 2000]
print(f"AAPL 当前价: ${current_price:.2f}")
print(f"AAPL ATR(14): ${atr:.2f}")
print(f"\n=== 仓位管理建议 ===")
for risk in risk_amounts:
    shares = calculate_position_size(current_price, atr, risk)
    position_value = shares * current_price
    actual_risk = shares * 2 * atr
    print(f"风险金额: ${risk} → 买入 {shares} 股 | 市值: ${position_value:.2f} | 实际风险: ${actual_risk:.2f}")
```

**📊 案例结果解读：**
- 同样的 $1000 风险，ATR 低的股票可以买更多股
- 实际风险 ≈ 2 × ATR × 股数（因为止损是 2×ATR）
- ATR 仓位管理让你的风险在每只股票上差不多

---

### 案例 4：ATR + 布林带——动态止盈止损

```python
# 获取数据
stock = yf.Ticker('TSLA')
hist = stock.history(period='6mo')

# 计算布林带
hist['SMA20'] = hist['Close'].rolling(window=20).mean()
hist['STD20'] = hist['Close'].rolling(window=20).std()
hist['UB'] = hist['SMA20'] + 2 * hist['STD20']
hist['LB'] = hist['SMA20'] - 2 * hist['STD20']

# 计算 ATR
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

# ATR 动态止损
hist['ATR_Stop'] = hist['Close'] - 2 * hist['ATR']

# 布林带下轨止损
hist['BB_Stop'] = hist['LB']

# 两者取较保守的（离入场更远的）
hist['Stop'] = hist[['ATR_Stop', 'BB_Stop']].max(axis=1)

# 打印最新状态
print(f"TSLA 当前价: ${hist['Close'].iloc[-1]:.2f}")
print(f"布林带下轨: ${hist['LB'].iloc[-1]:.2f}")
print(f"ATR 止损: ${hist['ATR_Stop'].iloc[-1]:.2f}")
print(f"综合止损（两者取高）: ${hist['Stop'].iloc[-1]:.2f}")
```

**📊 案例结果解读：**
- 布林带下轨是静态的支撑位
- ATR 止损是动态的，根据波动率调整
- 两者取较高者 = 更保守的止损
- 如果布林带下轨在 ATR 止损上方，用布林带止损；否则用 ATR 止损

**📊 追踪止盈机制（Trailing Stop）：**
- 追踪止盈是一种"移动止损"——当价格上涨时，止损位也跟着上移
- 公式：**追踪止盈位 = 当前价格 - 2 × ATR**
- 如果价格从 $200 涨到 $220，ATR = $5，则追踪止盈位 = $220 - $10 = $210
- 即使价格后来回调，只要不跌破 $210，就继续持有
- 这样可以"让利润奔跑，同时锁定部分收益"

---

## ⚠️ ATR 的局限性

### ❌ ATR 不能预测方向

ATR 只告诉你波动有多大，不告诉你价格往哪个方向走。

**✅ 正确做法：** 用 MACD 或均线判断方向，用 ATR 设置止损。

---

### ❌ ATR 止损可能过宽

对于低波动股票，ATR 很小，止损可能只离入场价 1-2%。但市场噪音可能导致频繁止损。

**✅ 正确做法：** 结合市场环境。如果在震荡市中，ATR 本身就小，可以适当放大 ATR 倍数（如用 2.5×ATR 而不是 1.5×ATR）。

---

### ❌ ATR 不适合短线交易

ATR 是为**日线级别**设计的指标。对于分钟线交易，ATR 变化太快。

**✅ 正确做法：** 
| 交易周期 | 建议 ATR 参数 |
|---------|--------------|
| 日线 | 14 日 ATR（默认）|
| 日内波段 | 5-7 日 ATR |
| 超短线 | 不建议使用 ATR |

---

## 📋 ATR 信号速查表

| 应用场景 | 公式/方法 | 说明 |
|---------|----------|------|
| **止损** | 入场价 - 1.5×ATR | 保守 |
| **止损（激进）** | 入场价 - 2×ATR | 常见用法 |
| **仓位管理** | 风险金额 / (2×ATR) | 每只股票等风险 |
| **ATR 突破** | ATR > 20日ATR最高 | 可能趋势启动 |
| **波动率比较** | ATR / 价格 = ATR% | 标准化比较 |

---

## 🧠 思考题

### 思考题 1 ✅ 含参考答案

**题目：**
某股票：
- 入场价 = $200
- ATR(14) = $8

请计算：
1. 1.5×ATR 止损位在哪里？亏损%是多少？
2. 如果改用 2×ATR 止损呢？

**参考答案：**
1. 1.5×ATR = 1.5 × $8 = $12
   止损位 = $200 - $12 = $188
   亏损% = $12 / $200 = 6%

2. 2×ATR = 2 × $8 = $16
   止损位 = $200 - $16 = $184
   亏损% = $16 / $200 = 8%

---

### 思考题 2 ✅ 含参考答案

**题目：**
你有 $10,000 想投资两只股票：
- 股票 A：价格 $50，ATR = $2
- 股票 B：价格 $200，ATR = $10

如果每只股票最多亏损 $500，用 ATR 仓位管理，各买多少股？

**参考答案：**
仓位 = $500 / (2 × ATR)

股票 A：$500 / (2 × $2) = 125 股（市值 $6,250）
股票 B：$500 / (2 × $10) = 25 股（市值 $5,000）

注意：虽然股票 A 价格更低，但因为波动更大，实际持仓市值差不多。这正是 ATR 仓位管理的核心思想——**等风险，不等股数，不等市值**。

---

### 思考题 3 ✅ 含参考答案

**题目：**
"MACD 金叉 + ATR 放大" 是否是更强的买入信号？为什么？

**参考答案：**
1. **是的**，MACD 金叉说明短期动量转正（趋势向上）
2. ATR 放大说明波动增加，可能有趋势启动
3. 两者结合 = **方向确认 + 波动确认**，比单一信号更可靠
4. 但要注意：ATR 放大也可能是假突破，需要结合成交量验证

---

## 📝 练习题

### 练习 1（入门）：计算 ATR ✅ 含验收标准

请用 yfinance 获取任意股票数据，计算并绘制 ATR。

**验收标准：** 运行代码后，你应该能看到：
1. 上图：股价走势
2. 下图：ATR 曲线（带填充区域）
3. 打印当前 ATR 值和 ATR 占价格百分比
4. ATR 创 20 日新高的标注（如有）

```python
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===== 验收标准检查 =====
# 运行后检查以下几点：
# 1. ✅ 上图：股价走势
# 2. ✅ 下图：ATR 曲线（带填充区域）
# 3. ✅ 打印当前 ATR 值和 ATR 占价格百分比
# 4. ✅ ATR 创 20 日新高的标注（如有）
# =========================

# 换成你想看的股票
ticker = 'TSLA'

stock = yf.Ticker(ticker)
hist = stock.history(period='6mo')

# 计算 True Range
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)

# 计算 ATR
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

# ATR 突破（20日新高）
hist['ATR_high'] = hist['ATR'].rolling(20).max()
hist['ATR_breakout'] = hist['ATR'] == hist['ATR_high']

# 绘制
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# 上图：股价
ax1.plot(hist.index, hist['Close'], label=f'{ticker} 收盘价', color='black')
ax1.set_title(f'{ticker} 股价', fontsize=16)
ax1.set_ylabel('价格 (USD)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 下图：ATR
ax2.plot(hist.index, hist['ATR'], label='ATR (14日)', color='blue')
ax2.fill_between(hist.index, 0, hist['ATR'], alpha=0.3, color='blue')
ax2.scatter(hist.loc[hist['ATR_breakout']].index, hist.loc[hist['ATR_breakout'], 'ATR'],
           marker='^', color='red', s=100, label='ATR 20日新高')
ax2.set_title(f'{ticker} ATR (平均真实波幅)', fontsize=16)
ax2.set_ylabel('ATR')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 打印验收结果
print("\n=== 验收结果 ===")
current_atr = hist['ATR'].iloc[-1]
current_price = hist['Close'].iloc[-1]
atr_pct = current_atr / current_price * 100
print(f"{ticker} 当前 ATR(14): ${current_atr:.2f}")
print(f"{ticker} 当前价格: ${current_price:.2f}")
print(f"ATR 占价格比例: {atr_pct:.2f}%")
print(f"ATR 20日新高次数: {hist['ATR_breakout'].sum()}")
print("\n✅ 验收标准 1-4 全部通过则练习完成！")
```

---

### 练习 2（进阶）：ATR 止损止盈 ✅ 含验收标准

假设你在 20 天前的收盘价买入，计算 ATR 止损位，并比较 1.5×ATR 和 2×ATR 的差异。

**验收标准：** 运行代码后，你应该能看到：
1. 20 天前的买入点和当前价格
2. 1.5×ATR 和 2×ATR 两个止损位
3. 如果价格上涨，动态调整止盈位（入场价 + 2×ATR）
4. 打印出止损和止盈的具体价格

```python
# ===== 验收标准检查 =====
# 运行后检查以下几点：
# 1. ✅ 20天前的买入点和当前价格
# 2. ✅ 1.5×ATR 和 2×ATR 两个止损位
# 3. ✅ 如果价格上涨，动态调整止盈位（入场价 + 2×ATR）
# 4. ✅ 打印出止损和止盈的具体价格
# =========================

# 计算 ATR
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

# 假设 20 天前买入
entry_idx = -20
entry_price = hist['Close'].iloc[entry_idx]
entry_atr = hist['ATR'].iloc[entry_idx]
current_price = hist['Close'].iloc[-1]

# 止损位
stop_loss_15 = entry_price - 1.5 * entry_atr
stop_loss_20 = entry_price - 2 * entry_atr

# 止盈位（入场价 + 2×ATR，动态跟踪）
take_profit = entry_price + 2 * entry_atr

print("\n=== ATR 止损止盈分析 ===")
print(f"买入日期: {hist.index[entry_idx].date()}")
print(f"买入价格: ${entry_price:.2f}")
print(f"入场时 ATR: ${entry_atr:.2f}")
print(f"当前价格: ${current_price:.2f}")
print(f"当前盈亏: {((current_price/entry_price)-1)*100:+.2f}%")
print(f"\n--- 止损位 ---")
print(f"1.5×ATR 止损: ${stop_loss_15:.2f} ({((stop_loss_15/entry_price)-1)*100:.2f}%)")
print(f"2×ATR 止损: ${stop_loss_20:.2f} ({((stop_loss_20/entry_price)-1)*100:.2f}%)")
print(f"\n--- 止盈位 ---")
print(f"2×ATR 止盈: ${take_profit:.2f} ({((take_profit/entry_price)-1)*100:+.2f}%)")

# 如果价格上涨，动态调整止盈
if current_price > entry_price:
    current_atr = hist['ATR'].iloc[-1]
    trailing_stop = current_price - 2 * current_atr
    print(f"\n--- 动态止盈（价格已上涨）---")
    print(f"当前 ATR: ${current_atr:.2f}")
    print(f"追踪止盈位: ${trailing_stop:.2f}")

print("\n✅ 验收标准 1-4 全部通过则练习完成！")
```

---

### 练习 3（挑战）：ATR 仓位管理 + 风险计算

用 ATR 仓位管理公式，计算在不同风险承受能力下，你应该买多少股，并验证实际风险。

**验收标准：** 运行代码后，你应该能看到：
1. 不同风险金额（$500, $1000, $2000）下的建议股数
2. 每个仓位对应的持仓市值
3. 验证实际风险是否接近目标风险

```python
# 仓位管理计算
def calculate_position_size(entry_price, atr, risk_amount=1000, atr_multiplier=2):
    """
    根据 ATR 计算仓位
    
    entry_price: 入场价
    atr: 当前 ATR
    risk_amount: 愿意亏损的最大金额
    atr_multiplier: ATR 倍数（默认 2）
    
    返回：建议仓位（股数）
    """
    risk_per_share = atr_multiplier * atr
    shares = risk_amount / risk_per_share
    return int(shares)

# 计算 ATR
hist['H-L'] = hist['High'] - hist['Low']
hist['H-PC'] = abs(hist['High'] - hist['Close'].shift(1))
hist['L-PC'] = abs(hist['Low'] - hist['Close'].shift(1))
hist['TR'] = hist[['H-L', 'H-PC', 'L-PC']].max(axis=1)
hist['ATR'] = hist['TR'].ewm(alpha=1/14, min_periods=14).mean()

current_price = hist['Close'].iloc[-1]
atr = hist['ATR'].iloc[-1]

print(f"\n=== ATR 仓位管理 ===")
print(f"{ticker} 当前价格: ${current_price:.2f}")
print(f"{ticker} ATR(14): ${atr:.2f}")

# 不同风险金额
risk_amounts = [500, 1000, 2000]
print(f"\n--- 仓位管理建议 ---")
for risk in risk_amounts:
    shares = calculate_position_size(current_price, atr, risk)
    position_value = shares * current_price
    actual_risk = shares * 2 * atr
    actual_risk_pct = actual_risk / position_value * 100
    print(f"风险金额: ${risk} → 买入 {shares} 股 | 市值: ${position_value:.2f} | 实际风险: ${actual_risk:.2f} ({actual_risk_pct:.1f}% 持仓)")
```

---

## 📋 本课小结

### 🎯 核心知识点

| 概念 | 关键点 |
|------|--------|
| **True Range** | max(今日高低差, 今日高-昨日收, 昨日收-今日低) |
| **ATR** | TR 的 14 日 EMA（默认参数）|
| **ATR 止损** | 入场价 - 1.5×ATR（保守）或 - 2×ATR（常用）|
| **ATR 仓位管理** | 仓位 = 风险金额 / (2 × ATR) |
| **ATR 突破** | ATR 创 20 日新高 = 可能趋势启动 |
| **ATR + 布林带** | 动态止盈止损，结合波动率和支撑位 |
| **ATR 局限性** | 不能预测方向，可能过宽，不适合短线 |

### 💡 记住这句话

> **"ATR 不是预测工具，而是风险量化工具。它告诉你每天平均波动多少，让你能根据波动率设置止损和仓位——同样的 $1000 风险，波动大的股票少买，波动小的股票可以多买。"**

### 📚 第六课预告

**第六课：完整技术分析系统——综合运用**

预告内容：
- 如何把学到的指标串起来（MA + RSI + MACD + 布林带 + ATR）
- 趋势判断 → 入场点 → 止损设置 → 仓位管理 → 持仓跟踪
- 完整的交割单案例分析
- 如何建立自己的交易系统

---

## 📎 v1.0 更新说明

| 版本 | 日期 | 改动 |
|------|------|------|
| v1.0 | 2026-03-28 | Emily 初稿 |
| v1.1 | 2026-03-28 | Diana 审核后：开篇添加"波动性体温计"类比；EMA前置知识增加SMA对比说明；案例4增加追踪止盈机制解释 |

---

*本课完 | 金融指标分析系列课程第五课 | Emily 老师*
