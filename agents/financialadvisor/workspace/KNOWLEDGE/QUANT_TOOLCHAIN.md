# 量化交易工具链

*Emily执行量化交易的完整技术栈*

---

## 策略开发平台

### TradingView + Pine Script v6
- 策略编写和回测
- 12个AI Agent协作开发系统
- GitHub: iamrichardD/tradingview

### ssquant（松鼠Quant开源框架）
- 全自动交易智能体框架
- 支持派大星（趋势追踪）、星大派（均值回归/反向）

---

## 回测框架

### 基础回测
- TradingView内置回测
- Backtrader（Pytho）

### 高级分析
- **Maxwell Agent**: 量化性能分析，回测验证、统计分析
- **Chronos Agent**: 前瞻偏差检测，确保时间完整性

### 回测质量指标
| 指标 | 说明 |
|------|------|
| 夏普比率 | 风险调整后收益（>1.5为好） |
| 最大回撤 | 历史最大亏损（<20%为可接受） |
| 胜率 | 盈利交易占比 |
| Profit Factor | 盈利总额/亏损总额（>1.5为好） |
| 持仓时间 | 平均持仓周期 |

---

## 订单执行

### Broker API对接
- **Interactive Brokers (IB)**: 机构级，覆盖全球
- **富途证券**: 港美股
- **老虎证券**: 港美股
- **Alpaca**: 美股，API友好，免费
- **Polygon**: 实时数据+交易

### 核心指标
- 滑点（实际成交价vs报价）
- 手续费（高频交易最大敌人）
- 成交率

---

## AI Agent工具链（TradingView案例）

### Strategic Management Tier（战略管理层）
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Fletcher | Context Manager | 仓库状态分析、Agent协调 |
| Seldon | Project Manager | Epic规划、资源分配 |
| Herbie | Agile Coach | 流程优化、质量把控 |

### Technical Excellence Specialists（技术专家层）
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Vex | Pine Script v6专家 | 语法合规、优化 |
| Maxwell | 量化性能分析师 | 回测验证、统计分析 |

### Risk & Temporal Integrity Specialists（风险与时间完整性层）
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Chronos | 前瞻偏差检测 | 时间完整性、历史准确性 |
| Atlas | 动态风险管理 | ATR仓位控制、多层风控 |

### Market Dynamics Specialists（市场动态层）
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Mercury | 加密市场专家 | BTC参数优化、波动模式 |
| Titan | 市场结构分析师 | CHoCH/BOS/IDM检测 |

---

## 执行流程

### 完整量化流程
```
感知 → 决策 → 执行 → 复盘 → 进化
```

**感知（步骤1）**
- 每日自动获取行情数据
- 区分交易日vs非交易日
- 交易日按仓位配置购买标的

**决策（步骤2-3）**
- 因子加工：运行UVRun + RFactor脚本
- 评分卡：建立选股标准

**执行（步骤4）**
- Opt函数做参数优化
- 回测验证策略有效性
- 实盘下单

**复盘（步骤5）**
- AI自动分析亏损原因
- 找出需要调整的参数
- 持续迭代优化

---

## Python量化库

```python
# 数据获取
import yfinance as yf      # Yahoo Finance免费数据
import akshare as ak       # A股数据
import baostock as bs      # A股基本面

# 分析
import pandas as pd
import numpy as np
from scipy import stats

# 回测
import backtrader as bt

# 机器学习
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
```

---

## 相关页面

- [[MARKET_ANALYSIS_FRAMEWORK]] — 市场分析框架
- [[RISK_MANAGEMENT]] — 风险管理
- [[BROKER_INTEGRATION]] — Broker对接详解
