#!/usr/bin/env python3
"""
US ETF 异动监控脚本
阈值: ±3% 涨跌幅触发警报
"""

import yfinance as yf
import json
from datetime import datetime

ETFS = ['SPY', 'QQQ', 'DIA']
THRESHOLD = 3.0  # 涨跌幅阈值 %

def check_etfs():
    results = []
    alerts = []
    
    for etf in ETFS:
        try:
            ticker = yf.Ticker(etf)
            info = ticker.info
            
            current_price = info.get('regularMarketPrice')
            prev_close = info.get('previousClose')
            market_state = info.get('marketState', 'UNKNOWN')
            
            if current_price and prev_close:
                change_pct = ((current_price - prev_close) / prev_close) * 100
                
                result = {
                    'etf': etf,
                    'price': round(current_price, 2),
                    'prev_close': round(prev_close, 2),
                    'change_pct': round(change_pct, 2),
                    'market_state': market_state,
                    'alert': abs(change_pct) >= THRESHOLD
                }
                results.append(result)
                
                if result['alert']:
                    direction = '🔺 涨幅' if change_pct > 0 else '🔻 跌幅'
                    alerts.append(f"{etf}: {direction} {change_pct:+.2f}% (${current_price})")
        except Exception as e:
            results.append({'etf': etf, 'error': str(e)})
    
    return results, alerts

def format_message(results, alerts):
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 构建表格
    lines = [f"**📊 美股 ETF 监控** ({now})"]
    lines.append("")
    lines.append("| ETF | 现价 | 昨收 | 涨跌幅 |")
    lines.append("|-----|------|------|--------|")
    
    for r in results:
        if 'error' in r:
            lines.append(f"| {r['etf']} | 错误: {r['error']} | - | - |")
        else:
            change_emoji = "🟢" if r['change_pct'] > 0 else "🔴" if r['change_pct'] < 0 else "⚪"
            lines.append(f"| {r['etf']} | ${r['price']} | ${r['prev_close']} | {change_emoji} {r['change_pct']:+.2f}% |")
    
    if alerts:
        lines.append("")
        lines.append("**🚨 异动警报:**")
        for a in alerts:
            lines.append(f"- {a}")
    
    return "\n".join(lines)

if __name__ == '__main__':
    results, alerts = check_etfs()
    message = format_message(results, alerts)
    print(message)
    
    # 输出 JSON 格式供脚本调用
    print("\n---JSON---")
    print(json.dumps({'results': results, 'alerts': alerts, 'message': message}))
