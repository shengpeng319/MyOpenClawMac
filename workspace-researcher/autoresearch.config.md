# Autoresearch Config: 美股量化交易 API 研究

## 任务目标
研究适合美股量化交易的 API，整理成最终推荐清单

## 研究问题
业界有哪些 API 适合做美股的量化自动化交易？

## 验证维度
1. **数据覆盖**：行情、技术指标、基本面、新闻
2. **免费额度**：是否有免费层、限制多少
3. **API 限制**：频率限制、延迟、可靠性
4. **易用性**：文档质量、Python 封装、执行门槛

## 初始候选 API（待验证）
- 行情：yfinance, Finnhub, Polygon.io, Alpha Vantage
- 技术指标：pandas-ta, Alpha Vantage
- 基本面：SEC EDGAR, yfinance
- 新闻：NewsAPI, Benzinga, Finnhub News
- 交易执行：Alpaca, Interactive Brokers, TD Ameritrade

## 评分标准（待设定）
- 实用性
- 成本效率
- 数据质量

## 成功标准
整理出 3-5 个核心 API 推荐组合，覆盖行情+基本面+新闻+执行

