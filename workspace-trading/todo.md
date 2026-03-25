# OpenClaw 量化交易系统 - 开发记录

> **创建日期**：2026-03-25
> **最后更新**：2026-03-25 19:17
> **状态**：规划阶段完成，等待用户注册 Alpaca

---

## 📋 项目概述

**项目名称**：OpenClaw Trading System (OCTS)
**定位**：量化学习/教学工具
**用户**：Peng Sheng（盛鹏）
**部署环境**：Mac Mini (arm64) + OpenClaw

---

## 📖 讨论过程记录

### 第一阶段：用户需求发现

**时间**：2026-03-25 08:52

**用户原话**：
> "请用autoresearch研究金融投资研报的生成过程有什么不足并改进"

**后续发展**：
用户提出更长远的需求：
> "我想调研一下 OpenClaw 有什么能力可以帮助我赚钱"

### 第二阶段：Emily 调研 + Claire Review

**Emily 的调研结果**：5个赚钱方向
1. 自动交易（用户选定）
2. 内容创作自动化
3. 商业自动化服务
4. 信息聚合订阅
5. 技能/工具开发

**Emily 设计的自动化交易架构**（初版）：
- 6大模块：行情数据、策略引擎、风险管理、执行引擎、持仓管理、通知告警
- 技术栈：yfinance + pandas-ta + Alpaca
- 实施路线：5周

### 第三阶段：Claire Review 发现的问题

**Review 时间**：2026-03-25 16:50

Claire 对初版架构的评审结果：

| 维度 | 评分 | 说明 |
|------|------|------|
| 架构完整性 | 8/10 | 6大模块覆盖核心需求 |
| 技术可行性 | 7/10 | 基本可行，有若干工程难点 |
| 风控设计 | 6/10 | 框架有，但执行层细节不足 |
| 策略设计 | 5/10 | 策略太简单，实战价值有限 |
| 商业可行性 | 4/10 | 有根本性问题 |

**Claire 发现的严重问题**：

#### 问题 1：风控漏洞（5/10）

| 漏洞 | 说明 |
|------|------|
| 跨策略仓位叠加 | 两个策略同时买同一标的，总仓位超限 |
| 流动性风险未定义 | 没有定义高波动标的的过滤规则 |
| 隔夜跳空风险 | 没有防止美股隔夜跳空5-10%的机制 |
| 风控单点故障 | 风控服务宕机时没有 fail-safe 设计 |

**补充风控指标（Claire 建议）**：
- 最大持仓集中度（单标的 ≤ 20% 总资产）
- 日内交易次数上限
- 策略相关性检查
- 资金利用率（现金仓位永远 ≥ 10%）
- 杠杆率动态调整（VIX>25时自动降杠杆）

#### 问题 2：策略太简单（4/10）

| 策略 | 原设计 | 问题 | Claire 建议 |
|------|--------|------|------------|
| RSI 均值回归 | RSI < 30 买入 | 可持续几个月，熊市反复止损 | 加成交量确认 + ATR 止损 |
| MACD 趋势跟踪 | 金叉买入死叉卖出 | 震荡市反复被刷 | 加 ADX > 25 趋势确认 |
| 板块轮动 | 未详细说明 | yfinance 没有板块资金流向数据 | 用 ETF 代理（XLK/XLE/XLF） |

#### 问题 3：遗漏模块

| 遗漏 | 说明 |
|------|------|
| 回测/实盘一致性校验 | 分红/拆股导致数据不连续 |
| 策略信号与执行解耦 | 没有订单队列 |
| 仓位快照与恢复 | 系统崩溃后无法恢复 |
| 性能监控 | 没有延迟/QPS 监控 |
| 策略评级/选择机制 | 没有动态权重 |

#### 问题 4：商业可行性问题（3/10）

> "公开的 RSI/MACD 策略已经被量化基金用过无数遍，散户用这套系统，大概率跑不赢大盘。"

三个优势都没有：
1. 信息优势 ❌
2. 执行优势 ❌
3. 策略优势 ❌

**Claire 建议**：定位为量化学习/教学工具，而非赚钱机器

### 第四阶段：Emily 整合 Claire 反馈

**时间**：2026-03-25 16:59

Emily 整合 Claire 的建议，输出改进版架构：

#### 改进后的 4 层风控体系

```
Layer 1: 事前风控
- 单笔仓位 ≤ 5% 总资产
- 全局同标的合计仓位 ≤ 20% 总资产（跨策略汇总）←【新增】
- ATR 过滤：ATR > 3% 禁止日内交易 ←【新增】

Layer 2: 事中风控
- 动态止损（2% 或 2×ATR）
- 杠杆率动态调整（VIX>25 降杠杆）

Layer 3: 隔夜风控 ←【新增】
- 收盘前 30 分钟强制检查
- 隔夜仓位上限 ≤ 50%

Layer 4: 事后风控
- VaR/CVaR/最大回撤
- 策略表现归因
```

#### 改进后的策略 v2

**RSI 均值回归 v2**：
```python
if RSI < 30 AND Volume < 20日均量50% AND Price > 50日均线 AND ADX < 25:
    买入
    止损：入场价 - 2×ATR
```

**MACD 趋势跟踪 v2**：
```python
if MACD金叉 AND ADX > 25 AND MACD柱状图连续3根放大 AND 成交量 > 1.5×均量:
    买入
    止损：入场价 - 2×ATR
```

**板块轮动 v2**：用 ETF 代理（XLK/SPY、XLE/SPY、XLF/SPY 相对强弱）

### 第五阶段：实施计划 v1.0

**时间**：2026-03-25 17:xx

Emily 创建了完整的实施计划 v1.0：
- 目录结构
- 系统依赖
- Python 包依赖
- API 申请
- 实施路线图（5 周）

### 第六阶段：Claire 审核实施计划 v1.0

**Review 时间**：2026-03-25 19:01

Claire 发现的新问题：

| 问题 | 严重性 | 说明 |
|------|--------|------|
| **Python 3.14 太新** | 🔴 高 | 很多包未支持，建议用 3.12 |
| **alpaca-trade-api 已废弃** | 🔴 高 | 应改用 alpaca-py |
| 目录结构缺失模块 | 🟡 中 | 缺少 notifier/metrics/strategy_router |
| 实施顺序太紧 | 🟡 中 | Phase 1 一周太紧 |
| 缺少集成测试 | 🟡 中 | 只有单元测试 |
| .env 位置不安全 | 🟡 中 | 应放在 ~/.env/ |

**Alpaca 依赖修正**：
```txt
# 修正前
alpaca-trade-api  # ❌ 已废弃

# 修正后
alpaca-py  # ✅ 正确
redis[hiredis]  # ✅ 正确
empyrical  # ✅ 新增（风险指标）
psycopg2-binary  # ✅ 新增（PostgreSQL）
```

### 第七阶段：实施计划 v2.0

**时间**：2026-03-25 19:17

Emily 根据 Claire 的审核建议，更新实施计划到 v2.0。

---

## 📊 最终确定的方案

### 目录结构

```
~/.openclaw/workspace-trading/
├── config/                          # 配置文件
│   ├── broker.yaml                 # 券商API（区分 paper/live）
│   ├── risk_rules.yaml             # 风控规则
│   ├── strategies.yaml             # 策略参数
│   ├── notification.yaml           # 通知设置
│   └── .gitignore
├── core/                           # 核心业务逻辑
│   ├── market_data.py             # 行情数据
│   ├── strategy.py                # 策略基类
│   ├── risk_manager.py            # 4层风控
│   ├── executor.py               # 执行引擎
│   ├── portfolio.py              # 持仓管理
│   ├── metrics.py                # VaR/夏普计算
│   ├── position_state_machine.py  # 持仓状态机
│   └── data_manager.py          # 数据管理
├── services/                       # 服务层
│   ├── order_queue.py           # FIFO 订单队列
│   ├── notifier.py             # 通知服务
│   ├── strategy_router.py       # 策略选择
│   ├── config_validator.py      # 配置校验
│   └── recovery.py             # 崩溃恢复
├── strategies/                    # 策略实现
│   ├── rsi_v2.py              # RSI + 量 + ADX
│   ├── macd_v2.py             # MACD + ADX
│   └── sector_rotation.py      # ETF 板块轮动
├── models/                       # 数据模型
│   ├── order.py
│   ├── position.py
│   └── signal.py
├── services/                    # 服务层
├── data/                        # 数据存储
│   ├── cache/                  # Redis 缓存
│   ├── daily/                  # 日线数据
│   └── logs/trades/            # 交易日志
├── backtest/                   # 回测
│   ├── engine.py
│   ├── validator.py            # Walk-forward
│   └── results/
├── tests/                      # 测试
│   ├── unit/                  # 单元测试
│   └── integration/           # 集成测试
├── scripts/                    # OpenClaw 集成
│   └── trading_cli.py         # Agent 调用接口
├── docs/
├── requirements.txt
└── IMPLEMENTATION_PLAN_v2.md
```

### 系统依赖

| 软件 | 版本 | 用途 | 状态 |
|------|------|------|------|
| Python | 3.12 | 运行环境 | ⚠️ 需设置 venv |
| Redis | 7.0+ | 实时缓存 | ⚠️ 需安装 |
| PostgreSQL | 14+ | 持久化 | ⚠️ Phase 2 再装 |

### Python 依赖

```txt
# 核心
numpy>=1.24.0
pandas>=2.0.0
yfinance>=0.2.0
pandas-ta>=0.3.14
sqlalchemy>=2.0.0
redis[hiredis]>=4.5.0
alpaca-py>=0.5.0        # 【修正】替代废弃的 alpaca-trade-api

# 风控
empyrical>=0.5.0       # 【新增】

# 数据库
psycopg2-binary>=2.9.0  # 【新增】
asyncpg>=0.28.0

# 工具
loguru>=0.7.0
pyyaml>=6.0
python-dotenv>=1.0.0
schedule>=1.2.0

# 回测（可选）
vectorbt>=0.25.0
plotly>=5.15.0

# 测试
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
```

### 实施路线图

| 阶段 | 时间 | 目标 |
|------|------|------|
| Phase 1a | 第1周前半 | 数据层 + Redis/SQLite |
| Phase 1b | 第1周后半 | 订单队列 + Alpaca 连接 |
| Phase 2 | 第2周 | 3个策略 + 3层风控 |
| Phase 3 | 第3周 | Walk-forward + 第4层风控 |
| Phase 4 | 第4周 | Alpaca Live + fail-safe |
| Phase 5 | 第5-8周 | Dashboard + 策略动态权重 |

### 5 级测试体系

| Level | 类型 | 运行频率 |
|-------|------|---------|
| L1 | 单元测试 (pytest) | 每次 commit |
| L2 | 策略回测验证 (vectorbt) | 每周 |
| L3 | 集成测试 | 每次代码变更 |
| L4 | 模拟交易 (Alpaca Paper) | 1周 |
| L5 | 真实交易 (tiny amount) | 持续 |

### 安全设计

- .env 放在 `~/.env/trading.env`（不在 workspace 内）
- API Keys 不提交到 git
- chmod 600 保护配置文件
- 长期考虑 keyring 加密存储

---

## 📌 待办事项

### 你的任务（主机主人）

| 任务 | 状态 | 说明 |
|------|------|------|
| 注册 Alpaca Paper Trading | ⏳ 待完成 | https://app.alpaca.markets/ |
| 获取 API Key + Secret Key | ⏳ 待完成 | 发给 Emily |
| 确认 Python 3.12 可用 | ⏳ 待确认 | `python3.12 --version` |

### Emily 的任务

| 任务 | 状态 | 说明 |
|------|------|------|
| 创建 Python 3.12 venv | ⏳ 待开始 | Phase 1a |
| 安装依赖包 | ⏳ 待开始 | Phase 1a |
| 配置 Alpaca 连接 | ⏳ 待开始 | Phase 1a |
| 实现数据层 | ⏳ 待开始 | Phase 1a |
| 实现订单队列 | ⏳ 待开始 | Phase 1b |
| 实现策略 | ⏳ 待开始 | Phase 2 |
| 实现风控 | ⏳ 待开始 | Phase 2 |

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| `~/.openclaw/workspace-trading/IMPLEMENTATION_PLAN.md` | 实施计划 v1.0 |
| `~/.openclaw/workspace-trading/IMPLEMENTATION_PLAN_v2.md` | 实施计划 v2.0（最新）|
| `~/.openclaw/workspace-trading/todo.md` | 本文件 |

---

## 📝 备注

### 关于 Claire

Claire 是 OpenClaw 中的 researcher agent，负责深度研究和 review。

**Emily-Claire 协作机制**：
- Emily 生成报告 → 发送路径 + 核心观点 + 置信度给 Claire
- Claire 审阅并提供具体反馈
- Claire 评估维度：投资参考价值、准确性、预测验证

### 关键决策记录

1. **定位**：量化学习/教学工具，而非赚钱机器（Claire 建议，用户认可）
2. **券商**：Alpaca（免费、文档好、API 简单）
3. **数据**：yfinance（免费）+ Alpaca Data
4. **Python**：3.12（避免 3.14 兼容性问题）
5. **测试**：5 级测试体系，避免回测/实盘差距

---

*Created by Emily (Financial Advisor Agent)*
*Reviewed by Claire (Researcher Agent)*
*2026-03-25*
