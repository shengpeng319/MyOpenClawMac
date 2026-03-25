# Emily 数据脚本说明

## 📁 脚本列表

| 脚本 | 功能 | 速度 | 使用场景 |
|------|------|------|---------|
| `get_all_data.py` | 综合数据（4合1） | ~2min | **默认首选** |
| `get_report_data.py` | 全市场分类数据 | ~30s | 快速市场概览 |
| `get_risk_metrics.py` | 风险指标计算 | ~30s | VaR/Sharpe/Max Drawdown |
| `get_technical_indicators.py` | 技术指标计算 | ~30s | RSI/MACD/Bollinger |
| `get_fundamental_data.py` | 基本面数据 | ~30s | **EPS/营收/利润率/估值** |
| `score_report.sh` | 研报质量评分 | 5s | 研报生成后自检 |

---

## 🚀 快速使用

### 1. 综合数据获取（推荐）
```bash
# 获取所有数据（价格+风险+技术+基本面）
uv run --script scripts/get_all_data.py NVDA AAPL MSFT

# 默认标的（SPY QQQ NVDA AAPL MSFT GOOGL JPM XOM GLD）
uv run --script scripts/get_all_data.py
```

### 2. 基本面数据（新增）
```bash
# 获取 EPS、营收增长、利润率、估值等
uv run --script scripts/get_fundamental_data.py NVDA AAPL MSFT GOOGL

# 单标的
uv run --script scripts/get_fundamental_data.py NVDA
```

### 3. 实时价格
```bash
# 获取所有分类市场数据（~30秒）
uv run --script scripts/get_report_data.py

# 指定标的
uv run --script scripts/get_report_data.py SPY QQQ NVDA
```

### 4. 技术指标
```bash
# 单标的
uv run --script scripts/get_technical_indicators.py SPY

# 多个标的
uv run --script scripts/get_technical_indicators.py SPY QQQ NVDA AAPL MSFT
```

### 5. 风险指标
```bash
# 默认分析 SPY QQQ
uv run --script scripts/get_risk_metrics.py

# 指定标的
uv run --script scripts/get_risk_metrics.py SPY QQQ NVDA
```

### 6. 研报质量自检
```bash
bash scripts/score_report.sh results/你的研报.md
```

---

## 📊 数据覆盖

### get_report_data.py 覆盖范围

| 类别 | 标的 |
|------|------|
| 📈 宽基指数 | SPY, QQQ, DIA, IWM |
| 🛢️ 大宗商品 | GLD, USO, CL=F, GC=F |
| 🏦 债券 | TLT, IEF, BND |
| 📊 板块ETF | XLK, XLE, XLF, XLV, XLY, XLP, XLRE, XLU, XLI, XLB |
| 🌍 国际市场 | EFA, EEM, FXI |
| 💻 科技股 | NVDA, AAPL, MSFT, GOOGL, META, AMZN, TSLA |
| 🏦 金融股 | JPM, GS, BAC, WFC, C |
| ⛽ 能源股 | XOM, CVX, COP |
| 💊 医疗股 | UNH, JNJ, PFE |
| 🛒 消费股 | WMT, HD, MCD |
| 🏭 工业股 | CAT, BA |

**共 40+ 标的**

---

## 📈 技术指标说明

| 指标 | 含义 | 关键阈值 |
|------|------|---------|
| RSI (14) | 相对强弱指数 | >70 超买, <30 超卖 |
| MACD | 移动平均收敛发散 | 金叉/死叉信号 |
| MA20/50/200 | 移动均线 | 价格 > MA = 牛市 |
| Bollinger Bands | 布林带 | 突破上轨/下轨信号 |
| ATR | 平均真实波幅 | 日均波动幅度 |

---

## ⚠️ 风险指标说明

| 指标 | 含义 | 解读 |
|------|------|------|
| Sharpe Ratio | 夏普比率 | >1 优秀, <0 较差 |
| Sortino Ratio | 索提诺比率 | 风险调整后收益 |
| Calmar Ratio | 卡玛比率 | 收益/最大回撤 |
| VaR (95%) | 风险价值 | 95%概率日损失 |
| Max Drawdown | 最大回撤 | 历史最大跌幅 |

---

## 📊 基本面数据说明（新增）

| 类别 | 指标 | 含义 |
|------|------|------|
| **估值** | P/E | 市盈率，越低越便宜 |
| | Forward P/E | 远期市盈率 |
| | PEG | 市盈率/增长比，<1被低估 |
| | P/S, P/B | 市销率、市净率 |
| **盈利** | EPS | 每股收益 |
| | Forward EPS | 预期每股收益 |
| | EPS增长 | 盈利增长率 |
| | 营收增长 | 收入增长率 |
| **利润率** | 毛利率 | 毛利/收入 |
| | 营业利润率 | 营业利润/收入 |
| | 净利率 | 净利润/收入 |
| | EBITDA利润率 | EBITDA/收入 |
| **现金流** | 经营现金流 | 运营产生的现金 |
| | 自由现金流 | 扣除资本支出后的现金 |
| **股息** | 股息率 | 股息/股价 |
| **52周** | 区间位置 | 当前价格在52周中的位置 |
| **分析师** | 评级 | strong_buy/buy/hold/sell |
| | 目标价 | 分析师平均目标价 |

---

## 🔧 环境要求

- Python 3.10+
- yfinance: `uv add yfinance`

