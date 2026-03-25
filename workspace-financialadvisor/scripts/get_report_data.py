#!/usr/bin/env python3
"""
Emily 研报数据汇总脚本
自动获取所有需要的市场数据，供研报生成使用

使用方法:
    uv run --script scripts/get_report_data.py           # 获取所有数据
    uv run --script scripts/get_report_data.py --format markdown  # Markdown格式输出
    uv run --script scripts/get_report_data.py --format json      # JSON格式输出
"""

import sys
import json
from datetime import datetime

# 默认标的列表
DEFAULT_TICKERS = {
    # 宽基指数ETF
    'SPY': '标普500 ETF',
    'QQQ': '纳斯达克100 ETF',
    'DIA': '道琼斯ETF',
    'IWM': '罗素2000 ETF',
    
    # 大宗商品
    'GLD': '黄金ETF',
    'USO': '原油ETF',
    'CL=F': 'WTI原油期货',
    'GC=F': '黄金期货',
    
    # 国债/债券
    'TLT': '20年期国债ETF',
    'IEF': '7-10年期国债ETF',
    'BND': '综合债券ETF',
    
    # 恐慌指数
    'VIXY': 'VIX ETF',
    
    # 板块ETF
    'XLK': '科技板块',
    'XLE': '能源板块',
    'XLF': '金融板块',
    'XLV': '医疗板块',
    'XLY': '消费板块',
    'XLP': '必需消费',
    'XLRE': '房地产',
    'XLU': '公用事业',
    'XLI': '工业',
    'XLB': '材料',
    
    # 国际市场
    'EFA': 'EAFE国际指数',
    'EEM': '新兴市场指数',
    'FXI': '沪深300中国',
    
    # 科技股
    'NVDA': '英伟达',
    'AAPL': '苹果',
    'MSFT': '微软',
    'GOOGL': '谷歌',
    'META': 'Meta',
    'AMZN': '亚马逊',
    'TSLA': '特斯拉',
    
    # 金融
    'JPM': '摩根大通',
    'GS': '高盛',
    'BAC': '美国银行',
    'WFC': '富国银行',
    'C': '花旗',
    
    # 能源
    'XOM': '埃克森美孚',
    'CVX': '雪佛龙',
    'COP': '康菲石油',
    
    # 医疗
    'UNH': '联合健康',
    'JNJ': '强生',
    'PFE': '辉瑞',
    
    # 消费
    'WMT': '沃尔玛',
    'HD': '家得宝',
    'MCD': '麦当劳',
    
    # 工业
    'CAT': '卡特彼勒',
    'BA': '波音',
}

def get_all_market_data(tickers_dict=None):
    """获取所有市场数据"""
    try:
        import yfinance as yf
    except ImportError:
        print("Error: yfinance not installed")
        return {}
    
    if tickers_dict is None:
        tickers_dict = DEFAULT_TICKERS
    
    results = {}
    tickers_list = list(tickers_dict.keys())
    
    # 批量下载
    data = yf.download(tickers_list, period='1d', group_by='ticker', progress=False)
    
    for ticker, name in tickers_dict.items():
        try:
            if ticker in data.columns.get_level_values(0):
                ticker_data = data[ticker]
                
                current_price = ticker_data['Close'].iloc[-1] if len(ticker_data) > 0 else None
                prev_close = ticker_data['Open'].iloc[0] if len(ticker_data) > 0 else None
                
                if current_price and prev_close:
                    change = float(current_price) - float(prev_close)
                    pct = (change / float(prev_close)) * 100
                else:
                    change = 0
                    pct = 0
                
                results[ticker] = {
                    'symbol': ticker,
                    'name': name,
                    'current_price': float(current_price) if current_price else None,
                    'change': round(change, 2),
                    'change_percent': round(pct, 2),
                    'day_high': float(ticker_data['High'].max()) if len(ticker_data) > 0 else None,
                    'day_low': float(ticker_data['Low'].min()) if len(ticker_data) > 0 else None,
                }
            else:
                results[ticker] = {'symbol': ticker, 'name': name, 'error': 'No data'}
                
        except Exception as e:
            results[ticker] = {'symbol': ticker, 'name': name, 'error': str(e)}
    
    return results

def format_markdown(data):
    """格式化输出Markdown格式"""
    output = []
    output.append("## 📊 实时市场数据")
    output.append(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    output.append("")
    
    # 定义分类
    categories = {
        '📈 宽基指数': ['SPY', 'QQQ', 'DIA', 'IWM'],
        '🛢️ 大宗商品': ['GLD', 'USO', 'CL=F', 'GC=F'],
        '🏦 债券': ['TLT', 'IEF', 'BND'],
        '📊 板块ETF': ['XLK', 'XLE', 'XLF', 'XLV', 'XLY', 'XLP', 'XLRE', 'XLU', 'XLI', 'XLB'],
        '🌍 国际市场': ['EFA', 'EEM', 'FXI'],
        '💻 科技股': ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN', 'TSLA'],
        '🏦 金融股': ['JPM', 'GS', 'BAC', 'WFC', 'C'],
        '⛽ 能源股': ['XOM', 'CVX', 'COP'],
        '💊 医疗股': ['UNH', 'JNJ', 'PFE'],
        '🛒 消费股': ['WMT', 'HD', 'MCD'],
        '🏭 工业股': ['CAT', 'BA'],
    }
    
    for category, tickers in categories.items():
        output.append(f"### {category}")
        output.append("| 标的 | 名称 | 价格 | 涨跌 | 涨跌% |")
        output.append("|------|------|------|------|------|")
        
        has_data = False
        for ticker in tickers:
            if ticker in data and 'error' not in data[ticker]:
                d = data[ticker]
                arrow = "📈" if d['change'] >= 0 else "📉"
                price_str = f"${d['current_price']:.2f}" if d['current_price'] else "N/A"
                output.append(f"| {ticker} | {d['name']} | {price_str} | {arrow} {d['change']:+.2f} | {d['change_percent']:+.2f}% |")
                has_data = True
        
        if not has_data:
            output.append("| - | - | - | - | - |")
        
        output.append("")
    
    return "\n".join(output)

def format_json(data):
    """格式化输出JSON格式"""
    return json.dumps(data, indent=2, default=str)

if __name__ == '__main__':
    # 解析参数
    format_type = 'markdown'
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            format_type = sys.argv[idx + 1]
    
    data = get_all_market_data()
    
    if format_type == 'json':
        print(format_json(data))
    else:
        print(format_markdown(data))
