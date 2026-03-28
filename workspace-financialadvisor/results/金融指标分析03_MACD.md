# 金融指标分析系列课程

## 📗 第三课：趋势确认与动量捕捉——MACD

*Emily 老师出品 | 2026-03-28 | v1.3（Claire 顶背离代码逻辑修复版）*

---

## 🎯 学习目标

学完这课后，你能：
- ✅ 理解 MACD 的三个组成部分：DIF、DEA、MACD 柱状图
- ✅ 掌握 MACD 的**四步**计算方法，特别是 12/26/9 这三个参数的历史来源
- ✅ 用 Python 计算并绘制 MACD
- ✅ 识别 MACD 金叉死叉信号
- ✅ 识别 MACD 与股价的背离（比 RSI 背离更准确）
- ✅ 理解 MACD 是**滞后指标**（lagging indicator）及其实际影响
- ✅ 组合 RSI + MACD 双重确认交易信号

---

## 🌅 开篇：为什么需要 MACD？

想象你在开车。

- **均线**告诉你：现在在哪个车道行驶（趋势方向）
- **RSI**告诉你：现在是加速还是减速（动量强弱）

但它们都**滞后**——等你看到信号时，最佳时机可能已经过了。

**MACD 就是来解决这个问题的。**

MACD 的全称是"移动平均收敛散度"（Moving Average Convergence Divergence），由 Gerald Appel 在 1970 年代发明。它不仅告诉你趋势方向，还告诉你趋势的**动量**——这股趋势是在加速还是减速？

> 💡 **生活中的类比：** 想象你开车上坡。RSI 告诉你"你现在踩油门很用力"，但 MACD 告诉你"虽然你踩得很用力，但车速其实在变慢"——这就是 MACD 能发现"顶背离"的原因。

---

## 📊 什么是 MACD？

MACD 由三个部分组成：

| 组成部分 | 全称 | 作用 |
|---------|------|------|
| **DIF（快线）** | MACD Line / DIF | 短期（12天）EMA - 长期（26天）EMA，反映短期动量 |
| **DEA（慢线）** | Signal Line | DIF 的 9 天 EMA，平滑处理后产生信号 |
| **MACD 柱（直方图）** | Histogram | DIF - DEA，柱的长短反映动量强弱 |

### 为什么是 12 和 26？

**历史来源：**
- Gerald Appel 通过大量历史数据测试，发现 **12天 EMA - 26天 EMA** 的组合效果最好
- 12天 ≈ 两周（短期）
- 26天 ≈ 一个月（长期）
- 这个组合在 1970 年代被证明有效，至今仍是默认参数

**为什么是 9？**
- DIF 和 DEA 都是均线，所以需要再平滑一次
- **9天 EMA** 是经过大量测试的最优平滑参数
- 这不是精确计算出来的，而是**经验值**

---

## 🔢 计算方法

### MACD 四步计算

> ⚠️ **前置知识提醒：** 如果你对 EMA（指数移动平均线）不熟悉，请先回顾第一课"移动平均线"中的 EMA 部分。MACD 的计算依赖于 EMA 的概念。

**第一步：计算 12 日 EMA 和 26 日 EMA**
```
EMA12 = 最近12天收盘价的指数加权平均
EMA26 = 最近26天收盘价的指数加权平均
```

**第二步：计算 DIF（快线）**
```
DIF = EMA12 - EMA26
```

**第三步：计算 DEA（慢线/信号线）**
```
DEA = DIF 的 9 天 EMA
```

**第四步：计算 MACD 柱**
```
MACD 柱 = DIF - DEA
（有些软件会乘以 2 放大显示，但本质是一样的）
```

### Python 代码

```python
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 获取数据
stock = yf.Ticker('AAPL')
hist = stock.history(period='6mo')

# 计算 EMA
hist['EMA12'] = hist['Close'].ewm(span=12, adjust=False).mean()
hist['EMA26'] = hist['Close'].ewm(span=26, adjust=False).mean()

# 计算 DIF（快线）
hist['DIF'] = hist['EMA12'] - hist['EMA26']

# 计算 DEA（慢线/信号线）
hist['DEA'] = hist['DIF'].ewm(span=9, adjust=False).mean()

# 计算 MACD 柱（注意：有些软件乘以2放大，这里直接用差值）
hist['MACD'] = hist['DIF'] - hist['DEA']

# 查看结果
print(hist[['Close', 'EMA12', 'EMA26', 'DIF', 'DEA', 'MACD']].tail(10))
```

---

## 📈 MACD 的核心用法

### 1️⃣ 金叉与死叉

#### 金叉（买入信号）✅

**现象：** DIF 从下往上穿越 DEA

**为什么是买入信号？**
- DIF > DEA → 短期动量 > 长期动量 → 趋势向上
- 金叉出现意味着动量开始转正

**文字描述：**
```
DIF（快线）：━━━━━↗━━━━━━━━
DEA（慢线）：━━━━━━━↗━━━━━━
             ↑ 金叉点（买入信号）
```

#### 死叉（卖出信号）⚠️

**现象：** DIF 从上往下穿越 DEA

**为什么是卖出信号？**
- DIF < DEA → 短期动量 < 长期动量 → 趋势向下
- 死叉出现意味着动量开始转负

**文字描述：**
```
DEA（慢线）：━━━━━━━↘━━━━━━
DIF（快线）：━━━━━↘━━━━━━━━
             ↑ 死叉点（卖出信号）
```

---

### 2️⃣ 零轴金叉死叉

#### 零轴上方金叉（强势买入）💪

**现象：** DIF 和 DEA 都在零轴上方，DIF 向上穿越 DEA

**为什么强势？**
- 零轴上方 = 12日 EMA > 26日 EMA = 短期价格 > 长期价格 = 上升趋势
- 在上升趋势中的金叉信号更强

---

#### 零轴下方金叉（弱势反弹）⚡

**现象：** DIF 和 DEA 都在零轴下方，DIF 向上穿越 DEA

**为什么弱势？**
- 零轴下方 = 下降趋势
- 此时的买入只是"反弹"，不是"趋势反转"

---

#### 零轴穿越的意义

| 位置 | 信号 | 强度 |
|------|------|------|
| 零轴上方金叉 | 买入 | 强 |
| 零轴上方死叉 | 卖出 | 中 |
| 零轴下方金叉 | 买入 | 弱（反弹）|
| 零轴下方死叉 | 卖出 | 强 |

---

### 3️⃣ MACD 背离——最准确的转势信号

**MACD 背离为什么比 RSI 背离更准确？**

因为 MACD 直接比较的是两条 EMA 的差值，而 EMA 本身就是均线的平滑版本，所以 MACD 的背离信号更可靠。

#### 顶背离（看跌信号）⚠️

**现象：** 股价创 120 天新高，但 DIF/DEA 没同步创新高

**文字描述：**
```
股价：不断创出新高 --------（最高点）
                            ↗ （继续上涨）
DIF： 在这里掉头向下 -----↗ （没能创新高）
```

#### 底背离（看涨信号）✅

**现象：** 股价创 120 天新低，但 DIF/DEA 没同步创新低

**文字描述：**
```
DIF： 在这里掉头向上 -----↘ （没能创新低）
                            ↘ （开始反弹）
股价：不断创出新低 --------（最低点）
```

> ⚠️ **重要说明：** 背离检测使用 120 天（半年）作为历史比较窗口。顶背离判断当前价格是否创 120 天内新高，而非窗口内局部高点。

#### Python 代码：识别 MACD 背离

```python
def find_macd_divergence(hist, lookback=120, threshold=0.5):
    """
    识别 MACD 顶背离和底背离
    
    lookback: 用于判断"创新高/新低"的历史窗口（默认120天=半年）
    threshold: DIF 从高点下降超过 X 才算有效背离
    
    顶背离逻辑：当前价格创 lookback 期新高，但 DIF 没创新高（从高点下降超过阈值）
    底背离逻辑：当前价格创 lookback 期新低，但 DIF 没创新低（从低点上升超过阈值）
    """
    signals = []
    
    for i in range(lookback, len(hist)):
        current_price = hist.iloc[i]['Close']
        current_dif = hist.iloc[i]['DIF']
        
        # 用 lookback 窗口判断是否"创新高/新低"
        lookback_data = hist.iloc[i-lookback:i]
        price_max = lookback_data['Close'].max()
        price_min = lookback_data['Close'].min()
        dif_max = lookback_data['DIF'].max()
        dif_min = lookback_data['DIF'].min()
        
        # 顶背离：价格创 lookback 期新高，但 DIF 从高点下降超过阈值
        # 价格创新高 = 可能见顶；DIF 没跟上 = 动量衰竭
        if current_price == price_max and (dif_max - current_dif) > threshold:
            signals.append({
                'date': hist.index[i],
                'type': '顶背离',
                'price': current_price,
                'dif': current_dif,
                'dif_max': dif_max,
                'note': f'价格创{lookback}天新高但DIF未跟随'
            })
        
        # 底背离：价格创 lookback 期新低，但 DIF 从低点上升超过阈值
        # 价格创新低 = 可能见底；DIF 没跟随创新低 = 动量积累
        if current_price == price_min and (current_dif - dif_min) > threshold:
            signals.append({
                'date': hist.index[i],
                'type': '底背离',
                'price': current_price,
                'dif': current_dif,
                'dif_min': dif_min,
                'note': f'价格创{lookback}天新低但DIF未跟随'
            })
    
    return signals

divergences = find_macd_divergence(hist)
print("=== MACD 背离信号 ===")
for sig in divergences[-10:]:
    print(f"{sig['date'].date()}: {sig['type']} | 价格: {sig['price']:.2f} | DIF: {sig['dif']:.4f} | {sig['note']}")
```

---

## ⚠️ 重要特性：MACD 是滞后指标

**MACD 的滞后性比 RSI 更大：**
- RSI 比较的是价格和14天平均
- MACD 比较的是12天EMA和26天EMA的差值的9天EMA
- **MACD 至少滞后 26 天！**

**滞后性的实际影响：**
- MACD 发出信号时，趋势可能已经走了很久
- MACD 不适合"抄底逃顶"，只适合"趋势确认"
- 结合 RSI 使用可以互补

> 💡 **重要提醒：** 滞后指标的特点是"信号出现时，趋势已经发生了"。MACD 的背离虽然比金叉死叉更准确，但仍然是"确认"信号，不是"预测"信号。

---

## 🖥️ 实战应用

### 案例 1：完整 MACD 分析代码

```python
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取 NVDA 数据（MACD 经典案例）
nvda = yf.Ticker('NVDA')
hist = nvda.history(period='1y')

# 计算 MACD
hist['EMA12'] = hist['Close'].ewm(span=12, adjust=False).mean()
hist['EMA26'] = hist['Close'].ewm(span=26, adjust=False).mean()
hist['DIF'] = hist['EMA12'] - hist['EMA26']
hist['DEA'] = hist['DIF'].ewm(span=9, adjust=False).mean()
hist['MACD'] = hist['DIF'] - hist['DEA']

# 绘制
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# 股价
ax1.plot(hist.index, hist['Close'], label='NVDA 收盘价', color='black')
ax1.set_title('NVDA 股价与 MACD 分析', fontsize=16)
ax1.set_ylabel('价格 (USD)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# MACD（注意：MACD柱用红绿色区分正负）
ax2.plot(hist.index, hist['DIF'], label='DIF（快线）', color='blue')
ax2.plot(hist.index, hist['DEA'], label='DEA（慢线）', color='orange')
colors = ['green' if x >= 0 else 'red' for x in hist['MACD']]
ax2.bar(hist.index, hist['MACD'], label='MACD 柱', color=colors, alpha=0.5)
ax2.axhline(y=0, color='gray', linestyle='--')
ax2.set_ylabel('MACD')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 打印最新状态
print(f"NVDA 当前状态：")
print(f"收盘价: ${hist['Close'].iloc[-1]:.2f}")
print(f"DIF: {hist['DIF'].iloc[-1]:.4f}")
print(f"DEA: {hist['DEA'].iloc[-1]:.4f}")
print(f"MACD: {hist['MACD'].iloc[-1]:.4f}")
```

**📊 案例结果解读：**
运行后你会看到：
- 上图是股价，下图是 MACD
- DIF > DEA 时，MACD 柱在零轴上方（绿色）
- DIF < DEA 时，MACD 柱在零轴下方（红色）
- 金叉/死叉点是 DIF 穿越 DEA 的时刻

---

### 案例 2：MACD + RSI 组合策略

**为什么这个组合有效？**
- RSI 判断超买超卖（时机）
- MACD 确认趋势方向（方向）
- 两者结合 = 时机 + 方向 = 提高胜率

**策略逻辑：**
- 只在 MACD 多头时买入（DIF > DEA 且都在零轴上方）
- RSI < 30 时买入（抄底）
- RSI > 70 时卖出（逃顶）

```python
# ========== RSI 计算函数 ==========
def calculate_rsi(prices, period=14):
    """
    计算 RSI（Wilder's 平滑法）
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Wilder's 平滑
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    
    # 处理极端情况
    rs = avg_gain / avg_loss
    rs = rs.replace([np.inf, -np.inf], 0)
    
    rsi = 100 - (100 / (1 + rs))
    return rsi
# ========== RSI 计算函数结束 ==========

# 计算 MACD
hist['EMA12'] = hist['Close'].ewm(span=12, adjust=False).mean()
hist['EMA26'] = hist['Close'].ewm(span=26, adjust=False).mean()
hist['DIF'] = hist['EMA12'] - hist['EMA26']
hist['DEA'] = hist['DIF'].ewm(span=9, adjust=False).mean()
hist['MACD'] = hist['DIF'] - hist['DEA']

# 计算 RSI
hist['RSI'] = calculate_rsi(hist['Close'])

# 买入信号：MACD 多头 + RSI 超卖
hist['BuySignal'] = (hist['DIF'] > hist['DEA']) & (hist['DEA'] > 0) & (hist['RSI'] < 30)

# 卖出信号：MACD 空头 + RSI 超买
hist['SellSignal'] = (hist['DIF'] < hist['DEA']) & (hist['DEA'] < 0) & (hist['RSI'] > 70)

# 查看信号
buy_dates = hist[hist['BuySignal']].index
sell_dates = hist[hist['SellSignal']].index

print(f"MACD+RSI 买入信号数量: {len(buy_dates)}")
print(f"MACD+RSI 卖出信号数量: {len(sell_dates)}")
```

**📊 案例结果解读：**
- MACD 多头 + RSI 超卖 = 顺势抄底（最佳买点）
- MACD 空头 + RSI 超买 = 逆势止盈（最佳卖点）
- 信号很少但很精准，适合长线投资者

---

### 案例 3：检测 MACD 背离

```python
# 查找背离信号
divergences = find_macd_divergence(hist)

print("=== MACD 背离信号 ===")
for sig in divergences[-10:]:
    print(f"{sig['date'].date()}: {sig['type']} | 价格: {sig['price']:.2f} | DIF: {sig['dif']:.4f} | {sig['note']}")
```

**📊 案例结果解读：**
- 顶背离出现后，股价通常会回调
- 底背离出现后，股价通常会反弹
- MACD 背离比 RSI 背离更可靠，但信号更少

---

## ⚠️ 常见误区

### ❌ 误区 1：MACD 金叉就买，死叉就卖

**为什么不对？**
- 在震荡行情中，MACD 会反复金叉死叉，导致频繁交易亏损
- 零轴下方的金叉是弱势反弹，不是趋势反转

**✅ 正确做法：**
- 只在零轴上方金叉时买入（确认是上升趋势）
- 结合 RSI 超卖信号过滤假信号

---

### ❌ 误区 2：MACD 可以预测顶和底

**为什么不对？**
- MACD 是**滞后指标**（lagging indicator）
- 背离出现时，最佳买卖点已经过去了
- MACD 帮你确认趋势，不是预测趋势

**✅ 正确做法：**
- 用 MACD 确认已有趋势
- 不要试图用 MACD 抄底逃顶

---

### ❌ 误区 3：MACD 参数不需要调整

**为什么不对？**
- 默认参数 12/26/9 是 1970 年代设定的
- 不同股票需要不同参数

**✅ 正确做法：**
| 股票类型 | 建议 MACD 参数 | 来源 |
|---------|--------------|------|
| 高波动成长股 | 8/17/9 或 5/35/5 | 社区经验，非权威建议 |
| 普通股票 | 12/26/9（默认）| Gerald Appel 经典参数 |
| 低波动蓝筹股 | 19/39/9 | 社区经验，非权威建议 |

> ⚠️ **重要提醒：** 以上参数修改建议来自社区经验，没有统一的权威文献支持。不同参数适用于不同交易风格，选择时需要根据自己的实测结果和风险承受能力来决定。

---

### ❌ 误区 4：只看 MACD 柱，不看 DIF 和 DEA

**为什么不对？**
- MACD 柱只是 DIF 和 DEA 的差值
- 只有理解 DIF 和 DEA 的关系，才能真正理解 MACD

**✅ 正确做法：**
- 先看 DIF 和 DEA 的相对位置
- 再看 MACD 柱的长短变化
- 三者结合才能得出准确判断

---

## 📋 MACD 信号速查表

| 信号类型 | 判断条件 | 信号强度 | 操作建议 |
|---------|---------|---------|---------|
| **零轴上方金叉** | DIF 从下穿越 DEA，且两者都在零轴上方 | ⭐⭐⭐⭐⭐ 极强 | 买入 |
| **零轴下方金叉** | DIF 从下穿越 DEA，但都在零轴下方 | ⭐⭐ 弱 | 谨慎，可能是反弹 |
| **零轴上方死叉** | DIF 从上穿越 DEA，且两者都在零轴上方 | ⭐⭐⭐ 中 | 减仓 |
| **零轴下方死叉** | DIF 从上穿越 DEA，但都在零轴下方 | ⭐⭐⭐⭐⭐ 极强 | 卖出/做空 |
| **顶背离** | 价格创120天新高，DIF 没创新高 | ⭐⭐⭐⭐ 强 | 警惕回调 |
| **底背离** | 价格创120天新低，DIF 没创新低 | ⭐⭐⭐⭐ 强 | 关注买入机会 |

---

## 🧠 思考题

### 思考题 1：
某股票当前状态：
- EMA12 = $105
- EMA26 = $100
- DIF = $5
- DIF 的 9 日 EMA = $4

请问 DIF 和 DEA 的关系是什么？MACD 柱是正还是负？这代表什么含义？

### 思考题 2：
一只股票在下降趋势中，MACD 出现底背离。你认为这是买入信号吗？为什么？

### 思考题 3：
"MACD 金叉出现在零轴下方，股价一定会反弹"，你同意吗？如果不同意，应该怎么理解这种信号？

---

## 📝 练习题

### 练习 1（入门）：绘制 MACD（✅ 含验收标准）

请用 yfinance 获取你感兴趣的一只股票数据，绘制：
- 股价线
- DIF（快线，蓝色）
- DEA（慢线，橙色）
- MACD 柱（**红绿色区分正负**）

**验收标准：** 运行代码后，你应该能看到：
1. 股价图和 MACD 图上下排列
2. DIF 和 DEA 两条线在 MACD 图中交叉
3. MACD 柱在零轴上下交替出现（**绿色=零轴上方，红色=零轴下方**）
4. 打印出当前 DIF、DEA、MACD 的数值

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
# 1. ✅ 股价图和 MACD 图上下排列
# 2. ✅ DIF（蓝）和 DEA（橙）在 MACD 图中交叉
# 3. ✅ MACD 柱在零轴上方时为绿色，下方时为红色
# 4. ✅ 打印出当前 DIF、DEA、MACD 的数值
# =========================

# 换成你想看的股票
ticker = 'TSLA'

stock = yf.Ticker(ticker)
hist = stock.history(period='6mo')

# 计算 MACD
hist['EMA12'] = hist['Close'].ewm(span=12, adjust=False).mean()
hist['EMA26'] = hist['Close'].ewm(span=26, adjust=False).mean()
hist['DIF'] = hist['EMA12'] - hist['EMA26']
hist['DEA'] = hist['DIF'].ewm(span=9, adjust=False).mean()
hist['MACD'] = hist['DIF'] - hist['DEA']

# 绘制（MACD 柱用红绿色区分正负）
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
ax1.plot(hist.index, hist['Close'])
ax1.set_title(f'{ticker} 股价')
ax2.plot(hist.index, hist['DIF'], label='DIF', color='blue')
ax2.plot(hist.index, hist['DEA'], label='DEA', color='orange')
colors = ['green' if x >= 0 else 'red' for x in hist['MACD']]
ax2.bar(hist.index, hist['MACD'], label='MACD 柱', color=colors, alpha=0.5)
ax2.axhline(y=0, color='gray', linestyle='--')
ax2.set_title(f'{ticker} MACD')
ax2.legend()
plt.show()

# 打印验收结果
print("=== 验收结果 ===")
print(f"{ticker} 当前 DIF: {hist['DIF'].iloc[-1]:.4f}")
print(f"{ticker} 当前 DEA: {hist['DEA'].iloc[-1]:.4f}")
print(f"{ticker} 当前 MACD: {hist['MACD'].iloc[-1]:.4f}")
print("✅ 验收标准 1-4 全部通过则练习完成！")
```

---

### 练习 2（进阶）：MACD + RSI 组合

修改上面的代码，添加 RSI 指标，并用 MACD + RSI 组合策略找出买入信号。

**验收标准：** 运行代码后，你应该能看到：
1. RSI 值在 30 以下时的买入信号日期
2. 买入信号发生时 DIF > DEA 且在零轴上方
3. 最近 5 次买入信号的具体日期和价格

```python
# ===== 验收标准检查 =====
# 运行后检查以下几点：
# 1. ✅ 显示 RSI < 30 的买入信号
# 2. ✅ 确认买入信号满足 DIF > DEA 且 DEA > 0
# 3. ✅ 打印最近 5 次买入信号的日期和价格
# =========================

# 计算 MACD
hist['EMA12'] = hist['Close'].ewm(span=12, adjust=False).mean()
hist['EMA26'] = hist['Close'].ewm(span=26, adjust=False).mean()
hist['DIF'] = hist['EMA12'] - hist['EMA26']
hist['DEA'] = hist['DIF'].ewm(span=9, adjust=False).mean()
hist['MACD'] = hist['DIF'] - hist['DEA']

# ========== RSI 计算函数 ==========
def calculate_rsi(prices, period=14):
    """
    计算 RSI（Wilder's 平滑法）
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Wilder's 平滑
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    
    # 处理极端情况
    rs = avg_gain / avg_loss
    rs = rs.replace([np.inf, -np.inf], 0)
    
    rsi = 100 - (100 / (1 + rs))
    return rsi
# ========== RSI 计算函数结束 ==========

hist['RSI'] = calculate_rsi(hist['Close'])

# 买入信号：MACD 多头 + RSI 超卖
hist['BuySignal'] = (hist['DIF'] > hist['DEA']) & (hist['DEA'] > 0) & (hist['RSI'] < 30)

buy_dates = hist[hist['BuySignal']].index
print(f"MACD+RSI 买入信号数量: {len(buy_dates)}")

# 打印验收结果
if len(buy_dates) > 0:
    print("\n=== 最近5次买入信号 ===")
    print(hist.loc[buy_dates[-5:], ['Close', 'RSI', 'DIF', 'DEA']])
    
print("\n✅ 验收标准 1-3 全部通过则练习完成！")
```

---

### 练习 3（挑战）：MACD 背离检测

用上面的 find_macd_divergence 函数，检测你关注股票的 MACD 背离信号。

**验收标准：** 运行代码后，你应该能看到：
1. 检测出的所有背离信号
2. 每个背离信号的日期、价格、DIF 值
3. 判断是顶背离还是底背离

```python
def find_macd_divergence(hist, lookback=120, threshold=0.5):
    """
    识别 MACD 顶背离和底背离
    
    lookback: 用于判断"创新高/新低"的历史窗口（默认120天=半年）
    threshold: DIF 从高点下降超过 X 才算有效背离
    """
    signals = []
    
    for i in range(lookback, len(hist)):
        current_price = hist.iloc[i]['Close']
        current_dif = hist.iloc[i]['DIF']
        
        # 用 lookback 窗口判断是否"创新高/新低"
        lookback_data = hist.iloc[i-lookback:i]
        price_max = lookback_data['Close'].max()
        price_min = lookback_data['Close'].min()
        dif_max = lookback_data['DIF'].max()
        dif_min = lookback_data['DIF'].min()
        
        # 顶背离
        if current_price == price_max and (dif_max - current_dif) > threshold:
            signals.append({
                'date': hist.index[i],
                'type': '顶背离',
                'price': current_price,
                'dif': current_dif,
                'dif_max': dif_max
            })
        
        # 底背离
        if current_price == price_min and (current_dif - dif_min) > threshold:
            signals.append({
                'date': hist.index[i],
                'type': '底背离',
                'price': current_price,
                'dif': current_dif,
                'dif_min': dif_min
            })
    
    return signals

divergences = find_macd_divergence(hist)
print("=== MACD 背离信号 ===")
for sig in divergences:
    print(f"{sig['date'].date()}: {sig['type']} | 价格: {sig['price']:.2f} | DIF: {sig['dif']:.4f}")
```

---

## 📋 本课小结

### 🎯 核心知识点

| 概念 | 关键点 |
|------|--------|
| **MACD 组成** | DIF（快线）+ DEA（慢线）+ MACD 柱 |
| **DIF** | 12日 EMA - 26日 EMA，反映短期动量 |
| **DEA** | DIF 的 9 日 EMA，信号线 |
| **MACD 柱** | DIF - DEA，反映动量强弱（零轴上方=多头）|
| **MACD 四步计算** | EMA12 → EMA26 → DIF → DEA → MACD柱 |
| **12/26/9 参数来源** | Gerald Appel 的经验值，1970 年代至今有效 |
| **MACD 是滞后指标** | 至少滞后 26 天，不能用来预测 |
| **金叉** | DIF 上穿 DEA = 买入信号 |
| **死叉** | DIF 下穿 DEA = 卖出信号 |
| **零轴上方** | 上升趋势（12日 EMA > 26日 EMA）|
| **MACD 背离** | 比 RSI 背离更准确的转势信号（使用120天窗口判断新高/新低）|

### 💡 记住这句话

> **"MACD 不是用来抄底逃顶的，而是用来确认趋势的。零轴上方的金叉 + RSI 超卖 = 顺势抄底的最佳时机；零轴下方的死叉 + RSI 超买 = 逆势止盈的信号。"**

### 📚 第四课预告

**第四课：布林带——波动与风险的视觉化**

预告内容：
- 布林带的组成：中轨、上轨、下轨
- 为什么是 ±2 标准差？（统计学原理）
- 布林带的三大形态：开口、收口、挤压
- 布林带 + RSI 组合：双重过滤假突破
- 布林带 + MACD 组合：趋势确认 + 突破信号

---

## 📎 v1.3 更新说明

| 版本 | 日期 | 改动 |
|------|------|------|
| v1 | 2026-03-28 | Emily 初稿 |
| v1.1 | 2026-03-28 | Diana 审核后：修正"三步"→"四步"；练习2补充 calculate_rsi 函数；练习1添加验收标准 |
| v1.2 | 2026-03-28 | Claire QA 后：背离函数添加窗口局部极值说明；MACD 柱添加红绿色区分；参数推荐表格添加"来源：社区经验"标注；添加 MACD 信号速查表 |
| **v1.3** | 2026-03-28 | **Claire 顶背离代码逻辑修复：改用 lookback=120 天判断真正的新高/新低，替代原来的 window 内局部极值判断** |

---

*本课完 | 金融指标分析系列课程第三课 | Emily 老师*
