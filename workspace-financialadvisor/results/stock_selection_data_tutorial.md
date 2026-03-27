# 选股型自动化交易系统 — 数据源完整教程

*Emily & Claire 联合研究 | 2026-03-27*

---

## 📌 教程目标

帮助投资者构建一套完整的**选股型自动化交易系统**数据管道，从数据获取到筛选决策全覆盖。

**核心理念：** 好公司 = 成长性 × 盈利能力 × 财务健康 × 估值合理 × 风险可控

---

## 🏗️ 数据体系总览

```
选股系统数据层
├── 1️⃣ 宏观经济数据
├── 2️⃣ 市场整体数据
├── 3️⃣ 行业/板块数据
├── 4️⃣ 个股基本面数据
├── 5️⃣ 个股财务数据
├── 6️⃣ 估值数据
├── 7️⃣ 风险指标数据
└── 8️⃣ 事件/情绪数据
```

---

## 📊 数据源清单与教程

### 1️⃣ 宏观经济数据

**用途：** 判断市场环境，决定仓位高低

| 数据项 | 说明 | 推荐数据源 | 获取方式 |
|--------|------|-----------|---------|
| GDP 增长率 | 宏观经济健康度 | FRED (Federal Reserve Economic Data) | `fredapi` Python 包 |
| CPI 通货膨胀率 | 货币政策参考 | FRED / BLS | `fredapi` |
| 美联储利率 | 资金成本、流动性 | FRED | `fredapi` |
| 失业率 / NFP | 就业市场 | FRED / BLS | `fredapi` |
| PMI 制造业指数 | 经济活力 | FRED / ISM | `fredapi` |
| 消费者信心指数 | 消费预期 | Conference Board | `fredapi` |
| VIX 恐慌指数 | 市场恐慌程度 | CBOE | yfinance: `^VIX` |

**Python 示例：**
```python
# 安装 fredapi
# pip install fredapi

from fredapi import Fred
fred = Fred(api_key='your_fred_api_key')

# 获取关键宏观数据
gdp = fred.get_series('GDP')  # 美国GDP
cpi = fred.get_series('CPIAUCSL')  # CPI
fed_rate = fred.get_series('FEDFUNDS')  # 联邦基金利率
vix = yf.download('^VIX', period='1mo')  # VIX
```

**注意：** FRED API 需要免费注册获取 API key

---

### 2️⃣ 市场整体数据

**用途：** 判断市场趋势，避免逆势操作

| 数据项 | 说明 | 数据源 | 获取方式 |
|--------|------|--------|---------|
| SPY / QQQ 走势 | 大盘指数 | yfinance | `yf.download('SPY', period='1y')` |
| 市场宽度指标 | 上涨/下跌家数比 | Finviz, TradingView | Web scraping 或 API |
| 期权 Put/Call 比 | 市场情绪 | Cboe | `yfinance` 或 Web scraping |
| 资金流向 | 行业/板块资金流动 | Finviz, Money流向 | Web scraping |
| 恐慌贪婪指数 | 市场情绪综合 | alternative.me | 免费 API |

**Python 示例：**
```python
import yfinance as yf

# 大盘指数数据
spy = yf.download('SPY', period='1y')
qqq = yf.download('QQQ', period='1y')

# 计算市场宽度（可以用 pandas 计算简单指标）
spy['MA20'] = spy['Close'].rolling(20).mean()
spy['RSI'] = ta.rsi(spy['Close'], 14)

# VIX（市场恐慌指数）
vix = yf.download('^VIX', period='1mo')
```

---

### 3️⃣ 行业/板块数据

**用途：** 选择强势行业，在强势行业中选股

| 数据项 | 说明 | 数据源 | 获取方式 |
|--------|------|--------|---------|
| 板块 ETF 涨跌 | 行业轮动 | yfinance (XLK, XLF 等) | sector ETF 系列 |
| 板块相对强弱 | 行业强弱排序 | Finviz | 手动或 scraping |
| 行业平均估值 | 板块 P/E 中位数 | Finviz, FMP | API 或 scraping |
| 板块资金流向 | 资金进出 | Finviz, Money流向 | Web scraping |

**Python 示例：**
```python
import yfinance as yf

# 行业 ETF 系列
sectors = {
    '科技': 'XLK',
    '金融': 'XLF', 
    '医疗': 'XLV',
    '消费': 'XLY',
    '能源': 'XLE',
    '工业': 'XLI'
}

# 获取各行业表现
sector_data = {}
for name, ticker in sectors.items():
    data = yf.download(ticker, period='3mo')
    sector_data[name] = data['Close'].pct_change().sum()
    
# 排序看强弱
sorted_sectors = sorted(sector_data.items(), key=lambda x: x[1], reverse=True)
print("行业强弱排序:", sorted_sectors)
```

---

### 4️⃣ 个股基本面数据

**用途：** 评估公司业务质量、竞争优势、管理层

| 数据项 | 说明 | 数据源 | 获取方式 |
|--------|------|--------|---------|
| 公司概况 | 业务描述、员工数 | Finnhub, FMP | API |
| 主营业务构成 | 收入来源分布 | Finnhub, Seeking Alpha | API 或 scraping |
| 市场份额 | 行业排名 | Statista, 公司年报 | 手动收集 |
| 竞争优势（护城河）| 分析 | 手动研究 | - |
| 管理层质量 | CEO 背景、薪酬 | Finnhub, Proxy statements | API |
| 股东结构 | 机构持仓、大股东 | Finnhub, FMP | API |

**Python 示例：**
```python
import finnhub

finnhub_client = finnhub.Client(api_key='your_finnhub_api_key')

# 公司基本信息
info = finnhub_client.company_profile2(symbol='AAPL', exchange='US')
print("公司名称:", info['name'])
print("行业:", info['finnhubIndustry'])
print("市值:", info['marketCapitalization'])

# 管理层信息
executives = finnhub_client.company_executive(symbol='AAPL')
print("CEO:", executives['executives'][0]['name'])
```

---

### 5️⃣ 个股财务数据

**用途：** 评估盈利能力、成长性、财务健康

| 数据项 | 子指标 | 数据源 | 获取方式 |
|--------|--------|--------|---------|
| **利润表** | 营收、净利、毛利率、营业利润 | yfinance, Finnhub, FMP | `yf.Ticker().financials` |
| **资产负债表** | 总资产、总负债、股东权益 | yfinance, Finnhub | `yf.Ticker().balance_sheet` |
| **现金流量表** | 经营现金流、投资现金流、融资现金流 | yfinance, Finnhub | `yf.Ticker().cashflow` |
| **成长指标** | 营收增长率、净利增长率、EPS增长率 | yfinance, FMP | 计算或 API |
| **盈利质量** | ROE、ROA、ROIC、净利润率 | yfinance | 公式计算 |

**Python 示例：**
```python
import yfinance as yf
import pandas as pd

ticker = yf.Ticker('AAPL')

# 利润表
income_stmt = ticker.income_stmt
print("营收 (3年):", income_stmt.loc['Total Revenue'])
print("净利 (3年):", income_stmt.loc['Net Income'])

# 资产负债表
balance = ticker.balance_sheet
print("总资产:", balance.loc['Total Assets'])
print("总负债:", balance.loc['Total Liabilities'])

# 现金流量表
cashflow = ticker.cashflow
print("经营现金流:", cashflow.loc['Operating Cash Flow'])
print("自由现金流:", cashflow.loc['Free Cash Flow'])

# 计算关键指标
revenue_growth = income_stmt.loc['Total Revenue'].pct_change() * 100
net_margin = income_stmt.loc['Net Income'] / income_stmt.loc['Total Revenue']
print("营收增长率:", revenue_growth)
print("净利润率:", net_margin)
```

---

### 6️⃣ 估值数据

**用途：** 判断股价是否被低估/高估

| 数据项 | 说明 | 数据源 | 获取方式 |
|--------|------|--------|---------|
| P/E (TTM) | 市盈率 | yfinance, Finnhub | `yf.Ticker().info['trailingPE']` |
| Forward P/E | 预期市盈率 | yfinance, Finnhub | `yf.Ticker().info['forwardPE']` |
| PEG | 市盈率相对增长比 | yfinance, FMP | 手动计算 (P/E / EPS增长率) |
| P/B | 市净率 | yfinance | `yf.Ticker().info['priceToBook']` |
| P/S | 市销率 | yfinance | `yf.Ticker().info['priceToSalesTrailing12Months']` |
| EV/EBITDA | 企业价值倍数 | yfinance, Finnhub | 手动计算 |
| DCF | 现金流折现 | 需自己建模 | 复杂计算 |

**Python 示例：**
```python
import yfinance as yf

stock = yf.Ticker('AAPL')
info = stock.info

# 估值指标
print("P/E (TTM):", info.get('trailingPE'))
print("Forward P/E:", info.get('forwardPE'))
print("P/B:", info.get('priceToBook'))
print("P/S:", info.get('priceToSalesTrailing12Months'))
print("PEG:", info.get('pegRatio'))
print("股息率:", info.get('dividendYield'))

# 获取分析师目标价
print("分析师目标价:", info.get('targetMeanPrice'))
print("分析师评级:", info.get('recommendationKey'))
```

---

### 7️⃣ 风险指标数据

**用途：** 控制下行风险，避免踩雷

| 数据项 | 说明 | 计算/数据源 | 获取方式 |
|--------|------|------------|---------|
| Beta | 相对大盘波动 | 历史数据计算 | `yf.Ticker().info['beta']` |
| Volatility (年化) | 股价波动率 | `stock['Close'].pct_change().std() * sqrt(252)` | 计算 |
| VaR (Value at Risk) | 最大单日损失概率 | 历史模拟法 | 公式计算 |
| Max Drawdown | 最大回撤 | 历史数据 | 公式计算 |
| Sharpe Ratio | 风险调整收益 | `(收益率 - 无风险利率) / 波动率` | 计算 |
| Sortino Ratio | 下行风险调整收益 | 公式计算 | 计算 |
| Debt-to-Equity | 资产负债率 | 资产负债表 | `yf.Ticker().info['debtToEquity']` |
| Current Ratio | 流动比率 | 资产负债 | 手动计算 |

**Python 示例：**
```python
import yfinance as yf
import numpy as np

stock = yf.Ticker('AAPL')
info = stock.info

# 获取历史数据
hist = stock.history(period='2y')

# Beta (市场敏感度)
beta = info.get('beta')
print("Beta:", beta)

# 年化波动率
daily_returns = hist['Close'].pct_change().dropna()
annual_vol = daily_returns.std() * np.sqrt(252)
print("年化波动率:", f"{annual_vol:.2%}")

# VaR (95% confidence, 1-day)
var_95 = daily_returns.quantile(0.05)
print("VaR (95%, 1天):", f"{var_95:.2%}")

# 最大回撤
cummax = hist['Close'].cummax()
drawdown = (hist['Close'] - cummax) / cummax
max_dd = drawdown.min()
print("最大回撤:", f"{max_dd:.2%}")

# Sharpe Ratio (假设无风险利率 4%)
risk_free = 0.04
sharpe = (daily_returns.mean() * 252 - risk_free) / annual_vol
print("Sharpe Ratio:", f"{sharpe:.2f}")
```

---

### 8️⃣ 事件/情绪数据

**用途：** 把握买卖时机，避开危险时期

| 数据项 | 说明 | 数据源 | 获取方式 |
|--------|------|--------|---------|
| 财报发布日期 | 业绩公告 | Finnhub, Nasdaq | `finnhub_client.ipo_calendar()` 或 `yf.Ticker().calendar` |
| 分析师评级变化 | 机构观点 | Finnhub, Zacks | API |
| 内部交易 | 高管买卖 | Finnhub, SEC EDGAR | API |
| 新闻情绪 | 新闻正负面 | Finnhub News API | API |
| 股票回购 | 回购计划/完成 | SEC EDGAR, 公司公告 | 手动收集 |

**Python 示例：**
```python
import finnhub

finnhub_client = finnhub.Client(api_key='your_finnhub_api_key')

# 近期新闻
news = finnhub_client.company_news('AAPL', _from='2026-03-01', to='2026-03-27')
for article in news[:5]:
    print(f"标题: {article['headline']}")
    print(f"情绪: {article.get('sentiment', 'N/A')}")
    print()

# 财报日期
earnings = finnhub_client.company_earnings('AAPL', limit=5)
for e in earnings:
    print(f"财报日期: {e['period']}, EPS 实际: {e['epsActual']}, EPS 预期: {e['epsEstimate']}")
```

---

## 🛠️ 数据获取工具栈推荐

### 免费工具（适合个人投资者）

| 工具 | 用途 | 费用 | 特点 |
|------|------|------|------|
| **yfinance** | 价格、财务、新闻 | 免费 | Python首选，数据全面 |
| **FRED API** | 宏观经济数据 | 免费 | 美联储数据，权威 |
| **Finnhub** | 基本面、新闻、估值 | 免费 tier | 实时新闻，API友好 |
| **pandas-ta** | 技术指标计算 | 免费 | 本地计算，不依赖外部 |
| **Seeking Alpha** | 财报、分析师观点 | 免费 | 质量高，需手动 |
| **SEC EDGAR** | 官方文件 | 免费 | 最权威，但难解析 |

### 付费工具（适合专业投资者）

| 工具 | 用途 | 费用 | 特点 |
|------|------|------|------|
| **Financial Modeling Prep (FMP)** | 财务数据、估值 | $29/月起 | 财务报表最完整 |
| **Alpha Vantage** | 全品类金融数据 | 免费 tier / $49.9/月 | 数据全面 |
| **Polygon.io** | 实时市场数据 | $200/月起 | 毫秒级延迟 |
| **Bloomberg** | 全终端 | $25,000/年 | 专业级，机构用 |
| **FactSet** | 财务分析 | 昂贵 | 机构级 |

---

## 📐 选股筛选模型设计

### 评分体系（示例）

```
综合评分 = 成长性得分 × 30% + 盈利质量得分 × 25% + 估值得分 × 25% + 风险得分 × 20%
```

| 维度 | 指标 | 权重 | 筛选标准 |
|------|------|------|---------|
| **成长性** | 营收增长率（3年） | 15% | > 10% 得高分 |
| | EPS增长率（3年） | 15% | > 10% 得高分 |
| **盈利质量** | ROE | 15% | > 15% 得高分 |
| | 净利润率趋势 | 10% | 稳定或上升 |
| **估值** | PEG | 20% | < 1 得高分 |
| | P/E vs 行业平均 | 15% | 低于行业得高分 |
| | P/B | 10% | < 3 得高分 |
| **风险** | Beta | 10% | 0.8-1.2 中等 |
| | Debt/Equity | 10% | < 50% 得高分 |

### 筛选流程

```
Step 1: 初筛（估值+财务健康）
├── P/E < 30
├── P/B < 5
├── Debt/Equity < 100%
└── 净利润 > 0

Step 2: 成长性筛选
├── 营收3年CAGR > 10%
├── EPS3年CAGR > 10%
└── 最近季度营收正增长

Step 3: 盈利质量筛选
├── ROE > 10%
├── 净利润率 > 5%
└── 毛利率稳定或上升

Step 4: 综合评分排序
├── 计算综合得分
└── 得分 > 70 分进入候选池

Step 5: 人工复审
├── 业务质量判断
├── 竞争优势分析
└── 管理层评估
```

---

## 🔄 完整数据管道示例

```python
import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(ticker):
    """获取单只股票完整数据"""
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # 1. 基本信息
    data = {
        'ticker': ticker,
        'name': info.get('shortName'),
        'sector': info.get('sector'),
        'market_cap': info.get('marketCap'),
    }
    
    # 2. 估值指标
    data.update({
        'pe': info.get('trailingPE'),
        'forward_pe': info.get('forwardPE'),
        'pb': info.get('priceToBook'),
        'ps': info.get('priceToSalesTrailing12Months'),
        'peg': info.get('pegRatio'),
        'dividend_yield': info.get('dividendYield'),
    })
    
    # 3. 成长性指标（计算）
    financials = stock.financials
    if not financials.empty:
        revenue = financials.loc['Total Revenue']
        if len(revenue) >= 3:
            data['revenue_3yr_cagr'] = ((revenue.iloc[0] / revenue.iloc[-1]) ** (1/3) - 1) * 100
    
    # 4. 风险指标
    data['beta'] = info.get('beta')
    data['debt_to_equity'] = info.get('debtToEquity')
    
    return pd.Series(data)

# 对多只股票进行筛选
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA']

results = []
for ticker in tickers:
    try:
        data = get_stock_data(ticker)
        results.append(data)
    except Exception as e:
        print(f"{ticker} 获取失败: {e}")

# 汇总
df = pd.DataFrame(results)
print(df)
```

---

## ⚠️ 注意事项

1. **数据延迟：** yfinance 免费数据有 15 分钟延迟
2. **财务数据更新：** 季度财报通常滞后 1-2 周
3. **API 限制：** 免费 API 有请求频率限制
4. **数据验证：** 免费数据可能有错误，重要决策前请核实
5. **模型风险：** 历史数据不代表未来表现

---

## 📋 待 Claire 补充验证

1. 各数据源的最新 pricing 和限制
2. 中文社区的实际使用反馈
3. 是否有其他推荐的免费/付费数据源
4. FMP vs Finnhub 财务数据完整性对比

---

*本教程基于 2026-03-27 的调研，数据源和政策可能随时变化。建议注册免费 API key 先试用。*
