#!/usr/bin/env python3
"""
Emily 实时市场数据获取脚本
使用 yfinance 获取实时市场数据

使用方法:
    uv run --script scripts/get_market_data.py          # 获取所有数据
    uv run --script scripts/get_market_data.py SPY QQQ  # 获取指定标的
"""

import sys
import json
from datetime import datetime

def get_market_data(tickers=None):
    """获取市场数据"""
    try:
        import yfinance as yf
    except ImportError:
        print("Error: yfinance not installed. Run: uv pip install yfinance")
        sys.exit(1)
    
    if tickers is None:
        tickers = ['SPY', 'QQQ', 'DIA', 'IWM', 'GLD', 'USO', 'CL=F', 'GC=F']
    
    results = {}
    
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            info = data.info
            
            # 提取关键数据
            results[ticker] = {
                'symbol': ticker,
                'current_price': info.get('currentPrice') or info.get('regularMarketPrice'),
                'previous_close': info.get('previousClose') or info.get('regularMarketPreviousClose'),
                'change': info.get('regularMarketChange'),
                'change_percent': info.get('regularMarketChangePercent'),
                'day_high': info.get('dayHigh'),
                'day_low': info.get('dayLow'),
                'volume': info.get('volume'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'dividend_yield': info.get('dividendYield'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
                'name': info.get('shortName') or info.get('longName', ticker),
            }
            
            # 计算涨跌
            if results[ticker]['previous_close'] and results[ticker]['current_price']:
                change = results[ticker]['current_price'] - results[ticker]['previous_close']
                pct = (change / results[ticker]['previous_close']) * 100
                results[ticker]['change'] = round(change, 2)
                results[ticker]['change_percent'] = round(pct, 2)
            
        except Exception as e:
            results[ticker] = {'symbol': ticker, 'error': str(e)}
    
    return results

def print_market_data(data):
    """格式化打印市场数据"""
    print("=" * 60)
    print(f"📊 Emily 市场数据 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    for symbol, info in data.items():
        if 'error' in info:
            print(f"❌ {symbol}: {info['error']}")
            continue
        
        price = info.get('current_price', 'N/A')
        change = info.get('change', 0)
        pct = info.get('change_percent', 0)
        
        # 涨跌符号
        if change and change > 0:
            arrow = "📈"
            change_str = f"+{change:.2f}"
            pct_str = f"+{pct:.2f}%"
        elif change and change < 0:
            arrow = "📉"
            change_str = f"{change:.2f}"
            pct_str = f"{pct:.2f}%"
        else:
            arrow = "➡️"
            change_str = "0.00"
            pct_str = "0.00%"
        
        name = info.get('name', symbol)
        print(f"\n{arrow} {name} ({symbol})")
        print(f"   价格: ${price:.2f} | 涨跌: {change_str} ({pct_str})")
        
        if info.get('day_high') and info.get('day_low'):
            print(f"   日高/日低: ${info['day_high']:.2f} / ${info['day_low']:.2f}")
        
        if info.get('pe_ratio'):
            print(f"   P/E: {info['pe_ratio']:.2f}")
        
        if info.get('market_cap'):
            mcap = info['market_cap']
            if mcap >= 1e12:
                print(f"   市值: ${mcap/1e12:.2f}T")
            elif mcap >= 1e9:
                print(f"   市值: ${mcap/1e9:.2f}B")
    
    print("\n" + "=" * 60)

def print_json(data):
    """输出JSON格式数据"""
    print(json.dumps(data, indent=2, default=str))

if __name__ == '__main__':
    # 获取命令行参数
    tickers = sys.argv[1:] if len(sys.argv) > 1 else None
    
    data = get_market_data(tickers)
    
    # 如果指定了 --json 参数，输出JSON格式
    if '--json' in sys.argv:
        print_json(data)
    else:
        print_market_data(data)
