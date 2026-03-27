#!/usr/bin/env python3
"""
Emily 技术指标计算脚本
计算 RSI、MACD、Bollinger Bands、移动均线等

Bug修复 (2026-03-26):
- RSI 计算从 SMA 改为 Wilder's 平滑 (与 pandas-ta/TradingView 一致)
- 改用 Adj Close 替代 Close (考虑分红/拆股调整)
"""
import sys
import numpy as np
from datetime import datetime

def calculate_sma(prices, period):
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def calculate_ema(prices, period):
    if len(prices) < period:
        return None
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return ema

def calculate_rsi(prices, period=14):
    """
    使用 Wilder's 平滑计算 RSI (标准 RSI 算法)
    与 pandas-ta.ta.RSI() 和 TradingView 一致
    """
    if len(prices) < period + 1:
        return None
    
    # Calculate price changes
    deltas = np.diff(prices)
    
    # Separate gains and losses
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    
    # Initialize with SMA for first period (Wilder's 平滑起点)
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    
    # Apply Wilder's smoothing for remaining values
    # avg_gain = (prev_avg_gain * (period - 1) + current_gain) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def calculate_macd(prices, fast=12, slow=26, signal=9):
    if len(prices) < slow + signal:
        return None
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    if ema_fast is None or ema_slow is None:
        return None
    macd_line = ema_fast - ema_slow
    diffs = []
    for i in range(slow, len(prices)):
        ema_f = calculate_ema(prices[:i+1], fast)
        ema_s = calculate_ema(prices[:i+1], slow)
        if ema_f and ema_s:
            diffs.append(ema_f - ema_s)
    signal_line = calculate_ema(diffs, signal) if len(diffs) >= signal else macd_line
    return {'macd': round(macd_line, 4), 'signal': round(signal_line, 4), 'histogram': round(macd_line - signal_line, 4)}

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    if len(prices) < period:
        return None
    sma = calculate_sma(prices, period)
    if sma is None:
        return None
    std = (sum((p - sma) ** 2 for p in prices[-period:]) / period) ** 0.5
    return {'upper': round(sma + std_dev * std, 2), 'middle': round(sma, 2), 'lower': round(sma - std_dev * std, 2), 'bandwidth': round((std_dev * std * 2) / sma * 100, 2)}

def calculate_atr(highs, lows, closes, period=14):
    if len(highs) < 2:
        return None
    trs = [max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1])) for i in range(1, len(closes))]
    if len(trs) < period:
        return None
    return round(sum(trs[-period:]) / period, 4)

def get_technical_summary(ticker, period='3mo'):
    import yfinance as yf
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, auto_adjust=True)
    if hist.empty or len(hist) < 50:
        return None
    
    # Bug fix: 使用 Adj Close 替代 Close (考虑分红/拆股调整)
    if 'Adj Close' in hist.columns:
        closes = hist['Adj Close'].tolist()
    else:
        closes = hist['Close'].tolist()
    
    highs = hist['High'].tolist()
    lows = hist['Low'].tolist()
    volumes = hist['Volume'].tolist()
    price = closes[-1]
    avg_vol = sum(volumes[-20:]) / 20
    return {
        'ticker': ticker, 'price': round(price, 2),
        'change_1d': round((closes[-1] - closes[-2]) / closes[-2] * 100, 2) if len(closes) >= 2 else 0,
        'change_1w': round((closes[-1] - closes[-6]) / closes[-6] * 100, 2) if len(closes) >= 6 else 0,
        'change_1m': round((closes[-1] - closes[-21]) / closes[-21] * 100, 2) if len(closes) >= 21 else 0,
        'ma20': round(calculate_sma(closes, 20), 2) if len(closes) >= 20 else None,
        'ma50': round(calculate_sma(closes, 50), 2) if len(closes) >= 50 else None,
        'ma200': round(calculate_ema(closes, 200), 2) if len(closes) >= 200 else None,
        'rsi': calculate_rsi(closes, 14),
        'macd': calculate_macd(closes),
        'bollinger': calculate_bollinger_bands(closes, 20, 2),
        'atr': calculate_atr(highs, lows, closes, 14),
        'volume_ratio': round(volumes[-1] / avg_vol, 2) if avg_vol > 0 else 0,
        'avg_volume': int(avg_vol)
    }

def format_technical_report(data):
    if not data or 'error' in data:
        return f"### ❌ {data.get('ticker', 'Unknown')}: {data.get('error', 'No data')}\n"
    
    out = []
    out.append(f"### 🎯 {data['ticker']}\n")
    
    # Price
    emoji = "📈" if data['change_1d'] >= 0 else "📉"
    out.append(f"**价格:** ${data['price']} {emoji} {data['change_1d']:+.2f}% (日) | {data['change_1w']:+.2f}% (周) | {data['change_1m']:+.2f}% (月)\n")
    out.append("")
    
    # Moving averages
    out.append("**📊 移动均线:** ")
    mas = []
    if data['ma20']: mas.append(f"MA20 ${data['ma20']} {'✅' if data['price'] > data['ma20'] else '❌'}")
    if data['ma50']: mas.append(f"MA50 ${data['ma50']} {'✅' if data['price'] > data['ma50'] else '❌'}")
    if data['ma200']: mas.append(f"MA200 ${data['ma200']} {'✅' if data['price'] > data['ma200'] else '❌'}")
    out.append(" | ".join(mas) if mas else "数据不足")
    out.append("\n")
    
    # RSI
    out.append("**📈 RSI (14):** ")
    if data['rsi']:
        if data['rsi'] > 70: out.append(f"🔴 超买 ({data['rsi']})")
        elif data['rsi'] < 30: out.append(f"🟢 超卖 ({data['rsi']})")
        else: out.append(f"⚪ 中性 ({data['rsi']})")
    else:
        out.append("数据不足")
    out.append("\n")
    
    # MACD
    out.append("**📉 MACD (12,26,9):** ")
    if data['macd']:
        h = data['macd']['histogram']
        status = "🟢 金叉" if h > 0 else "🔴 死叉"
        out.append(f"{status} MACD:{data['macd']['macd']:.4f} Signal:{data['macd']['signal']:.4f} Hist:{h:+.4f}")
    else:
        out.append("数据不足")
    out.append("\n")
    
    # Bollinger Bands
    out.append("**🎯 Bollinger Bands (20,2):**\n")
    if data['bollinger']:
        bb = data['bollinger']
        out.append(f"Upper ${bb['upper']} | Middle ${bb['middle']} | Lower ${bb['lower']} (带宽:{bb['bandwidth']}%)\n")
        if data['price'] > bb['upper']: out.append("📈 突破上轨（超买）\n")
        elif data['price'] < bb['lower']: out.append("📉 跌破下轨（超卖）\n")
        else: out.append("⚪ 在中轨附近\n")
    
    # ATR & Volume
    out.append(f"**🌊 ATR (14):** ${data['atr'] if data['atr'] else 'N/A'}\n")
    out.append(f"**📊 成交量:** {data['volume_ratio']}x 均量\n")
    
    return "".join(out)

def main():
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ['SPY']
    print("## 📊 技术指标分析")
    print(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    for ticker in tickers:
        data = get_technical_summary(ticker)
        print(format_technical_report(data))

if __name__ == "__main__":
    main()
