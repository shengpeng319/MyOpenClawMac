# 金融指标分析系列课程

## 📗 第二课：判断超买超卖——RSI（相对强弱指数）

*Emily 老师出品 | 2026-03-28 | v3.0（Diana 教育审核版）*

---

## 🎯 学习目标

学完这课后，你能：
- ✅ 理解 RSI 的含义——为什么它能判断超买超卖
- ✅ 掌握 RSI 的计算方法，特别是 Wilder's 平滑算法
- ✅ 用 Python 计算并绘制 RSI
- ✅ 识别 RSI 的超买超卖信号
- ✅ 识别 RSI 背离——最重要的转势信号
- ✅ 识别 RSI 高位钝化和低位钝化现象
- ✅ 避开使用 RSI 时的常见误区

---

## 🌅 开篇：为什么需要 RSI？

想象你参加一场马拉松比赛。

- 第1公里：你精力充沛，跑得很快（相当于股票刚涨）
- 第10公里：你开始疲劳，速度下降
- 第30公里：很多人已经走不动了，但有人在硬撑

**问题是：你怎么知道选手们是真的跑不动了，还是在蓄力冲刺？**

股票也是一样。股价涨了，你不知道是多头力量还没释放完，还是已经涨过头了、快要回调了。

**RSI 就是股市里的"体能检测仪"。**

它告诉你这只股票现在是"体能过剩"（超买）还是"体力透支"（超卖）。体能过剩继续涨会累垮，体力透支后反而可能爆发力反弹。

> 💡 **生活中的类比：** RSI 就像健身房的体脂秤。体脂率 5% 以下（超低）意味着你需要补充能量，体脂率 35%（超高）意味着你需要加大运动量。RSI < 30 = 该补充"能量"（买入），RSI > 70 = 该"减脂"（卖出）。

---

## 📊 什么是 RSI？

**RSI（Relative Strength Index，相对强弱指数）** 由 J. Welles Wilder 于 1978 年发明，是最常用的超买超卖指标。

**RSI 的核心逻辑：**
```
RSI = 100 - (100 / (1 + RS))
其中 RS = 平均涨幅 / 平均跌幅
```

**RS 是什么意思？**
- 如果最近14天，股票平均每天涨 $2，跌 $1 → RS = 2，RSI = 66.7（偏强）
- 如果最近14天，股票平均每天涨 $1，跌 $2 → RS = 0.5，RSI = 33.3（偏弱）

**为什么 RSI 的范围是 0-100？**
因为 RS 是"平均涨幅 / 平均跌幅"，是一个比率：
- 涨跌幅相等 → RS = 1 → RSI = 50（中性）
- 涨幅远大于跌幅 → RS → ∞ → RSI → 100（极强）
- 跌幅远大于涨幅 → RS → 0 → RSI → 0（极弱）

**这就是 RSI 能反映"相对强弱"的数学原理。**

---

## 🔢 计算方法

### 1️⃣ RSI 标准参数：14 天

**为什么是 14 天？**
Wilder 在 1978 年的原著《New Concepts in Technical Trading Systems》里推荐 14 天，这是一个经验值：
- 太短（如 5 天）：噪音太多，信号不稳定
- 太长（如 30 天）：反应太慢，错过时机
- **14 天刚好平衡了灵敏度和稳定性**

**这就是为什么 99% 的交易软件默认 RSI(14)。**

### 2️⃣ RSI 的计算方法

#### 方法 A：简单平均法（❌ 不推荐）

```python
# 简单但有缺陷
delta = prices.diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))
```

**问题：** 这种方法会让最新的数据和最老的数据权重一样，导致 RSI 变化迟缓。

#### 方法 B：Wilder's 平滑法（✅ 推荐/正确方法）

**为什么 Wilder's 平滑更好？**
因为它用了**指数加权**的思想，最新的数据权重更大，反应更快。

**核心公式：**
```
今日平均涨幅 = (昨日平均涨幅 × 13 + 今日涨幅) / 14
今日平均跌幅 = (昨日平均跌幅 × 13 + 今日跌幅) / 14
```

简单理解：今天的平均值 ≈ 昨天的平均值 + 一点点今天的新数据

这就是为什么 pandas 的 `ewm(alpha=1/14)` 就是 Wilder's 平滑！

### ⚠️ 极端值情况处理

**当 avg_loss = 0 时（所有日子都在涨）：**
```
RS = avg_gain / 0 = ∞
RSI = 100 - (100 / (1 + ∞)) = 100
```
→ RSI = 100 不是错误，是数学上的正确结果！

**当 avg_gain = 0 时（所有日子都在跌）：**
```
RS = 0 / avg_loss = 0
RSI = 100 - (100 / (1 + 0)) = 0
```
→ RSI = 0 不是错误，是数学上的正确结果！

**Python 处理极端值的方法：**
```python
def calculate_rsi(prices, period=14):
    """
    计算 RSI，处理极端情况
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Wilder's 平滑
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    
    # 处理极端情况
    rs = avg_gain / avg_loss
    rs = rs.replace([np.inf, -np.inf], 0)  # 处理除零情况
    
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(50)  # 初始值设为中性
    
    return rsi

hist['RSI'] = calculate_rsi(hist['Close'])
```

---

## 📈 RSI 的核心用法

### 1️⃣ 超买超卖区间

| RSI 值 | 含义 | 操作建议 |
|--------|------|---------|
| **RSI > 70** | 超买区 | 考虑卖出或减仓 |
| **RSI 50** | 中性 | 观望 |
| **RSI < 30** | 超卖区 | 考虑买入或加仓 |
| **RSI < 20** | 极端超卖 | 极强买入信号 |

**为什么是 70 和 30？**
这是统计学上的经验值：
- 历史数据显示，RSI > 70 的日子，后续下跌的概率显著增加
- RSI < 30 的日子，后续反弹的概率显著增加
- 这不是绝对的，但概率上是有利的

**为什么不是 80/20？**
- 80/20 会错过很多有效信号
- 70/30 是 Wilder 经过大量历史数据测试后的最优解
- 当然，你也可以根据不同股票的性格调整（比如波动大的用 80/20）

### 2️⃣ RSI 高位钝化和低位钝化

**什么是高位钝化？**
强势股（如 Tesla、Coinbase）在牛市里可能连续数周 RSI 在 65-75 之间徘徊，迟迟不突破 70 进入超买区，也迟迟不回调。这就是"高位钝化"—— RSI 一直在相对高位，但股价还在涨。

**什么是低位钝化？**
弱势股在熊市里可能连续数月 RSI 在 25-35 之间徘徊，迟迟不突破 30 进入超卖区，也迟迟不反弹。这就是"低位钝化"—— RSI 一直在相对低位，但股价还在跌。

**为什么会出现钝化？**
因为 RSI 是相对强弱指标，衡量的是"最近14天涨了多少 vs 跌了多少"。如果一只股票每天都在涨（即使涨幅很小），累积效应会让 RSI 持续处于相对高位。

**如何应对钝化？**
- **不要**看到 RSI > 70 就立刻卖出（可能错过更多利润）
- **不要**看到 RSI < 30 就立刻买入（可能接飞刀）
- 结合趋势判断：上升趋势中 RSI 在 65-75 徘徊可能是正常回调；下降趋势中 RSI 在 25-35 徘徊可能只是中继

---

### 3️⃣ RSI 背离——最重要的转势信号

**什么是背离？**
背离就是 RSI 和股价"打架"了——一个往东，一个往西。这通常意味着趋势即将反转。

#### 顶背离（看跌信号）⚠️

**现象：** 股价创新高，但 RSI 没有创新高

**为什么是看跌信号？**
- 正常情况：股价创新高 = 多头力量强 → RSI 也该创新高
- 顶背离：股价创新高，但 RSI 没跟上 = 多头力量已经在衰减！

**文字描述：**
```
股价：不断创出新高 --------（最高点）
                            ↗ （继续上涨）
RSI：  在这里掉头向下 -----↗ （没能创新高）
```

#### 底背离（看涨信号）✅

**现象：** 股价创新低，但 RSI 没有创新低

**为什么是看涨信号？**
- 正常情况：股价创新低 = 空头力量强 → RSI 也该创新低
- 底背离：股价创新低，但 RSI 没跟上 = 空头力量已经在衰减！

**文字描述：**
```
RSI：  在这里掉头向上 -----↘ （没能创新低）
                            ↘ （开始反弹）
股价：不断创出新低 --------（最低点）
```

**Python 代码：识别背离（修正版，含阈值）**
```python
def find_divergence(hist, window=60, rsi_drop_threshold=5):
    """
    识别 RSI 顶背离和底背离
    rsi_drop_threshold: RSI 从高点下降超过 X% 才算有效背离
    """
    signals = []
    
    for i in range(window, len(hist)):
        # 最近 window 天的数据
        window_data = hist.iloc[i-window:i]
        
        # 找最高点和最低点
        price_max = window_data['Close'].max()
        price_min = window_data['Close'].min()
        rsi_max = window_data['RSI'].max()
        rsi_min = window_data['RSI'].min()
        
        # 当前点
        current_price = hist.iloc[i]['Close']
        current_rsi = hist.iloc[i]['RSI']
        
        # 顶背离：价格创新高且 RSI 从高点下降超过阈值
        if current_price == price_max and (rsi_max - current_rsi) > rsi_drop_threshold:
            signals.append({
                'date': hist.index[i],
                'type': '顶背离',
                'price': current_price,
                'rsi': current_rsi,
                'rsi_max': rsi_max
            })
        
        # 底背离：价格创新低且 RSI 从低点上升超过阈值
        if current_price == price_min and (current_rsi - rsi_min) > rsi_drop_threshold:
            signals.append({
                'date': hist.index[i],
                'type': '底背离',
                'price': current_price,
                'rsi': current_rsi,
                'rsi_min': rsi_min
            })
    
    return signals

# 查找背离信号（RSI 变化超过 5% 才算有效）
divergences = find_divergence(hist, rsi_drop_threshold=5)
print("=== 背离信号 ===")
for sig in divergences[-10:]:  # 最近10个信号
    print(f"{sig['date'].date()}: {sig['type']} | 价格: {sig['price']:.2f} | RSI: {sig['rsi']:.2f}")
```

---

## 🖥️ 实战应用

### 案例 1：完整 RSI 分析代码

```python
# 安装 pandas_ta（如果还没安装）
!pip install pandas_ta

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta

%matplotlib inline

# 获取 MSFT 数据（RSI 经典案例）
msft = yf.Ticker('MSFT')
hist = msft.history(period='1y')

# 方法1：使用 pandas_ta（推荐）
hist['RSI'] = ta.rsi(hist['Close'], length=14)

# 方法2：手动计算（理解原理）
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rs = rs.replace([np.inf, -np.inf], 0)
    rsi = 100 - (100 / (1 + rs))
    return rsi

hist['RSI_manual'] = calculate_rsi(hist['Close'])

# 绘制股价和 RSI
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# 股价
ax1.plot(hist.index, hist['Close'], label='MSFT 收盘价', color='blue')
ax1.set_title('MSFT 股价与 RSI 分析', fontsize=16)
ax1.set_ylabel('价格 (USD)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# RSI
ax2.plot(hist.index, hist['RSI'], label='RSI(14)', color='purple')
ax2.axhline(y=70, color='red', linestyle='--', label='超买线 (70)')
ax2.axhline(y=30, color='green', linestyle='--', label='超卖线 (30)')
ax2.axhline(y=50, color='gray', linestyle=':', label='中性线 (50)')
ax2.fill_between(hist.index, 70, 100, alpha=0.1, color='red')  # 超买区
ax2.fill_between(hist.index, 0, 30, alpha=0.1, color='green')  # 超卖区
ax2.set_ylabel('RSI')
ax2.set_ylim(0, 100)
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 打印 RSI 统计
print(f"RSI 当前值: {hist['RSI'].iloc[-1]:.2f}")
print(f"RSI 最高值: {hist['RSI'].max():.2f}")
print(f"RSI 最低值: {hist['RSI'].min():.2f}")
print(f"RSI 平均值: {hist['RSI'].mean():.2f}")
```

**📊 案例结果解读：**
运行后你会看到：
- 上图是股价，下图是 RSI
- RSI 在 30 以下（绿色区域）是超卖区，可能是买入机会
- RSI 在 70 以上（红色区域）是超买区，可能是卖出机会
- RSI 50 是中性线，在它以上偏强，以下偏弱

**⚠️ pandas_ta 安装失败备选方案：**
如果 `!pip install pandas_ta` 失败，可以用手动计算方法：
```python
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rs = rs.replace([np.inf, -np.inf], 0)
    rsi = 100 - (100 / (1 + rs))
    return rsi

hist['RSI'] = calculate_rsi(hist['Close'])
```

---

### 案例 2：RSI + 均线组合策略

**为什么这个组合有效？**
- 均线判断趋势方向
- RSI 判断买卖时机

**策略逻辑：**
- 只在多头排列时买入（MA20 > MA60）
- RSI < 30 时买入（抄底）
- RSI > 70 时卖出（逃顶）

```python
# 计算信号
hist['MA20'] = hist['Close'].rolling(20).mean()
hist['MA60'] = hist['Close'].rolling(60).mean()
hist['RSI'] = ta.rsi(hist['Close'], 14)

# 买入信号：多头排列 + RSI 超卖
hist['BuySignal'] = (hist['MA20'] > hist['MA60']) & (hist['RSI'] < 30)

# 卖出信号：RSI 超买
hist['SellSignal'] = hist['RSI'] > 70

# 查看信号
buy_dates = hist[hist['BuySignal']].index
sell_dates = hist[hist['SellSignal']].index

print(f"买入信号数量: {len(buy_dates)}")
print(f"卖出信号数量: {len(sell_dates)}")
print("\n最近买入信号:")
print(hist.loc[buy_dates[-5:], ['Close', 'RSI', 'MA20', 'MA60']])
```

**📊 案例结果解读：**
- 买入信号 = 多头排列（趋势向上）+ RSI 超卖（价格偏低）= 顺势抄底
- 卖出信号 = RSI 超买（价格偏高）= 逆势止盈
- 信号数量不宜过多，如果太频繁说明参数需要调整

---

## ⚠️ 常见误区

### ❌ 误区 1：RSI > 70 一定要卖出

**为什么不对？**
- 强势股可以长时间维持在 RSI > 70（"高位钝化"）
- 做空卖在 RSI > 70 可能被逼空

**✅ 正确做法：**
- RSI > 70 是"提醒"，不是"命令"
- 结合作者的"第一课"均线趋势判断
- 上升趋势中 RSI 在 65-75 徘徊可能是正常回调
- 下降趋势中 RSI > 70 才是真正该卖的时候

---

### ❌ 误区 2：RSI < 30 一定要买入

**为什么不对？**
- 弱势股可以长时间维持在 RSI < 30（"低位钝化"）
- 地板下面还有地下室

**✅ 正确做法：**
- RSI < 30 是"机会"，但要确认"地基"稳固
- 结合作者的"第一课"均线趋势判断
- 下降趋势中 RSI 在 25-35 徘徊可能只是下跌中继
- 上升趋势中 RSI < 30 才是真正的买入机会

---

### ❌ 误区 3：所有股票用同一个 RSI 参数

**为什么不对？**
- 蓝筹股（Apple、Microsoft）波动相对小，RSI 很少到极端值
- 成长股（Tesla、Coinbase）波动大，RSI 经常到极端值
- 周期股（航空、能源）RSI 规律和成长股完全不同

**✅ 正确做法：**
| 股票类型 | 建议 RSI 参数 |
|---------|-------------|
| 高波动成长股（TSLA、Coinbase）| RSI(7) 或 RSI(10) |
| 普通股票 | RSI(14)（默认）|
| 低波动蓝筹股 | RSI(21) |
| 周期股 | RSI(14)，注意趋势判断 |

---

### ❌ 误区 4：把 RSI 当成预测工具

**为什么不对？**
- RSI 是**滞后指标**（lagging indicator），不是预测工具
- 它告诉你的是"已经发生了什么"，不是"将要发生什么"

**✅ 正确做法：**
- RSI 帮你确认趋势，不是预测趋势
- RSI > 70 → 确认上涨动力强劲
- RSI < 30 → 确认下跌动能强劲
- 结合作者的"第三课"MACD 等领先指标

---

## 🧠 思考题

### 思考题 1：
假设某股票最近14天收盘价变化分别是：
+$3, +$2, -$1, +$4, +$1, -$2, +$5, -$3, +$2, +$1, -$1, +$3, +$2, +$4

请手动计算：
- 平均涨幅 = ?
- 平均跌幅 = ?
- RS = ?
- RSI = ?

### 思考题 2：
一只股票在上升趋势中，RSI 持续在 65-75 之间徘徊，但没有一次突破 70。这是好事还是坏事？这种现像叫什么？

### 思考题 3：
"RSI 底背离意味着股价一定会反弹"，你同意吗？如果不同意，应该怎么理解 RSI 底背离？

---

## 📝 练习题

### 练习 1（入门）：计算你关注股票的 RSI
```python
# 安装 pandas_ta（如果还没安装）
!pip install pandas_ta

import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt

%matplotlib inline

# 换成你想看的股票
ticker = 'NVDA'

stock = yf.Ticker(ticker)
hist = stock.history(period='6mo')

# 计算 RSI
hist['RSI'] = ta.rsi(hist['Close'], length=14)

# 绘制
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
ax1.plot(hist.index, hist['Close'])
ax1.set_title(f'{ticker} 股价')
ax2.plot(hist.index, hist['RSI'], color='purple')
ax2.axhline(y=70, color='red', linestyle='--')
ax2.axhline(y=30, color='green', linestyle='--')
ax2.set_ylim(0, 100)
ax2.set_title(f'{ticker} RSI')
plt.show()

print(f"{ticker} 当前 RSI: {hist['RSI'].iloc[-1]:.2f}")
```

---

### 练习 2（进阶）：识别超买超卖事件
修改上面的代码，找出 RSI > 70 和 RSI < 30 的日期，计算每次超买后多久开始下跌（超卖后多久开始反弹）。

**提示：** 可以用以下方法找日期：
```python
# 找出 RSI > 70 的日期
overbought_dates = hist[hist['RSI'] > 70].index
print(f"超买日期数量: {len(overbought_dates)}")
```

---

### 练习 3（挑战）：检测 RSI 背离
用第一课的数据，尝试检测 AAPL 或 NVDA 的 RSI 背离信号。

```python
# 使用之前定义的 find_divergence 函数
divergences = find_divergence(hist, rsi_drop_threshold=5)
print("=== 背离信号 ===")
for sig in divergences:
    print(f"{sig['date'].date()}: {sig['type']} | 价格: {sig['price']:.2f} | RSI: {sig['rsi']:.2f}")
```

---

## 📋 本课小结

### 🎯 核心知识点

| 概念 | 关键点 |
|------|--------|
| **RSI 含义** | 相对强弱指数，反映股票在最近14天的涨跌相对强度 |
| **RSI 公式** | RSI = 100 - (100 / (1 + RS))，RS = 平均涨幅 / 平均跌幅 |
| **Wilder's 平滑** | 正确的 RSI 计算方法，用 ewm(alpha=1/14) 实现 |
| **极端值处理** | avg_loss=0 → RSI=100；avg_gain=0 → RSI=0（数学正确，非错误）|
| **超买区** | RSI > 70，可能回调（注意高位钝化）|
| **超卖区** | RSI < 30，可能反弹（注意低位钝化）|
| **高位钝化** | 强势股长期 RSI 在 65-75 徘徊，RSI 失效 |
| **低位钝化** | 弱势股长期 RSI 在 25-35 徘徊，RSI 失效 |
| **顶背离** | 股价创新高但 RSI 没跟上 → 看跌信号 |
| **底背离** | 股价创新低但 RSI 没创新低 → 看涨信号 |
| **参数自适应** | 高波动股用 RSI(7/10)，低波动股用 RSI(21) |

### 💡 记住这句话

> **"RSI 不是告诉你什么时候买，而是告诉你什么时候该小心。超买不代表立刻跌，超卖不代表立刻涨——但它们都在提醒你：注意风险/机会。结合趋势判断，才能用好 RSI。"**

### 📚 第三课预告

**第三课：MACD——趋势确认与动量捕捉**

预告内容：
- MACD 的组成：DIF、DEA、MACD 柱
- 为什么用 12 和 26 这两个参数？（和 EMA 的历史有关）
- MACD 金叉死叉的真正含义
- MACD 背离：比 RSI 背离更准确的反转信号
- RSI + MACD 组合：双重确认交易信号

---

## 📎 v3.0 更新说明

| 版本 | 日期 | 改动 |
|------|------|------|
| v1 | 2026-03-28 | Emily 初版 |
| v2 | 2026-03-28 | Claire QA 后：添加 pandas_ta 安装说明；添加极端值处理说明；修正背离检测阈值 |
| v3 | 2026-03-28 | Diana 教育审核后：删除背离 ASCII 图改用文字描述；简化 Wilder's 平滑解释；高位钝化补充 65-75 徘徊描述；添加 pandas_ta 备选方案；练习2加代码提示；背离加 RSI 变化阈值(5%)；首次"滞后指标"加括号解释 |

---

*本课完 | 金融指标分析系列课程第二课 | Emily 老师*
