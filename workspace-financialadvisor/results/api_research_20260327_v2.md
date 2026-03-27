# 美股量化交易 API 研究报告（按交易模式分类）

*Emily & Claire 联合研究 | 2026-03-27 | v2.0*

---

⚠️ **免责声明：** 本报告中的定价数据为 2026-03-27 调研结果，实际价格请以各 API 官网为准。

## 📊 按交易模式分类

### 模式 1️⃣：AI Agent 超低频数据获取
**特点：** 定时任务（如每日/每周）、获取数据后 AI 分析、人类决策
**代表：** OpenClaw 定时任务、每日报告生成

| API | 适用度 | 说明 |
|-----|--------|------|
| **yfinance** | ✅✅✅✅✅ | 免费、无限制、最适合定时任务 |
| **Finnhub** | ✅✅✅✅ | 免费 tier 充足，有 Python 封装 |
| **SEC EDGAR** | ✅✅✅✅ | 官方数据，适合基本面分析 |
| **Alpha Vantage** | ✅✅✅ | 免费次数有限，定时任务可能超限 |
| **NewsAPI** | ✅✅✅ | 新闻聚合，适合舆情分析 |

**推荐栈：** yfinance + Finnhub + SEC EDGAR

---

### 模式 2️⃣：低频交易（Swing Trading / 持仓几天到几周）
**特点：** 日线级别信号、每日收盘后分析、隔夜持仓

| API | 适用度 | 说明 |
|-----|--------|------|
| **yfinance** | ✅✅✅✅✅ | 日线数据完全满足 |
| **Alpaca** | ✅✅✅✅ | Commission-free + 完整 API |
| **Interactive Brokers** | ✅✅✅✅ | 全球市场、强大分析工具 |
| **Financial Modeling Prep** | ✅✅✅ | 结构化财报数据 |
| **pandas-ta** | ✅✅✅✅ | 本地技术指标计算 |
| **ta-lib** | ✅✅✅✅✅ | 更全面的技术指标（需安装） |
| **finta** | ✅✅✅ | 另一个流行的技术指标库 |

**推荐栈：** yfinance + Alpaca + pandas-ta（或 ta-lib）

---

### 模式 3️⃣：中频交易（日内交易/每日再平衡）
**特点：** 小时/分钟级别信号、收盘前平仓、日内多次交易

| API | 适用度 | 说明 |
|-----|--------|------|
| **Massive**（原 Polygon.io）| ✅✅✅✅✅ | 毫秒级实时数据，美股 19 家交易所 |
| **Alpaca** | ✅✅✅✅ | 实时行情 + 交易执行 |
| **IEX Cloud** | ✅✅✅✅ | 实时市场数据 |
| **Tradier** | ✅✅✅✅ | 股票 + 期权，实时报价 |
| **Benzinga** | ✅✅✅✅✅ | 美股新闻/情绪数据，**日内交易必备** |

**推荐栈：** Massive(原 Polygon.io) + Alpaca + Benzinga（新闻）

> ⚠️ **重大更新：** Polygon.io 已改名为 **Massive**，官网 massive.io，定价已有变化。

---

### 模式 4️⃣：高频交易/套利（HFT / Statistical Arbitrage）
**特点：** 微秒/毫秒延迟、C++ 或 FPGA、需要专人维护

| API | 适用度 | 说明 |
|-----|--------|------|
| **Rithmic** | ✅✅✅✅✅ | 专业级延迟（**<1μs**），期货为主 |
| **CQG** | ✅✅✅✅ | 专业交易台，高频期权（**1-5ms 延迟**）|
| **Interactive Brokers TWS** | ✅✅✅ | 优化后可达毫秒级，但非最优 |
| **Exegy** | ✅✅✅ | 硬件加速，数据+执行 |
| **Refinitiv** | ✅✅✅ | 机构级，低延迟数据 |

**注意：** 
- 高频交易需要：
  1. 共置托管（colocation）
  2. C++ 或 FPGA 开发
  3. 专用网络连接
  4. 极低延迟的 KP
- 成本：$10,000+/月起步

---

### 模式 5️⃣：半自动化（AI 建议 + 人类决策）
**特点：** AI 分析并给出建议、人类下单、适合机构投资者

| API | 适用度 | 说明 |
|-----|--------|------|
| **yfinance** | ✅✅✅✅✅ | 数据获取，AI 分析 |
| **Bloomberg** | ✅✅✅✅✅ | 专业终端，AI 输入 |
| **FactSet** | ✅✅✅✅ | 机构级数据分析 |
| **Capital IQ** | ✅✅✅✅ | 财务数据平台 |
| **Refinitiv** | ✅✅✅ | 桌面终端 |

**推荐栈：** yfinance + Bloomberg Terminal（人类参考）+ AI 建议输出

---

### 模式 6️⃣：全自动化（无人值守）
**特点：** AI 决策 + 自动执行、7x24 运行、风险管理关键

| Broker | 完整度 | 说明 |
|--------|--------|------|
| **Alpaca** | ✅✅✅✅ | $0 commission，免费实时行情；缺点：新闻数据弱，仅美股，订单执行有时延迟 |
| **Interactive Brokers** | ✅✅✅✅✅ | 功能全面，全球市场；有 $0.005/股交易成本 |
| **Tradier** | ✅✅✅✅ | Python 友好 |
| **TD Ameritrade** | ✅✅✅ | Thinkorswim 生态 |

**推荐栈：** 
- 简单自动化 → **Alpaca**（$0，适合学习）
- 功能全面 → **IBKR**（功能更强，有交易成本）

---

## 🧩 按编程语言推荐

### Python（最适合量化入门）
```
数据：yfinance, Finnhub, pandas-datareader
技术指标：pandas-ta, ta-lib, finta
交易执行：Alpaca-trade-api, ib_insync
回测：backtrader, zipline, vectorbt
```
**适合：** 模式 1、2、3、6

### C++（高频交易）
```
数据：Rithmic, CQG, Exegy
执行：自定义低延迟订单路由
网络：Winsock / epoll / ASIO
```
**适合：** 模式 4（高频套利）

### JavaScript/TypeScript（Web 集成）
```
数据：Finnhub, Alpha Vantage
执行：Alpaca SDK
前端：React + 交易 Dashboard
```
**适合：** 模式 1、2（Web 优先的方案）

---

## 💡 Emily 的场景化推荐

| 你的场景 | 推荐方案 | 预算 |
|----------|----------|------|
| OpenClaw 每日定时分析 | yfinance + Finnhub | $0 |
| 个人投资者 / 学习量化 | yfinance + Alpaca + pandas-ta | $0 |
| 兼职量化（日内交易） | Massive(原 Polygon.io) + Alpaca + Benzinga | $50-200/月 |
| 机构级自动化交易 | IBKR + Massive Pro | $200-500/月 |
| 高频套利（C++） | Rithmic + 共置托管 | $10,000+/月 |

---

## ⚠️ 关键注意事项

1. **延迟 vs 成本：** 实时数据（<1秒）成本高；日线数据（15分钟延迟）免费
2. **API 限制：** 免费 tier 通常有请求频率限制
3. **数据质量：** 免费 API 数据可能有遗漏或错误
4. **合规性：** 自动交易需遵守 SEC/FINRA 规则

---

## 📋 v2.0 更新说明

基于 Claire 审核反馈（78/100）：
1. ✅ Polygon.io → **Massive**（已改名）
2. ✅ 模式 3 增加 **Benzinga**（日内交易新闻必备）
3. ✅ 模式 6 增加 **IBKR 对比**（功能更强，有交易成本）
4. ✅ pandas-ta 补充 **ta-lib** 和 **finta** 替代方案
5. ✅ HFT 部分补充 **CQG 延迟 1-5ms** 指标

---

*本报告基于 2026-03-27 的调研，API 定价和政策可能随时变化。*
