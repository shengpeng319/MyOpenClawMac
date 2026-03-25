#!/usr/bin/env python3
"""
Emily 风险指标计算脚本
计算投资组合/ETF的风险指标：VaR, Sharpe Ratio, Sortino Ratio, Max Drawdown等

使用方法:
    uv run --script scripts/get_risk_metrics.py SPY          # 单标的
    uv run --script scripts/get_risk_metrics.py SPY QQQ GLD   # 多标的
"""

import sys
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def calculate_risk_metrics(ticker, period='3mo'):
    """计算风险指标"""
    try:
        import yfinance as yf
    except ImportError:
        return {'error': 'yfinance not installed'}
    
    try:
        # 下载历史数据
        data = yf.download(ticker, period=period, progress=False)
        
        if data.empty or len(data) < 30:
            return {'error': f'Insufficient data for {ticker}'}
        
        # 处理yfinance返回的多级索引列
        if isinstance(data.columns, pd.MultiIndex):
            close_prices = data['Close'][ticker]
        else:
            close_prices = data['Close']
        
        # 计算日收益率
        returns = close_prices.pct_change().dropna()
        
        # 基本统计
        mean_return = returns.mean() * 252  # 年化收益率
        std_return = returns.std() * np.sqrt(252)  # 年化波动率
        
        # VaR (Value at Risk) - 95% confidence
        var_95 = np.percentile(returns, 5)
        cvar_95 = returns[returns <= var_95].mean()  # CVaR / Expected Shortfall
        
        # VaR - 99% confidence
        var_99 = np.percentile(returns, 1)
        
        # Sharpe Ratio (假设无风险利率 3.5%)
        risk_free_rate = 0.035
        sharpe = (mean_return - risk_free_rate) / std_return if std_return > 0 else 0
        
        # Sortino Ratio (只用下行波动率)
        negative_returns = returns[returns < 0]
        downside_std = negative_returns.std() * np.sqrt(252) if len(negative_returns) > 0 else 0
        sortino = (mean_return - risk_free_rate) / downside_std if downside_std > 0 else 0
        
        # Max Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Calmar Ratio (年化收益 / Max Drawdown)
        calmar = mean_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        # Win Rate
        win_rate = (returns > 0).sum() / len(returns)
        
        # Best/Worst Day
        best_day = returns.max()
        worst_day = returns.min()
        
        # 数据点
        data_points = len(returns)
        
        return {
            'ticker': ticker,
            'period': period,
            'data_points': data_points,
            'annualized_return': round(mean_return * 100, 2),
            'annualized_volatility': round(std_return * 100, 2),
            'var_95': round(var_95 * 100, 2),
            'var_99': round(var_99 * 100, 2),
            'cvar_95': round(cvar_95 * 100, 2),
            'sharpe_ratio': round(sharpe, 2),
            'sortino_ratio': round(sortino, 2),
            'max_drawdown': round(max_drawdown * 100, 2),
            'calmar_ratio': round(calmar, 2),
            'win_rate': round(win_rate * 100, 2),
            'best_day': round(best_day * 100, 2),
            'worst_day': round(worst_day * 100, 2),
        }
        
    except Exception as e:
        return {'ticker': ticker, 'error': str(e)}

def format_markdown(results):
    """格式化输出Markdown"""
    output = []
    output.append("## 📊 风险指标分析")
    output.append(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    for ticker, metrics in results.items():
        if 'error' in metrics:
            output.append(f"❌ {ticker}: {metrics['error']}")
            continue
        
        output.append(f"### 🎯 {ticker} ({metrics['period']})")
        output.append("")
        
        # 风险收益指标
        output.append("**📈 风险收益指标**")
        output.append("| 指标 | 数值 | 解读 |")
        output.append("|------|------|------|")
        
        sharpe = metrics['sharpe_ratio']
        if sharpe > 1.5:
            sharpe_str = "⭐⭐⭐ 优秀"
        elif sharpe > 1:
            sharpe_str = "⭐⭐ 良好"
        elif sharpe > 0.5:
            sharpe_str = "⭐  一般"
        else:
            sharpe_str = "⚠️ 较差"
        output.append(f"| Sharpe Ratio | {sharpe} | {sharpe_str} |")
        
        sortino = metrics['sortino_ratio']
        output.append(f"| Sortino Ratio | {sortino} | 风险调整后收益 |")
        
        calmar = metrics['calmar_ratio']
        output.append(f"| Calmar Ratio | {calmar:.2f} | 收益/最大回撤 |")
        
        # 波动率
        vol = metrics['annualized_volatility']
        if vol > 30:
            vol_str = "⚠️ 高波动"
        elif vol > 15:
            vol_str = "中等波动"
        else:
            vol_str = "低波动"
        output.append(f"| 年化波动率 | {vol}% | {vol_str} |")
        
        # VaR
        output.append("")
        output.append("**⚠️ 风险指标 (VaR)**")
        output.append("| 指标 | 数值 | 含义 |")
        output.append("|------|------|------|")
        output.append(f"| VaR (95%) | {metrics['var_95']}% | 95%概率日损失不超过此值 |")
        output.append(f"| CVaR (95%) | {metrics['cvar_95']}% | 极端情况平均损失 |")
        output.append(f"| VaR (99%) | {metrics['var_99']}% | 99%概率日损失不超过此值 |")
        
        # 最大回撤
        output.append("")
        output.append("**📉 回撤分析**")
        output.append("| 指标 | 数值 | 含义 |")
        output.append("|------|------|------|")
        mdd = metrics['max_drawdown']
        output.append(f"| 最大回撤 | {mdd}% | 历史最大跌幅 |")
        output.append(f"| 最佳日 | +{metrics['best_day']}% | 单日最大涨幅 |")
        output.append(f"| 最差日 | {metrics['worst_day']}% | 单日最大跌幅 |")
        
        # 胜率
        output.append("")
        output.append(f"**🎲 交易统计**")
        output.append(f"- 数据周期: {metrics['period']} ({metrics['data_points']}个交易日)")
        output.append(f"- 胜率: {metrics['win_rate']}%")
        output.append(f"- 年化收益: {metrics['annualized_return']}%")
        
        output.append("")
    
    return "\n".join(output)

if __name__ == '__main__':
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ['SPY', 'QQQ', 'GLD']
    
    results = {}
    for ticker in tickers:
        results[ticker] = calculate_risk_metrics(ticker)
    
    print(format_markdown(results))
