# 量化交易工具链

*Emily执行量化交易的完整技术栈*

---

## 策略开发平台

### TradingView + Pine Script v6
- 策略编写和回测
- 12个AI Agent协作开发系统（iamrichardD/tradingview）
- 85.71%胜率BTC MACD策略案例

### ssquant（松鼠Quant开源框架）
- 全自动交易智能体框架
- 支持派大星（趋势追踪）、星大派（均值回归/反向）

---

## 回测框架

### 基础回测
- TradingView内置回测
- Backtrader（Python）

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

### Broker API
- **Interactive Brokers (IB)**: 全球覆盖，机构级
- **富途证券**: 港美股
- **老虎证券**: 港美股
- **Alpaca**: 美股，API友好
- **Polygon**: 实时数据+交易

### 核心指标
- 滑点（实际成交价vs报价）
- 手续费（高频交易最大敌人）
- 成交率

---

## AI Agent工具链（TradingView案例）

### Strategic Management Tier
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Fletcher | Context Manager | Agent协调 |
| Seldon | Project Manager | Epic规划 |
| Herbie | Agile Coach | 流程优化 |

### Technical Excellence Specialists
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Vex | Pine Script v6专家 | 语法合规 |
| Maxwell | 量化性能分析师 | 回测验证 |

### Risk & Temporal Integrity Specialists
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Chronos | 前瞻偏差检测 | 时间完整性 |
| Atlas | 动态风险管理 | ATR仓位控制 |

### Market Dynamics Specialists
| Agent | 角色 | 核心能力 |
|-------|------|---------|
| Mercury | 加密市场专家 | 参数优化 |
| Titan | 市场结构分析师 | CHoCH/BOS/IDM检测 |

---

## 完整量化流程

```
感知 → 决策 → 执行 → 复盘 → 进化
```

### Python量化库
```python
# 数据获取
import yfinance as yf      # Yahoo Finance
import pandas as pd
import numpy as np

# 回测
import backtrader as bt

# 机器学习
from sklearn.ensemble import RandomForestClassifier
```
