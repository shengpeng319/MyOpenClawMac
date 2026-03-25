#!/usr/bin/env python3
"""
Emily 基本面数据获取脚本
获取 EPS、营收增长、利润率、市盈率等财务指标
"""
import sys
from datetime import datetime

def get_fundamental_data(ticker):
    """获取单个标的基本面数据"""
    import yfinance as yf
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 基本信息
        data = {
            'ticker': ticker,
            'company_name': info.get('longName', info.get('shortName', 'N/A')),
            'price': info.get('currentPrice') or info.get('regularMarketPrice', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'beta': info.get('beta', 'N/A'),
            
            # 估值指标
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'forward_pe': info.get('forwardPE', 'N/A'),
            'peg_ratio': info.get('pegRatio', 'N/A'),
            'ps_ratio': info.get('priceToSalesTrailing12Months', 'N/A'),
            'pb_ratio': info.get('priceToBook', 'N/A'),
            
            # 盈利指标
            'eps': info.get('trailingEps', 'N/A'),
            'forward_eps': info.get('forwardEps', 'N/A'),
            'eps_growth': info.get('earningsGrowth', 'N/A'),
            'revenue_growth': info.get('revenueGrowth', 'N/A'),
            
            # 营收和利润
            'total_revenue': info.get('totalRevenue', 'N/A'),
            'revenue_per_share': info.get('revenuePerShare', 'N/A'),
            'gross_margin': info.get('grossMargin', 'N/A'),
            'operating_margin': info.get('operatingMargin', 'N/A'),
            'profit_margin': info.get('profitMargin', 'N/A'),
            'ebitda_margin': info.get('ebitdaMargins', 'N/A'),
            'net_income': info.get('netIncomeToCommon', 'N/A'),
            
            # 现金流
            'operating_cashflow': info.get('operatingCashflow', 'N/A'),
            'free_cashflow': info.get('freeCashflow', 'N/A'),
            
            # 股息
            'dividend_yield': info.get('dividendYield', 'N/A'),
            'dividend_rate': info.get('dividendRate', 'N/A'),
            
            # 52周区间
            'week52_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            'week52_low': info.get('fiftyTwoWeekLow', 'N/A'),
            'week52_change': info.get('52WeekChange', 'N/A'),
            
            # 推荐
            'recommendation': info.get('recommendationKey', 'N/A'),
            'target_price': info.get('targetMeanPrice', 'N/A'),
            
            # 分析师
            'analysts_count': info.get('numberOfAnalystOpinions', 'N/A'),
        }
        return data
    except Exception as e:
        return {'ticker': ticker, 'error': str(e)}

def format_large_number(value):
    """格式化大数字（亿/万）"""
    if value == 'N/A' or value is None:
        return 'N/A'
    try:
        value = float(value)
        if value >= 1e12:
            return f"${value/1e12:.2f}T"
        elif value >= 1e9:
            return f"${value/1e9:.2f}B"
        elif value >= 1e6:
            return f"${value/1e6:.2f}M"
        else:
            return f"${value:,.0f}"
    except:
        return str(value)

def format_percent(value):
    """格式化百分比"""
    if value == 'N/A' or value is None:
        return 'N/A'
    try:
        return f"{float(value)*100:.2f}%"
    except:
        return str(value)

def format_valuation(value):
    """格式化估值指标"""
    if value == 'N/A' or value is None:
        return 'N/A'
    try:
        return f"{float(value):.2f}"
    except:
        return str(value)

def format_fundamental_report(data):
    """格式化基本面报告"""
    if not data or 'error' in data:
        return f"### ❌ {data.get('ticker', 'Unknown')}: {data.get('error', 'No data')}\n"
    
    lines = []
    lines.append(f"### 📊 {data['ticker']} - 基本面数据")
    lines.append(f"*{data['company_name']}*")
    lines.append("")
    
    # 价格和市值
    lines.append("**📈 价格与市值**")
    price = data['price'] if data['price'] != 'N/A' else 'N/A'
    if price != 'N/A':
        lines.append(f"- 当前价格: ${price}")
    market_cap = format_large_number(data['market_cap'])
    lines.append(f"- 市值: {market_cap}")
    beta = format_valuation(data['beta'])
    lines.append(f"- Beta: {beta}")
    lines.append("")
    
    # 估值指标
    lines.append("**🎯 估值指标**")
    pe = format_valuation(data['pe_ratio'])
    fpe = format_valuation(data['forward_pe'])
    peg = format_valuation(data['peg_ratio'])
    ps = format_valuation(data['ps_ratio'])
    pb = format_valuation(data['pb_ratio'])
    lines.append(f"- 市盈率 (P/E): {pe}")
    lines.append(f"- 远期市盈率 (Forward P/E): {fpe}")
    lines.append(f"- PEG比率: {peg}")
    lines.append(f"- 市销率 (P/S): {ps}")
    lines.append(f"- 市净率 (P/B): {pb}")
    lines.append("")
    
    # 盈利指标
    lines.append("**💰 盈利指标**")
    eps = format_valuation(data['eps'])
    feps = format_valuation(data['forward_eps'])
    lines.append(f"- 每股收益 (EPS TTM): {eps}")
    lines.append(f"- 远期每股收益 (Forward EPS): {feps}")
    
    eps_growth = format_percent(data['eps_growth'])
    rev_growth = format_percent(data['revenue_growth'])
    lines.append(f"- EPS增长: {eps_growth}")
    lines.append(f"- 营收增长: {rev_growth}")
    lines.append("")
    
    # 营收和利润
    lines.append("**📊 营收与利润率**")
    revenue = format_large_number(data['total_revenue'])
    lines.append(f"- 总营收 (TTM): {revenue}")
    
    gross_margin = format_percent(data['gross_margin'])
    op_margin = format_percent(data['operating_margin'])
    profit_margin = format_percent(data['profit_margin'])
    ebitda_margin = format_percent(data['ebitda_margin'])
    
    lines.append(f"- 毛利率: {gross_margin}")
    lines.append(f"- 营业利润率: {op_margin}")
    lines.append(f"- 净利率: {profit_margin}")
    lines.append(f"- EBITDA利润率: {ebitda_margin}")
    lines.append("")
    
    # 现金流
    lines.append("**💵 现金流**")
    op_cf = format_large_number(data['operating_cashflow'])
    fc = format_large_number(data['free_cashflow'])
    lines.append(f"- 经营现金流: {op_cf}")
    lines.append(f"- 自由现金流: {fc}")
    lines.append("")
    
    # 股息
    lines.append("**💵 股息**")
    div_yield = format_percent(data['dividend_yield'])
    div_rate = format_valuation(data['dividend_rate'])
    lines.append(f"- 股息率: {div_yield}")
    lines.append(f"- 股息: {div_rate}")
    lines.append("")
    
    # 52周区间
    lines.append("**📅 52周区间**")
    high52 = format_valuation(data['week52_high'])
    low52 = format_valuation(data['week52_low'])
    price_now = data['price'] if data['price'] != 'N/A' else 0
    lines.append(f"- 最高: ${high52}")
    lines.append(f"- 最低: ${low52}")
    if price_now and data['week52_high'] != 'N/A' and float(data['week52_high']) > 0:
        position = (float(price_now) - float(data['week52_low'])) / (float(data['week52_high']) - float(data['week52_low'])) * 100
        lines.append(f"- 当前在52周区间中的位置: {position:.1f}%")
    lines.append("")
    
    # 分析师评级
    lines.append("**👔 分析师评级**")
    rec = data['recommendation']
    target = format_valuation(data['target_price'])
    analysts = data['analysts_count']
    lines.append(f"- 评级: {rec}")
    lines.append(f"- 目标价: ${target}")
    lines.append(f"- 分析师数量: {analysts}")
    lines.append("")
    
    return "\n".join(lines)

def main():
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ['SPY']
    
    print("## 📊 基本面数据")
    print(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    print("")
    
    for ticker in tickers:
        data = get_fundamental_data(ticker)
        print(format_fundamental_report(data))
        print("")

if __name__ == "__main__":
    main()
