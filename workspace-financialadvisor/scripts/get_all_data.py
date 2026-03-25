#!/usr/bin/env python3
"""
Emily 综合市场数据脚本
一键获取：实时价格 + 风险指标 + 技术指标 + 基本面数据
"""
import sys
import os
import subprocess
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace-financialadvisor")

def run_script(script_path, *args):
    """运行其他脚本并返回输出"""
    cmd = ['uv', 'run', '--script', script_path] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=WORKSPACE)
    return result.stdout + result.stderr

def main():
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ['SPY', 'QQQ', 'NVDA', 'AAPL', 'MSFT', 'GOOGL', 'JPM', 'XOM', 'GLD']
    
    print("=" * 60)
    print("📊 Emily 综合市场数据包")
    print(f"*{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    print("=" * 60)
    print("")
    
    # 1. 实时价格数据
    print("📈 [1/4] 获取实时价格数据...")
    price_output = run_script('scripts/get_report_data.py')
    print(price_output)
    print("")
    
    # 2. 风险指标 (只对主要ETF)
    print("⚠️  [2/4] 计算风险指标...")
    risk_tickers = ['SPY', 'QQQ']
    risk_output = run_script('scripts/get_risk_metrics.py', *risk_tickers)
    print(risk_output)
    print("")
    
    # 3. 技术指标 (所有标的)
    print("🎯 [3/4] 计算技术指标...")
    tech_output = run_script('scripts/get_technical_indicators.py', *tickers)
    print(tech_output)
    print("")
    
    # 4. 基本面数据 (科技巨头)
    print("📊 [4/4] 获取基本面数据...")
    fundamental_tickers = [t for t in tickers if t in ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN', 'TSLA', 'JPM', 'GS', 'XOM', 'CVX']]
    if fundamental_tickers:
        fund_output = run_script('scripts/get_fundamental_data.py', *fundamental_tickers)
        print(fund_output)
    else:
        print("(无科技/金融股，跳过基本面数据)")
    print("")
    
    print("=" * 60)
    print("✅ 数据获取完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
