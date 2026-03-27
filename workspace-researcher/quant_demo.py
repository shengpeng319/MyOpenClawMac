"""
量化交易简单 Demo
- 获取 MSFT 历史数据
- 计算 MA(5, 20) 和 RSI
- MA 金叉/死叉交易信号
- matplotlib 可视化
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 无头模式
import numpy as np
from datetime import datetime, timedelta

# ========== 1. 获取数据 ==========
print("=" * 50)
print("📊 量化交易 Demo - MSFT")
print("=" * 50)

ticker = "MSFT"
msft = yf.Ticker(ticker)
df = msft.history(period="6mo")  # 6个月数据

print(f"\n📈 数据范围: {df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}")
print(f"   数据点数: {len(df)}")

# ========== 2. 计算技术指标 ==========
# MA (移动平均线)
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()

# RSI (相对强弱指数 - Wilder's smoothing)
def calc_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calc_rsi(df['Close'])

# ========== 3. 生成交易信号 ==========
# 金叉: MA5 上穿 MA20 -> 买入信号
# 死叉: MA5 下穿 MA20 -> 卖出信号
df['Signal'] = 0
df.loc[df['MA5'] > df['MA20'], 'Signal'] = 1   # 买入
df.loc[df['MA5'] < df['MA20'], 'Signal'] = -1  # 卖出

# 找到信号变化点
df['Position'] = df['Signal'].diff()

# ========== 4. 输出最新信号 ==========
latest = df.iloc[-1]
latest_rsi = latest['RSI']
latest_price = latest['Close']
latest_ma5 = latest['MA5']
latest_ma20 = latest['MA20']

print(f"\n💰 最新收盘价: ${latest_price:.2f}")
print(f"   MA5:  ${latest_ma5:.2f}")
print(f"   MA20: ${latest_ma20:.2f}")
print(f"   RSI(14): {latest_rsi:.2f}")

# 判断信号
if latest['MA5'] > latest['MA20']:
    signal = "📈 买入信号 (MA5 > MA20)"
elif latest['MA5'] < latest['MA20']:
    signal = "📉 卖出信号 (MA5 < MA20)"
else:
    signal = "⏸️ 持有信号 (MA5 ≈ MA20)"

print(f"\n【{signal}】")

# RSI 判断
if latest_rsi > 70:
    rsi_signal = "RSI 超买 (谨慎买入)"
elif latest_rsi < 30:
    rsi_signal = "RSI 超卖 (可能反弹)"
else:
    rsi_signal = "RSI 正常区间"

print(f"【{rsi_signal}】")

# 综合建议
print("\n" + "=" * 50)
print("🎯 持仓建议")
print("=" * 50)
if latest['MA5'] > latest['MA20'] and latest_rsi < 70:
    print("✅ 建议: 买入/持有")
    print(f"   理由: MA 金叉确认，RSI {latest_rsi:.0f} 尚未超买")
elif latest['MA5'] < latest['MA20'] and latest_rsi > 30:
    print("⚠️ 建议: 卖出/观望")
    print(f"   理由: MA 死叉确认，RSI {latest_rsi:.0f} 仍在正常区间")
elif latest_rsi > 70:
    print("⚠️ 建议: 持有/止盈")
    print(f"   理由: RSI {latest_rsi:.0f} 已超买")
elif latest_rsi < 30:
    print("⚠️ 建议: 持有/关注")
    print(f"   理由: RSI {latest_rsi:.0f} 已超卖，可能反弹")
else:
    print("⏸️ 建议: 观望")
print("=" * 50)

# ========== 5. 可视化 ==========
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# 图1: 价格 + MA + 买卖信号
ax1.plot(df.index, df['Close'], label='收盘价', color='blue', linewidth=1.5)
ax1.plot(df.index, df['MA5'], label='MA5', color='orange', linewidth=1, alpha=0.8)
ax1.plot(df.index, df['MA20'], label='MA20', color='green', linewidth=1, alpha=0.8)

# 标注买卖信号
buy_signals = df[df['Position'] == 2]
sell_signals = df[df['Position'] == -2]
ax1.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', s=150, label='买入', zorder=5)
ax1.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', s=150, label='卖出', zorder=5)

ax1.set_title(f'{ticker} 价格 & 移动平均线 (6个月)', fontsize=14)
ax1.set_ylabel('价格 ($)')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)

# 图2: RSI
ax2.plot(df.index, df['RSI'], label='RSI(14)', color='purple', linewidth=1)
ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='超买线(70)')
ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='超卖线(30)')
ax2.fill_between(df.index, 70, 100, alpha=0.1, color='red')
ax2.fill_between(df.index, 0, 30, alpha=0.1, color='green')
ax2.set_title('RSI 指标', fontsize=14)
ax2.set_ylabel('RSI')
ax2.set_ylim(0, 100)
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
output_path = '/Users/shengpeng319/.openclaw/workspace-researcher/quant_demo_result.png'
plt.savefig(output_path, dpi=150)
print(f"\n📊 图表已保存: {output_path}")

# ========== 6. 最近信号统计 ==========
print("\n📋 最近交易信号:")
signal_count = 0
for idx, row in df.iterrows():
    if row['Position'] == 2:
        print(f"   ✅ 买入 @ ${row['Close']:.2f} ({idx.strftime('%Y-%m-%d')})")
        signal_count += 1
    elif row['Position'] == -2:
        print(f"   ❌ 卖出 @ ${row['Close']:.2f} ({idx.strftime('%Y-%m-%d')})")
        signal_count += 1
    if signal_count >= 10:  # 最多显示10个
        break

print("\n✅ Demo 完成!")
