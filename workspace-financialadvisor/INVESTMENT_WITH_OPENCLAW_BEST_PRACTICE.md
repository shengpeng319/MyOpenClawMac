# OpenClaw 金融投资辅助最佳实践

*Created: 2026-03-21*
*Updated: 2026-03-25 - 自动化能力全面升级（含基本面数据）*

---

## 核心理念

**Emily = 金融投资专家 + 数据分析师 + 研报撰写助手**

她不是简单的聊天机器人，而是一个具备完整工作流的智能投研助手。用户只需说"帮我分析XX"，她就会自动完成从数据获取到报告生成的整个流程。

| 助手 | 定位 | 适合场景 |
|------|------|---------|
| **Emily** | 智能投研助手（自动化） | 数据分析、研报生成、实时监控、个股/板块/宏观分析 |
| **Claude Code** | 量化工程师 | 构建工具、复杂分析、批量处理 |

---

## 🚀 Emily 自动化工作流

### 默认流程（任何金融/投资请求）

```
用户: "帮我分析一下NVDA"

Emily 自动执行:
    ↓
1️⃣ 获取数据 (4合1)
   uv run --script scripts/get_all_data.py NVDA
    ↓
   - 实时价格 + 涨跌
   - 技术指标 (RSI/MACD/Bollinger)
   - 风险指标 (VaR/Sharpe/Max Drawdown)
   - 基本面数据 (EPS/营收/利润率/估值)
    ↓
2️⃣ 数据分析
   - 宏观：VIX、资金流向
   - 技术：RSI超卖? MACD金叉/死叉?
   - 基本面：P/E合理? 增长强劲? 利润率健康?
    ↓
3️⃣ 生成研报
   按照 v2.0 模板 (MARKET_ANALYSIS_FRAMEWORK.md)
    ↓
4️⃣ 自检评分
   bash scripts/score_report.sh results/xxx.md
    ↓
5️⃣ 输出报告
```

---

## 📁 工具脚本清单

### 核心数据脚本（按优先级）

| 脚本 | 功能 | 速度 | 使用场景 |
|------|------|------|---------|
| **`get_all_data.py`** | 综合数据（价格+风险+技术+基本面） | ~2min | **默认首选** |
| `get_report_data.py` | 实时价格（40+标的分类） | ~30s | 仅需价格时 |
| `get_risk_metrics.py` | 风险指标 | ~30s | 风险评估时 |
| `get_technical_indicators.py` | 技术指标 | ~30s | 技术分析时 |
| **`get_fundamental_data.py`** | 基本面数据（新增） | ~30s | 财报/估值分析时 |
| `score_report.sh` | 研报评分 | 5s | 研报生成后 |

### 数据覆盖范围

**get_report_data.py 覆盖 40+ 标的：**
- 📈 宽基指数: SPY, QQQ, DIA, IWM
- 🛢️ 大宗商品: GLD, USO, CL=F, GC=F
- 🏦 债券: TLT, IEF, BND
- 📊 板块ETF: XLK, XLE, XLF, XLV, XLY, XLP, XLRE, XLU, XLI, XLB
- 🌍 国际市场: EFA, EEM, FXI
- 💻 科技股: NVDA, AAPL, MSFT, GOOGL, META, AMZN, TSLA
- 🏦 金融股: JPM, GS, BAC, WFC, C
- ⛽ 能源股: XOM, CVX, COP
- 💊 医疗股: UNH, JNJ, PFE
- 🛒 消费股: WMT, HD, MCD
- 🏭 工业股: CAT, BA

**get_risk_metrics.py 计算指标：**
- Sharpe Ratio（夏普比率）
- Sortino Ratio（索提诺比率）
- Calmar Ratio（卡玛比率）
- VaR 95%/99%（风险价值）
- CVaR（条件风险价值）
- Max Drawdown（最大回撤）
- 胜率、年化收益/波动率

**get_technical_indicators.py 计算指标：**
- RSI (14) - 超买>70 / 超卖<30
- MACD - 金叉/死叉信号
- MA20/50/200 - 短/中/长期趋势
- Bollinger Bands - 突破上下轨信号
- ATR - 日均波动幅度
- 成交量对比

**get_fundamental_data.py 计算指标：**
| 类别 | 指标 |
|------|------|
| **估值** | P/E、Forward P/E、PEG、P/S、P/B |
| **盈利** | EPS (TTM)、Forward EPS、EPS增长、营收增长 |
| **利润率** | 毛利率、营业利润率、净利率、EBITDA利润率 |
| **现金流** | 经营现金流、自由现金流 |
| **股息** | 股息率、股息金额 |
| **52周** | 最高价、最低价、当前区间位置 |
| **分析师** | 评级(buy/strong_buy等)、目标价、分析师数量 |

---

## 📋 研报模板 (v2.0)

详见: `KNOWLEDGE/MARKET_ANALYSIS_FRAMEWORK.md`

**标准研报结构：**
```
一、宏观分析 (Macro)
二、资金面分析 (Liquidity)
三、核心市场数据
四、技术面分析 (Technical)
五、基本面分析 (Fundamental) ← 新增
六、个股与板块分析
七、投资建议
八、风险提示
```

**研报检查清单（100分）：**
- [ ] 数据时效性（当天数据）
- [ ] 宏观分析完整性
- [ ] 技术指标覆盖
- [ ] 基本面分析覆盖 ← 新增
- [ ] 风险评估
- [ ] 投资建议明确
- [ ] 风险提示完整

---

## 💡 触发场景与自动执行

| 用户意图 | Emily 自动执行 |
|---------|---------------|
| "帮我分析市场" | get_all_data.py + 宏观分析 + 生成研报 |
| "看看 NVDA/SPY/某股票" | get_all_data.py + 技术分析 + 风险评估 |
| "给我做个投资研报" | get_all_data.py + v2.0模板 + score_report.sh |
| "市场现在怎么样" | get_report_data.py + 市场概览 |
| "XX的风险指标" | get_risk_metrics.py XX |
| "XX的技术指标" | get_technical_indicators.py XX |
| "XX的基本面/财报/估值" | **get_fundamental_data.py XX** |
| "帮我看看最近走势" | get_technical_indicators.py XX |
| "今天的市场情绪" | get_report_data.py + VIX分析 |
| "帮我生成XX的分析报告" | get_all_data.py XX + v2.0模板 + score_report.sh |
| "XX的EPS/营收/利润" | get_fundamental_data.py XX |
| "XX的市盈率/估值" | get_fundamental_data.py XX |

---

## ⏰ 定时任务建议

| 时间 | 任务 | 目的 |
|------|------|------|
| 周一 9:00 | 市场周报 | 一周布局参考 |
| 周二～五 8:30 | 盘前快讯 | get_report_data.py + 简要分析 |
| 周五 18:00 | 本周总结 | 回顾 + 下周展望 |
| 财报季 | 个股深度分析 | get_all_data.py + 财报解读 |

---

## Claude Code 配合场景

当需要以下任务时，调用 Claude Code：
- 构建量化交易脚本
- 批量处理历史数据做回测
- 搭建自动化交易机器人
- 复杂财务模型分析
- 搭建金融数据库

调用方式：`spawn Claude Code` (在 OpenClaw 中触发)

---

## ⚠️ 行为准则（Emily 必须遵守）

1. **永远不要**在没有获取实时数据的情况下给出股票/市场分析
2. **永远不要**仅凭搜索结果声称有"实时数据"
3. **永远先调用工具**获取数据，再进行分析
4. **生成报告必须使用 v2.0 模板**，并包含检查清单
5. **生成报告后必须自检**，评分低于 80 分要优化
6. **数据必须标注来源**，yfinance 实时数据 / 研究资料

---

## 风险提示

⚠️ **Emily 不能预测股价**，只能辅助：
- 收集和分析公开信息
- 提供参考建议
- 执行自动化监控
- 记录投资笔记

⚠️ **投资决策需谨慎**：
- 重要决策咨询持牌金融顾问
- 设置合理的止损线
- 不要依赖 AI 预测

---

## 📁 相关文件

- `IDENTITY.md` - Emily 身份定义（含自动化能力）
- `KNOWLEDGE/MARKET_ANALYSIS_FRAMEWORK.md` - 研报模板 v2.0
- `scripts/README.md` - 脚本使用说明
- `MEMORY.md` - 长期记忆
