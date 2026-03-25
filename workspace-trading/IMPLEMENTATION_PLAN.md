# 🚀 OpenClaw 量化交易系统 - 实施计划 v1.0

> **状态**：规划阶段（尚未开始实施）
> **创建日期**：2026-03-25
> **目标**：构建完整的自动化交易系统

---

## 1️⃣ 项目定位

| 项目 | 说明 |
|------|------|
| **项目名称** | OpenClaw Trading System (OCTS) |
| **定位** | 量化学习/教学工具，非专业交易系统 |
| **用户** | Peng Sheng（主机所有者）|
| **部署位置** | Mac Mini (arm64) + OpenClaw |

---

## 2️⃣ 目录结构

```
~/.openclaw/workspace-trading/
│
├── config/                          # 配置文件（敏感信息）
│   ├── broker.yaml                  # 券商API凭证
│   ├── risk_rules.yaml              # 风控规则
│   ├── strategies.yaml              # 策略参数
│   ├── notification.yaml            # 通知设置
│   └── .gitignore                   # 忽略敏感文件
│
├── core/                            # 核心模块
│   ├── __init__.py
│   ├── market_data.py               # 行情数据（Redis + yfinance）
│   ├── strategy.py                  # 策略引擎
│   ├── risk_manager.py              # 风险管理（4层风控）
│   ├── executor.py                  # 执行引擎（订单队列）
│   ├── portfolio.py                 # 持仓管理
│   ├── notification.py              # 通知模块
│   └── data_manager.py              # 数据管理层
│
├── strategies/                      # 策略实现
│   ├── __init__.py
│   ├── rsi_v2.py                    # RSI均值回归 v2
│   ├── macd_v2.py                   # MACD趋势跟踪 v2
│   └── sector_rotation.py           # ETF板块轮动
│
├── models/                          # 数据模型
│   ├── __init__.py
│   ├── order.py                     # 订单模型
│   ├── position.py                   # 持仓模型
│   └── signal.py                    # 信号模型
│
├── services/                        # 服务层
│   ├── __init__.py
│   ├── order_queue.py               # FIFO订单队列
│   ├── position_state_machine.py    # 持仓状态机
│   └── recovery.py                  # 崩溃恢复服务
│
├── data/                            # 数据存储
│   ├── cache/                       # Redis缓存（实时行情）
│   ├── daily/                       # 日线历史数据
│   ├── minute/                      # 分钟数据
│   └── logs/                        # 交易日志
│       ├── trades/                  # 成交记录
│       ├── errors/                  # 错误日志
│       └── daily/                   # 每日报告
│
├── backtest/                        # 回测模块
│   ├── engine.py                    # 回测引擎
│   ├── validator.py                 # Walk-forward验证
│   └── results/                    # 回测结果
│
├── scripts/                         # OpenClaw集成脚本
│   ├── get_all_data.py             # 获取所有数据（Emily用）
│   ├── run_strategy.py             # 运行策略
│   ├── check_positions.py          # 检查持仓
│   ├── daily_report.py             # 生成日报
│   └── emergency_close.py          # 紧急平仓
│
├── tests/                           # 单元测试
│   ├── test_strategy.py
│   ├── test_risk.py
│   ├── test_executor.py
│   └── test_order_queue.py
│
├── docs/                            # 文档
│   ├── ARCHITECTURE.md             # 架构文档
│   ├── API.md                     # API文档
│   └── USER_GUIDE.md              # 用户指南
│
├── README.md                        # 项目说明
├── requirements.txt                 # Python依赖
├── .env.example                    # 环境变量示例
└── IMPLEMENTATION_PLAN.md           # 本计划
```

---

## 3️⃣ 系统依赖

### 3.1 硬件要求

| 项目 | 要求 | 你的设备状态 |
|------|------|-------------|
| CPU | arm64 / x86_64 | ✅ Apple M1/M2/M3 (arm64) |
| 内存 | ≥ 8GB | ✅ Mac Mini |
| 磁盘 | ≥ 10GB 可用 | ✅ 足够 |
| 网络 | 稳定互联网 | ✅ 需要 |

### 3.2 操作系统

| 项目 | 要求 | 你的系统状态 |
|------|------|-------------|
| macOS | ≥ 12.0 | ✅ Darwin 25.3.0 |
| Linux | Ubuntu 20.04+ | N/A |
| Python | ≥ 3.10 | ✅ 3.14.3 |

### 3.3 系统级软件

| 软件 | 版本 | 用途 | 状态 | 安装方式 |
|------|------|------|------|---------|
| **Python** | 3.10+ | 运行环境 | ✅ 已有 | - |
| **uv** | 最新 | 包管理器 | ✅ 已有 | - |
| **Redis** | 7.0+ | 实时行情缓存 | ⚠️ 需安装 | `brew install redis` |
| **PostgreSQL** | 14+ | 持久化存储 | ⚠️ 需安装 | `brew install postgresql` |

> **说明**：Phase 1 可以先用 SQLite 代替 PostgreSQL，Phase 2 再切换

---

## 4️⃣ Python 依赖包

### 4.1 核心依赖

| 包名 | 版本 | 用途 | 已安装 |
|------|------|------|--------|
| `numpy` | - | 数值计算 | ✅ 2.4.3 |
| `pandas` | - | 数据处理 | ✅ 3.0.1 |
| `yfinance` | - | Yahoo Finance行情 | ✅ 1.2.0 |
| `pandas-ta` | - | 技术指标 | ❌ 需安装 |
| `sqlalchemy` | - | 数据库ORM | ❌ 需安装 |
| `redis` | - | Redis客户端 | ❌ 需安装 |
| `loguru` | - | 日志系统 | ❌ 需安装 |
| `pyyaml` | - | 配置文件 | ❌ 需安装 |
| `python-dotenv` | - | 环境变量 | ❌ 需安装 |
| `schedule` | - | 定时任务 | ❌ 需安装 |

### 4.2 券商API

| 包名 | 版本 | 用途 | 已安装 |
|------|------|------|--------|
| `alpaca-trade-api` | - | Alpaca券商接口 | ❌ 需安装 |

### 4.3 可选依赖

| 包名 | 版本 | 用途 | 是否必需 |
|------|------|------|---------|
| `vectorbt` | - | 快速回测 | 推荐 |
| `plotly` | - | 数据可视化 | 推荐 |
| `ta` | - | 技术指标（备选） | 可选 |
| `apscheduler` | - | 高级定时任务 | 可选 |

### 4.4 完整 requirements.txt

```
# Core Data
numpy>=1.24.0
pandas>=2.0.0
yfinance>=0.2.0

# Technical Analysis
pandas-ta>=0.3.14

# Database & Cache
sqlalchemy>=2.0.0
redis>=4.5.0

# Alpaca Broker API
alpaca-trade-api>=0.5.0

# Utilities
loguru>=0.7.0
pyyaml>=6.0
python-dotenv>=1.0.0
schedule>=1.2.0

# Optional - for backtesting and visualization
vectorbt>=0.25.0
plotly>=5.15.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

---

## 5️⃣ 代码实现方案

### 5.1 编程语言

| 语言 | 选择 | 理由 |
|------|------|------|
| **Python** | ✅ 主语言 | yfinance/pandas/ta-lib/ Alpaca 都用Python，生态最成熟 |

### 5.2 代码风格

| 项目 | 选择 | 理由 |
|------|------|------|
| **类型提示** | 使用 | 提高代码可读性，减少bug |
| **代码格式化** | Black | 统一风格 |
| **类型检查** | mypy | 静态类型检查 |
| **测试** | pytest | 单元测试框架 |

### 5.3 项目管理

| 项目 | 选择 | 理由 |
|------|------|------|
| **包管理** | uv | 你的环境已安装，快速 |
| **虚拟环境** | venv | 隔离依赖 |
| **配置管理** | YAML + .env | 敏感信息分离 |

---

## 6️⃣ API 平台申请

### 6.1 券商API（必须）

| 券商 | 费用 | 特点 | 申请难度 | 推荐度 |
|------|------|------|---------|--------|
| **Alpaca** | 免费(Paper)<br>Live: $0 commission | 最易集成<br>文档完善<br>支持美股+加密 | ⭐ 低<br>（邮箱即可）| ⭐⭐⭐⭐⭐ |
| Interactive Brokers | $0（最低佣金） | 多市场<br>API复杂 | ⭐⭐⭐⭐ 中 | ⭐⭐⭐ |
| TD Ameritrade | 免费 | 期权强<br>API限制多 | ⭐⭐⭐ 中 | ⭐⭐⭐ |

**推荐**：先用 **Alpaca Paper Trading**，熟悉后再开 Live 账户

### 6.2 数据源（可选）

| 数据源 | 费用 | 用途 | 推荐度 |
|--------|------|------|--------|
| **Yahoo Finance (yfinance)** | 免费 | 历史数据+实时（15min延迟）| ⭐⭐⭐⭐⭐ |
| **Alpaca Data** | 免费(含Paper) | 实时行情（需订阅）| ⭐⭐⭐⭐ |
| **Polygon.io** | $9/月 起 | 专业级实时数据 | ⭐⭐⭐ |

> **建议**：Phase 1 用 yfinance + Alpaca Data 足够

---

## 7️⃣ 需要订阅的服务

### 7.1 必须项

| 服务 | 费用 | 用途 | 备注 |
|------|------|------|------|
| **Alpaca Paper Trading** | 免费 | 模拟交易 | 申请即有 |
| **Alpaca Live Trading** | 免费($0commission) | 真实交易 | 可选，需要SSN |

### 7.2 可选项

| 服务 | 费用 | 用途 | 建议 |
|------|------|------|------|
| **Polygon.io Starter** | $9/月 | 实时数据 | Phase 2 再考虑 |
| **TradingView Pro** | $14.95/月 | 图表分析 | 可选 |
| **QuantConnect** | 免费 | 回测验证 | 可选 |

### 7.3 总体费用预估

| 阶段 | 月费用 | 说明 |
|------|--------|------|
| Phase 1-2 (学习期) | **$0** | 全用免费方案 |
| Phase 3+ (真实交易) | **$0-$15** | Alpaca免费，Polygon可选 |

---

## 8️⃣ 实施路线图

### Phase 1: 基础架构（第1周）

**目标**：跑通数据层 + 订单队列

```
任务清单：
□ 安装 Python 依赖包
□ 申请 Alpaca Paper Trading 账号
□ 配置 config/broker.yaml
□ 实现 Redis 数据缓存（可用 SQLite 替代）
□ 实现 core/market_data.py（行情获取）
□ 实现 models/order.py（订单模型）
□ 实现 services/order_queue.py（FIFO队列）
□ 实现 core/executor.py（执行引擎）
□ 集成到 OpenClaw（scripts/）
□ 测试：获取 SPY 实时数据
```

### Phase 2: 策略开发（第2周）

**目标**：实现 3 个策略 v2

```
任务清单：
□ 实现 core/strategy.py（策略基类）
□ 实现 strategies/rsi_v2.py（RSI + 量 + ADX）
□ 实现 strategies/macd_v2.py（MACD + ADX）
□ 实现 strategies/sector_rotation.py（ETF相对强弱）
□ 实现 core/risk_manager.py（4层风控）
□ 实现 Walk-forward 回测验证
□ 测试：历史数据回测
```

### Phase 3: 执行优化（第3周）

**目标**：连接真实券商

```
任务清单：
□ 切换到 Alpaca Live API
□ 实现 fail-safe 风控机制
□ 实现 core/portfolio.py（持仓管理）
□ 实现 services/recovery.py（崩溃恢复）
□ 实现每日报告生成
□ 记录每笔成交日志
```

### Phase 4: 监控告警（第4周）

**目标**：完整监控体系

```
任务清单：
□ 实现 core/notification.py（飞书通知）
□ 配置定时任务（每日报告）
□ 添加性能监控（延迟/QPS）
□ 实现策略动态权重
□ 添加 Prometheus metrics（可选）
```

### Phase 5: 模拟实盘验证（额外2-3个月）

**目标**：验证策略可靠性

```
任务清单：
□ 用 Alpaca Live 跑模拟资金
□ 记录每一笔成交
□ 对比回测 vs 实盘差异
□ 验证模型可靠性
□ 调整策略参数
```

---

## 9️⃣ 你需要做的事情（主人任务）

### 你的角色：提供资源 + 授权 + 审批

| 任务 | 具体事项 | 耗时 | 你的操作 |
|------|---------|------|---------|
| **1. 申请 Alpaca 账号** | 注册 Paper Trading | 5分钟 | 你在网页完成 |
| **2. 获取 API Keys** | 从 Alpaca Dashboard 复制 | 2分钟 | 你在网页完成 |
| **3. 安装 Redis** | `brew install redis` | 2分钟 | 给我命令我执行 |
| **4. 安装 PostgreSQL** | `brew install postgresql` | 2分钟 | 给我命令我执行 |
| **5. 审批 .env 配置** | 确认 API Keys 写入配置 | 1分钟 | 你审批 |
| **6. 测试授权** | 确认可以下单（Paper） | 1分钟 | 你确认 |

### 快速开始清单

```
□ Step 1: 去 https://app.alpaca.markets/ 注册 Paper Trading 账号
□ Step 2: 登录后在 Dashboard 获取 API Key 和 Secret Key
□ Step 3: 把这两个 key 发给我
□ Step 4: 我来完成剩下的所有配置和代码
```

---

## 🔟 安全注意事项

### 敏感信息处理

| 信息 | 存储位置 | 保护方式 |
|------|---------|---------|
| API Keys | `~/.openclaw/workspace-trading/config/broker.yaml` | 不提交到 git |
| 密码 | `.env` 文件 | 不提交到 git |
| 交易记录 | 本地数据库 | 定期备份 |

### .gitignore 内容

```gitignore
# Sensitive files
config/broker.yaml
.env
*.pem
*.key

# Data files
data/
*.db
*.sqlite

# Logs
logs/
*.log

# Python
__pycache__/
*.pyc
.venv/
```

---

## 📋 实施检查清单

### 实施前（你的任务）

- [ ] 申请 Alpaca Paper Trading 账号
- [ ] 获取 API Key 和 Secret Key
- [ ] 安装 Homebrew（如果需要）
- [ ] 确认网络环境稳定

### Phase 1 交付物

- [ ] Python 依赖安装完成
- [ ] Alpaca Paper Trading 连接成功
- [ ] 可以获取 SPY 实时数据
- [ ] 订单队列可以正常工作
- [ ] 可以发送测试订单（Paper）

### Phase 2 交付物

- [ ] 3 个策略全部实现
- [ ] 风控模块实现
- [ ] Walk-forward 回测完成
- [ ] 回测结果记录

---

## ❓ 常见问题

**Q: 需要多少钱开始？**
A: $0。Alpaca Paper Trading 免费，yfinance 免费。

**Q: 需要美国身份证吗？**
A: Alpaca Paper Trading 注册只需要邮箱。Live 账户需要 SSN。

**Q: 我的数据会被用于什么？**
A: 仅用于你自己的交易系统，不会上传到任何第三方（除 Alpaca）。

**Q: 系统会自动下单吗？**
A: 需要你授权。可以设置为"自动执行"或"信号提醒+手动确认"。

**Q: 亏损了怎么办？**
A: Phase 1-2 都是 Paper Trading，不会亏真实资金。Phase 3+ 请谨慎。

---

*本计划基于 2026-03-25 的 Claude Review 改进*
*如需修改，请联系 Emily*
