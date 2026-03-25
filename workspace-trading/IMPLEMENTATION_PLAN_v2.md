# 🚀 OpenClaw 量化交易系统 - 实施计划 v2.0

> **状态**：规划阶段（已采纳 Claire Review 建议）
> **创建日期**：2026-03-25
> **v1.0 → v2.0 变更**：采纳 researcher (Claire) review 建议
> **目标**：构建完整的自动化交易系统

---

## 0️⃣ Claire Review 核心改进 (v1.0 → v2.0)

| 问题 | v1.0 | v2.0 改进 |
|------|-------|----------|
| Python 版本 | 3.14 (太新) | **3.12 venv** + 3.14 兼容性警告 |
| Alpaca 库 | alpaca-trade-api (废弃) | **alpaca-py** |
| 依赖包名 | redis, 缺少 empyrical | **redis[hiredis]**, **empyrical**, psycopg2-binary |
| 目录结构 | 缺少部分模块 | **+notifier/metrics/strategy_router/config_validator** |
| 实施顺序 | Phase 1 太紧 | **分离为 1a + 1b** |
| 测试策略 | 只有单元测试 | **5级测试体系** |
| 安全设计 | .env 在 workspace | **移到 ~/.env/** |

---

## 1️⃣ 项目定位

| 项目 | 说明 |
|------|------|
| **项目名称** | OpenClaw Trading System (OCTS) |
| **定位** | 量化学习/教学工具，非专业交易系统 |
| **用户** | Peng Sheng（主机所有者）|
| **部署位置** | Mac Mini (arm64) + OpenClaw |

---

## 2️⃣ 目录结构 (v2.0)

```
~/.openclaw/workspace-trading/
│
├── config/                          # 配置文件
│   ├── broker.yaml                 # 券商API凭证
│   ├── risk_rules.yaml             # 风控规则
│   ├── strategies.yaml             # 策略参数
│   ├── notification.yaml           # 通知设置
│   └── .gitignore                  # 忽略敏感文件
│
├── core/                           # 核心业务逻辑
│   ├── __init__.py
│   ├── market_data.py              # 行情数据（Redis + yfinance）
│   ├── strategy.py                 # 策略基类
│   ├── risk_manager.py             # 风险管理（4层风控）
│   ├── executor.py                 # 执行引擎
│   ├── portfolio.py                # 持仓管理
│   ├── metrics.py                  # 【新增】VaR/夏普/卡尔玛计算
│   ├── position_state_machine.py   # 【从services移入】持仓状态机
│   └── data_manager.py             # 数据管理层
│
├── services/                       # 服务层
│   ├── __init__.py
│   ├── order_queue.py              # FIFO 订单队列
│   ├── notifier.py                 # 【新增】通知服务（飞书/邮件）
│   ├── strategy_router.py          # 【新增】策略选择/动态权重
│   ├── config_validator.py         # 【新增】配置校验
│   └── recovery.py                 # 崩溃恢复服务
│
├── strategies/                     # 策略实现
│   ├── __init__.py
│   ├── rsi_v2.py                  # RSI均值回归 v2
│   ├── macd_v2.py                 # MACD趋势跟踪 v2
│   └── sector_rotation.py          # ETF板块轮动
│
├── models/                        # 数据模型（纯数据结构）
│   ├── __init__.py
│   ├── order.py                   # 订单模型
│   ├── position.py                # 持仓模型
│   └── signal.py                  # 信号模型
│
├── data/                         # 数据存储
│   ├── cache/                    # Redis缓存（实时行情）
│   ├── daily/                    # 日线历史数据
│   ├── minute/                   # 分钟数据
│   └── logs/                    # 日志
│       ├── trades/              # 成交记录
│       ├── errors/              # 错误日志
│       └── daily/              # 每日报告
│
├── backtest/                     # 回测模块
│   ├── engine.py               # 回测引擎
│   ├── validator.py            # Walk-forward 验证
│   └── results/                # 回测结果
│
├── tests/                       # 测试
│   ├── unit/                  # 单元测试
│   ├── integration/           # 【新增】集成测试
│   └── fixtures/             # 测试数据
│
├── scripts/                    # OpenClaw 集成脚本
│   ├── trading_cli.py        # 【新增】Agent 调用接口
│   ├── get_all_data.py      # 获取数据
│   ├── run_strategy.py      # 运行策略
│   ├── check_positions.py   # 检查持仓
│   ├── daily_report.py      # 生成日报
│   └── emergency_close.py   # 紧急平仓
│
├── docs/                       # 文档
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── USER_GUIDE.md
│
├── README.md
├── requirements.txt           # Python 依赖
├── .env.example              # 环境变量示例
└── IMPLEMENTATION_PLAN_v2.md  # 本计划
```

---

## 3️⃣ 系统级依赖

### 3.1 Python 环境 ⚠️ 重要

| 版本 | 状态 | 建议 |
|------|------|------|
| **Python 3.14** | ⚠️ 太新 | 不推荐（很多包未支持） |
| **Python 3.12** | ✅ 推荐 | 开发环境 |
| **Python 3.11** | ✅ 可用 | 备选 |

**设置 Python 3.12 开发环境**：

```bash
# 创建 venv
cd ~/.openclaw/workspace-trading
uv venv --python 3.12 .venv312

# 激活环境
source .venv312/bin/activate

# 验证
python --version  # 应该是 3.12.x

# 如果没有 3.12，先安装
# brew install python@3.12
```

### 3.2 系统软件

| 软件 | 版本 | 用途 | 状态 | 安装 |
|------|------|------|------|------|
| **Redis** | 7.0+ | 实时行情缓存 | ⚠️ 需安装 | `brew install redis` |
| **PostgreSQL** | 14+ | 持久化存储 | ⚠️ 需安装 | `brew install postgresql` |

> **Phase 1 可用 SQLite 替代 PostgreSQL**，Phase 2 再安装

### 3.3 Apple Silicon (M1/M2/M3) 注意事项

```bash
# 安装 Redis 时可能需要
brew install redis --build-from-source

# PostgreSQL 通常原生支持 Apple Silicon
brew install postgresql@14
```

---

## 4️⃣ Python 依赖 (v2.0 修正版)

### 4.1 核心依赖

| 包名 | 版本 | 用途 | 备注 |
|------|------|------|------|
| `numpy` | ≥1.24 | 数值计算 | ✅ 已有 |
| `pandas` | ≥2.0 | 数据处理 | ✅ 已有 |
| `yfinance` | ≥0.2 | Yahoo Finance 行情 | ✅ 已有 |
| `pandas-ta` | ≥0.3 | 技术指标 | 需安装 |
| `sqlalchemy` | ≥2.0 | 数据库 ORM | 需安装 |
| `redis[hiredis]` | ≥4.5 | Redis 客户端 | **修正：redis[hiredis]** |
| **`alpaca-py`** | ≥0.5 | **Alpaca 券商接口** | **修正：替代废弃的 alpaca-trade-api** |
| `loguru` | ≥0.7 | 日志系统 | 需安装 |
| `pyyaml` | ≥6.0 | 配置文件 | 需安装 |
| `python-dotenv` | ≥1.0 | 环境变量 | 需安装 |
| `schedule` | ≥1.2 | 定时任务 | 需安装 |

### 4.2 风险指标

| 包名 | 版本 | 用途 | 备注 |
|------|------|------|------|
| `empyrical` | ≥0.5 | **【新增】VaR/夏普/卡尔玛计算** | 强烈推荐 |

### 4.3 数据库驱动

| 包名 | 版本 | 用途 | 备注 |
|------|------|------|------|
| `psycopg2-binary` | ≥2.9 | **【新增】PostgreSQL 驱动 | Phase 2+ 需要 |
| `asyncpg` | ≥0.28 | PostgreSQL 异步驱动 | 可选 |

### 4.4 回测与可视化

| 包名 | 版本 | 用途 | 备注 |
|------|------|------|------|
| `vectorbt` | ≥0.25 | 快速回测 | 推荐 |
| `plotly` | ≥5.15 | 数据可视化 | 推荐 |

### 4.5 测试

| 包名 | 版本 | 用途 | 备注 |
|------|------|------|------|
| `pytest` | ≥7.4 | 单元测试框架 | 需安装 |
| `pytest-asyncio` | ≥0.21 | 异步测试 | 需安装 |
| `pytest-cov` | ≥4.1 | 测试覆盖率 | 可选 |

### 4.6 requirements.txt (v2.0)

```
# Core Data
numpy>=1.24.0
pandas>=2.0.0
yfinance>=0.2.0

# Technical Analysis
pandas-ta>=0.3.14

# Database & Cache
sqlalchemy>=2.0.0
redis[hiredis]>=4.5.0

# 【修正】Alpaca Broker API - 使用新版库
alpaca-py>=0.5.0

# Risk Metrics 【新增】
empyrical>=0.5.0

# Database Drivers 【新增】
psycopg2-binary>=2.9.0
asyncpg>=0.28.0

# Utilities
loguru>=0.7.0
pyyaml>=6.0
python-dotenv>=1.0.0
schedule>=1.2.0

# Backtesting & Visualization (Optional but recommended)
vectorbt>=0.25.0
plotly>=5.15.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
```

### 4.7 安装命令

```bash
# 激活 venv
source ~/.openclaw/workspace-trading/.venv312/bin/activate

# 安装核心依赖
uv pip install numpy pandas yfinance pandas-ta sqlalchemy redis[hiredis] alpaca-py

# 安装风控指标
uv pip install empyrical

# 安装工具库
uv pip install loguru pyyaml python-dotenv schedule

# 安装测试
uv pip install pytest pytest-asyncio pytest-cov

# 【可选】回测和可视化
uv pip install vectorbt plotly
```

---

## 5️⃣ API 平台 (v2.0)

### 5.1 Alpaca 配置

**重要**：Alpaca Paper 和 Live 是**不同的 endpoint**！

```yaml
# broker.yaml
alpaca:
  mode: paper  # paper | live
  api_key: "PKXXXXXXXXXXXXXXXX"
  secret_key: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  
  endpoints:
    paper: https://paper-api.alpaca.markets
    live: https://api.alpaca.markets
  
  data_endpoints:
    paper: wss://paper-data.alpaca.markets
    live: wss://data.alpaca.markets
```

### 5.2 API 申请清单

| 平台 | 费用 | 用途 | 申请地址 |
|------|------|------|---------|
| **Alpaca Paper Trading** | 免费 | 模拟交易 | https://app.alpaca.markets/ |
| **Alpaca Live Trading** | $0 commission | 真实交易 | 同上，需 SSN |

---

## 6️⃣ 实施路线图 (v2.0 修正版)

### 并行任务优化

```
Week 1: [数据层] 和 [OpenClaw集成] 可以并行
Week 2: [策略开发] 和 [风控开发] 可以并行
Week 3: [Walk-forward回测] 和 [监控Dashboard] 可以并行
```

### 详细阶段

| 阶段 | 时间 | 目标 | 关键交付物 |
|------|------|------|-----------|
| **Phase 1a** | 第1周前半 | 数据层 + Redis缓存 + SQLite | market_data.py, data_manager.py |
| **Phase 1b** | 第1周后半 | 订单队列 + 状态机 + Alpaca连接 | order_queue.py, executor.py, alpaca-py集成 |
| **Phase 2** | 第2周 | 3个策略 + 3层风控 + 简单回测 | strategies/*.py, risk_manager.py (3层) |
| **Phase 3** | 第3周 | Walk-forward回测 + 第4层风控 | backtest/engine.py, risk_manager.py (4层) |
| **Phase 4** | 第4周 | Alpaca Live + fail-safe + 崩溃恢复 | recovery.py, fail-safe 机制 |
| **Phase 5** | 第5-8周 | 监控Dashboard + 飞书通知 + 策略动态权重 | services/notifier.py, strategy_router.py |

### Phase 1a 详细任务

```
□ 安装 Python 3.12 venv
□ 安装依赖包
□ 申请 Alpaca Paper Trading 账号
□ 配置 config/broker.yaml（区分 paper/live）
□ 实现 core/market_data.py（yfinance + Redis）
□ 实现 core/data_manager.py（SQLite 持久化）
□ 实现 services/config_validator.py
□ 测试：获取 SPY 实时数据
```

### Phase 1b 详细任务

```
□ 实现 models/order.py（订单模型）
□ 实现 models/position.py（持仓模型）
□ 实现 services/order_queue.py（FIFO 队列）
□ 实现 core/position_state_machine.py
□ 实现 core/executor.py（alpaca-py 集成）
□ 实现 services/recovery.py（持久化日志）
□ 集成到 OpenClaw（scripts/trading_cli.py）
□ 测试：发送 Paper 订单
```

### Phase 2 详细任务

```
□ 实现 strategies/rsi_v2.py（RSI + 量 + ADX）
□ 实现 strategies/macd_v2.py（MACD + ADX）
□ 实现 strategies/sector_rotation.py（ETF 相对强弱）
□ 实现 core/risk_manager.py（Layer 1-3 风控）
□ 实现 backtest/engine.py（简单回测）
□ 测试：策略回测
```

### Phase 3 详细任务

```
□ 实现 backtest/validator.py（Walk-forward）
□ 实现 core/metrics.py（VaR/夏普/卡尔玛）
□ 完善风控 Layer 4（事后风控）
□ 对比 vectorbt 验证回测结果
□ 测试：多周期回测验证
```

### Phase 4 详细任务

```
□ 切换到 Alpaca Live API
□ 实现 fail-safe 风控机制（风控宕机=拒绝所有订单）
□ 实现崩溃恢复（重启后从持久化日志恢复状态）
□ 对比 Paper vs Live 执行差异
□ 测试：Live API 连接和订单执行
```

### Phase 5 详细任务

```
□ 实现 services/notifier.py（飞书/邮件通知）
□ 实现 services/strategy_router.py（动态策略权重）
□ 实现监控 Dashboard（Prometheus metrics 可选）
□ 配置定时任务（每日报告）
□ 记录每笔成交，对比回测
```

---

## 7️⃣ 测试策略 (v2.0 新增)

### 5 级测试体系

| Level | 测试类型 | 工具 | 运行频率 | 负责人 |
|-------|---------|------|---------|--------|
| **L1** | 单元测试 | pytest | 每次 commit | 自动 |
| **L2** | 策略回测验证 | vectorbt | 每周 | 自动 |
| **L3** | 集成测试 | pytest + Alpaca Paper | 每次代码变更 | 自动 |
| **L4** | 模拟交易 | Alpaca Paper | 1周 | 自动 |
| **L5** | 真实交易 | Alpaca Live (tiny amount) | 持续 | 人工监控 |

### 快速验证命令

```bash
# L1: 单元测试
pytest tests/unit/ -v --tb=short

# L1: 带覆盖率
pytest tests/unit/ --cov=core --cov-report=html

# L2: 回测验证（每周）
python -m backtest.validator --compare vectorbt

# L3: 集成测试
python -m tests.integration --alpaca paper

# L4: 模拟交易验证
python -m scripts.run_strategy --mode paper --days 7
```

### 测试目录结构

```
tests/
├── unit/                    # 单元测试
│   ├── __init__.py
│   ├── test_risk_manager.py
│   ├── test_order_queue.py
│   ├── test_strategy.py
│   └── fixtures/           # 测试数据
│       └── sample_data.csv
├── integration/            # 【新增】集成测试
│   ├── __init__.py
│   ├── test_order_flow.py  # 订单队列 → 执行 → 持仓更新
│   ├── test_alpaca_connection.py
│   └── test_recovery.py    # 崩溃恢复
└── conftest.py            # pytest 配置
```

---

## 8️⃣ 安全设计 (v2.0 改进)

### 8.1 环境变量位置

⚠️ **.env 不再放在 workspace 内**，移到 `~/.env/`

```bash
# 创建 ~/.env 目录
mkdir -p ~/.env

# 创建 trading 系统配置
cat > ~/.env/trading.env << 'EOF'
# Alpaca API Keys
ALPACA_API_KEY=PKXXXXXXXXXXXXXXXX
ALPACA_SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ALPACA_MODE=paper

# Database
DATABASE_URL=sqlite:///./data/trading.db

# Redis
REDIS_URL=redis://localhost:6379

# Notification
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
EOF

# 保护文件权限
chmod 600 ~/.env/trading.env
```

### 8.2 .gitignore (v2.0)

```gitignore
# Environment variables 【修正：移到 ~/.env/】
.env
*.env
.env.*

# Data files
data/
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv*/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/

# Build
dist/
build/
*.egg-info/
```

### 8.3 安全最佳实践

| 项目 | 建议 |
|------|------|
| **API Keys** | 放在 `~/.env/trading.env`，不要提交到 git |
| **生产环境** | 考虑使用 `keyring` 库或 AWS Secrets Manager |
| **pre-commit hook** | 添加 git hook 防止误提交敏感信息 |

```bash
# 安装 pre-commit hook（可选）
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# 检查是否误提交敏感信息
if git diff --cached | grep -E "(ALPACA_API_KEY|SECRET_KEY|password)" > /dev/null; then
    echo "ERROR: Attempting to commit sensitive information!"
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

---

## 9️⃣ OpenClaw 集成 (v2.0)

### Phase 1-2: scripts/ + exec 调用

```python
# Agent 调用方式
exec("python3 ~/.openclaw/workspace-trading/scripts/trading_cli.py run_strategy RSI")
```

### trading_cli.py 设计

```python
#!/usr/bin/env python3
"""
OpenClaw Agent 调用接口
用法: python3 trading_cli.py <command> [args]
"""
import sys
import json
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if cmd == "run_strategy":
        strategy = sys.argv[2] if len(sys.argv) > 2 else "RSI"
        from core.strategy import StrategyRunner
        result = StrategyRunner.run(strategy)
        print(json.dumps(result, indent=2, default=str))
        
    elif cmd == "get_positions":
        from core.portfolio import Portfolio
        portfolio = Portfolio.load()
        print(json.dumps(portfolio.to_dict(), indent=2, default=str))
        
    elif cmd == "get_orders":
        from core.executor import Executor
        executor = Executor()
        orders = executor.get_orders()
        print(json.dumps(orders, indent=2, default=str))
        
    elif cmd == "emergency_close":
        from services.notifier import EmergencyClose
        result = EmergencyClose.execute()
        print(json.dumps(result, indent=2, default=str))
        
    elif cmd == "help":
        print("""Trading CLI - OpenClaw Integration
Commands:
  run_strategy <name>  - Run a strategy (RSI, MACD, SECTOR)
  get_positions        - Get current positions
  get_orders           - Get open orders
  emergency_close      - Close all positions immediately
  help                 - Show this help
""")
    else:
        print(f"Unknown command: {cmd}")
        print("Run 'trading_cli.py help' for usage")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Phase 4+: 迁移到 MCP Server（备选）

```json
// OpenClaw MCP 配置
{
  "mcpServers": {
    "trading": {
      "command": "python3",
      "args": ["-m", "trading_mcp_server"],
      "env": {
        "ALPACA_API_KEY": "xxx",
        "ALPACA_SECRET_KEY": "xxx"
      }
    }
  }
}
```

---

## 🔟 你需要做的事情 (v2.0)

### 你的任务清单

| 任务 | 具体事项 | 耗时 | 状态 |
|------|---------|------|------|
| **1. 注册 Alpaca** | https://app.alpaca.markets/ | 5分钟 | ⏳ 待你完成 |
| **2. 获取 API Keys** | Dashboard 复制 Key 和 Secret | 2分钟 | ⏳ 待你完成 |
| **3. 确认 Python 3.12** | `python3.12 --version` | 1分钟 | ⏳ 待确认 |

### 快速开始流程

```
Step 1: 去 https://app.alpaca.markets/ 注册 Paper Trading 账号
Step 2: 登录后在 Dashboard 获取 API Key 和 Secret Key
Step 3: 把这两个 key 发给我
Step 4: 我来完成环境搭建和代码实现
```

---

## 📋 实施检查清单

### 实施前（你的任务）

- [ ] 申请 Alpaca Paper Trading 账号
- [ ] 获取 API Key 和 Secret Key
- [ ] 确认 Python 3.12 可用（`python3.12 --version`）
- [ ] 如果没有 3.12，安装：`brew install python@3.12`

### Phase 1a 交付物

- [ ] Python 3.12 venv 创建完成
- [ ] 依赖包安装完成
- [ ] Alpaca Paper 连接成功
- [ ] config/broker.yaml 配置完成
- [ ] market_data.py 可以获取 SPY 实时数据
- [ ] SQLite 数据存储正常

### Phase 1b 交付物

- [ ] order_queue.py FIFO 队列正常工作
- [ ] position_state_machine.py 状态机正常
- [ ] executor.py 可以发送 Paper 订单
- [ ] trading_cli.py 可以被 OpenClaw 调用
- [ ] recovery.py 持久化日志正常

---

## ❓ 常见问题

**Q: 为什么用 Python 3.12 而不是 3.14？**
A: Python 3.14 太新（2024年10月发布），很多包还没支持。3.12 是稳定版本，生态最完善。

**Q: 需要多少钱开始？**
A: $0。Alpaca Paper Trading 免费，yfinance 免费。

**Q: 什么时候可以用真实资金？**
A: Phase 5 之后，且需要你手动授权。系统设置为"信号提醒+手动确认"模式。

**Q: 亏损了怎么办？**
A: Phase 1-4 都是 Paper/Live 模拟资金，不会亏真实钱。Phase 5+ 请谨慎。

---

## 📄 变更历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-03-25 | 初始计划 |
| v2.0 | 2026-03-25 | 采纳 Claire Review 建议：修正依赖、目录结构、实施路线图、测试体系、安全设计 |

---

*本计划基于 2026-03-25 的 Claude Review 改进 v2.0*
*如需修改，请联系 Emily*
