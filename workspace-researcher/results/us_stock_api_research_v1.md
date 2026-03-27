# 美股量化交易 API 研究报告 v1.0

## 研究目标
整理适合美股量化交易的 API 组合，覆盖：行情、技术指标、基本面、新闻、交易执行

---

## 一、行情数据 API

### 1. yfinance（Yahoo Finance）
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐⭐⭐⭐ | 完全免费，无需 API Key |
| 数据延迟 | ⭐⭐⭐ | 15-20分钟延迟，非实时 |
| 覆盖范围 | ⭐⭐⭐⭐ | 美股、港股、A股、加密货币等 |
| 可靠性 | ⭐⭐⭐⭐ | Yahoo 大厂背书，稳定性好 |
| Python 封装 | ⭐⭐⭐⭐⭐ | `pip install yfinance`，接口简洁 |
| **综合** | **8/10** | 入门首选，免费无限制 |

**限制**：无实时数据（延迟 15-20 分钟），不适合日内交易

```python
import yfinance as yf
data = yf.download("AAPL", start="2024-01-01")
```

---

### 2. Finnhub
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐⭐ | 100 calls/day |
| 数据延迟 | ⭐⭐⭐⭐⭐ | 实时数据（WebSocket） |
| 覆盖范围 | ⭐⭐⭐⭐ | 全球股票、新闻、IPO、财报 |
| API 限制 | 60 calls/sec | 付费用户更高 |
| Python 封装 | ⭐⭐⭐⭐ | `pip install finnhub-python` |
| **综合** | **7/10** | 实时性好，但免费额度少 |

**定价**：$29/月（专业版）起

```python
import finnhub
finnhub_client = finnhub.Client(api_key="YOUR_KEY")
quote = finnhub_client.quote("AAPL")  # real-time quote
```

---

### 3. Polygon.io（现为 Massive）
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐ | 500 calls/day（已收紧） |
| 数据延迟 | ⭐⭐⭐⭐⭐ | 实时 + 历史，顶级质量 |
| 覆盖范围 | ⭐⭐⭐⭐⭐ | 全美股、期权、Forex、加密 |
| API 限制 | 付费解锁更高 | 稳定性极佳 |
| Python 封装 | ⭐⭐⭐⭐⭐ | 官方 SDK，文档完善 |
| **综合** | **8/10** | 专业级，但免费额度少 |

**定价**：$200/月（基础专业版）起

---

### 4. Alpha Vantage
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐ | 25 requests/day（极低） |
| 数据延迟 | ⭐⭐⭐⭐ | 实时/历史 |
| 技术指标 | ⭐⭐⭐⭐⭐ | 强大，RSI、MACD、BB 等 50+ |
| Python 封装 | ⭐⭐⭐⭐ | `pip install alpha-vantage` |
| **综合** | **6/10** | 指标丰富，但免费额度太低 |

**定价**：$49.99/月（标准版）起

---

### 5. IEX Cloud（IEX Markets）
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐⭐ | 50M credits/月（测试用够） |
| 数据延迟 | ⭐⭐⭐⭐ | 实时 + 历史 |
| 覆盖范围 | ⭐⭐⭐⭐ | 美股为主，数据质量高 |
| Python 封装 | ⭐⭐⭐⭐ | 官方 Python 客户端 |
| **综合** | **7/10** | 性价比高，免费额度实用 |

**定价**：按查询量付费（$0.00005/credit）

---

## 二、新闻/舆情 API

### 6. NewsAPI
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐ | 100 requests/day |
| 商业限制 | ❌ | 仅开发/非商业用途 |
| Python 封装 | ⭐⭐⭐⭐ | `pip install newsapi-python` |
| **综合** | **5/10** | 非商业项目可用，商用太贵 |

**定价**：$449/月起（商业版）

---

### 7. Benzinga
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐ | 有限免费 |
| 新闻质量 | ⭐⭐⭐⭐⭐ | 财经专业媒体，实时性好 |
| 覆盖范围 | ⭐⭐⭐⭐ | 美股、全球市场、宏观 |
| **综合** | **7/10** | 专业级财经新闻 |

**定价**：$100/月起

---

### 8. Finnhub News（与行情 API 合并）
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐⭐ | 100 calls/day（与行情共享） |
| 新闻质量 | ⭐⭐⭐⭐ | 实时新闻、社交媒体情绪 |
| **综合** | **7/10** | 一站式解决方案 |

---

## 三、基本面数据 API

### 9. SEC EDGAR
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐⭐⭐⭐ | 完全免费，无限制 |
| 数据类型 | ⭐⭐⭐⭐⭐ | 10-K、10-Q、8-K、委托书等 |
| API 支持 | ⭐⭐ | 需自行爬取，无官方 API |
| Python 封装 | ⭐⭐⭐ | `sec-edgar-downloader` 等第三方库 |
| **综合** | **8/10** | 免费且全面，但需爬虫 |

```python
# 使用 sec-edgar-downloader
pip install sec-edgar-downloader
```

---

### 10. yfinance（基本面）
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐⭐⭐⭐ | 免费 |
| 数据类型 | ⭐⭐⭐⭐ | 财报、现金流、股息、评级 |
| **综合** | **8/10** | 与行情数据一起获取，方便 |

```python
stock = yf.Ticker("AAPL")
info = stock.info  # 基本面信息
financials = stock.financials
```

---

## 四、技术指标计算

### 11. pandas-ta
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐⭐⭐⭐⭐ | 完全免费，开源 |
| 指标数量 | ⭐⭐⭐⭐⭐ | 150+ 指标（RSI、MACD、BB、SMA 等） |
| 本地计算 | ⭐⭐⭐⭐⭐ | 不依赖 API，用价格数据计算 |
| Python 封装 | ⭐⭐⭐⭐⭐ | `pip install pandas-ta` |
| **综合** | **9/10** | 技术指标首选，无需任何费用 |

```python
import pandas as pd
import pandas_ta as ta

df = pd.read_csv("price_data.csv")
df['rsi'] = ta.rsi(df['close'], length=14)
df['macd'] = ta.macd(df['close'])
```

---

## 五、交易执行 API

### 12. Alpaca
| 维度 | 评分 | 说明 |
|------|------|------|
| 模拟交易 | ⭐⭐⭐⭐⭐ | 完全免费 |
| 真实交易 | ⭐⭐⭐⭐ | 零佣金（股票、ETF） |
| API 质量 | ⭐⭐⭐⭐⭐ | REST + WebSocket，文档完善 |
| Python 封装 | ⭐⭐⭐⭐⭐ | 官方 SDK |
| **综合** | **9/10** | 量化交易入门首选 |

```python
import alpaca_trade_api as alpaca

api = alpaca.REST('API_KEY', 'SECRET_KEY', base_url='https://paper-api.alpaca.markets')
api.submit_order symbol='AAPL', qty=10, side='buy', type='market', time_in_force='day'
```

---

### 13. Interactive Brokers (TWS API)
| 维度 | 评分 | 说明 |
|------|------|------|
| 模拟交易 | ⭐⭐⭐⭐ | IBKR Paper Trading |
| 真实交易 | ⭐⭐⭐⭐⭐ | 全球市场、零佣金（美股） |
| API 复杂度 | ⭐⭐ | 需要安装 TWS，配置复杂 |
| Python 封装 | ⭐⭐⭐ | `ib_insync` 第三方封装 |
| **综合** | **8/10** | 专业级，但学习曲线陡 |

---

### 14. TD Ameritrade API
| 维度 | 评分 | 说明 |
|------|------|------|
| 状态 | ❌ | **已停止对新用户开放** |
| 替代方案 | Alpaca、Interactive Brokers | - |

---

## 六、其他补充

### 15. NASDAQ Data Link（原 Quandl）
| 维度 | 评分 | 说明 |
|------|------|------|
| 免费额度 | ⭐ | 有限 |
| 数据质量 | ⭐⭐⭐⭐⭐ | 优质金融数据（替代数据、期货等） |
| **综合** | **6/10** | 高级用户专用 |

---

## 七、综合推荐组合

### 🥇 最低成本组合（$0）
| 用途 | API | 成本 |
|------|------|------|
| 行情 | yfinance | 免费 |
| 技术指标 | pandas-ta | 免费 |
| 基本面 | SEC EDGAR + yfinance | 免费 |
| 新闻 | Finnhub (100 calls/day) | 免费 |
| 执行 | Alpaca Paper | 免费 |

**总成本：$0/月**

---

### 🥈 性价比组合（~$30/月）
| 用途 | API | 成本 |
|------|------|------|
| 行情 | Finnhub Pro | $29/月 |
| 技术指标 | pandas-ta | 免费 |
| 基本面 | yfinance | 免费 |
| 新闻 | Finnhub News | 包含 |
| 执行 | Alpaca | 免费（模拟） |

**总成本：$29/月**

---

### 🥉 专业级组合（$200+/月）
| 用途 | API | 成本 |
|------|------|------|
| 行情实时 | Polygon.io (Massive) | $200/月 |
| 技术指标 | pandas-ta | 免费 |
| 基本面 | SEC EDGAR + yfinance | 免费 |
| 新闻 | Benzinga Pro | $100/月 |
| 执行 | Alpaca / IBKR | $0 |

**总成本：$300/月起**

---

## 八、验证清单

- [x] yfinance - 实测可用
- [x] Finnhub - API Key 申请
- [x] Polygon.io - 已更名为 Massive
- [ ] Alpha Vantage - 需验证免费额度是否仍然 25/day
- [x] pandas-ta - pip install 可用
- [ ] IEX Cloud - 需进一步验证定价
- [x] Alpaca - 文档完善
- [ ] Interactive Brokers - 需账号

---

## 九、待深入验证

1. **Alpha Vantage 免费额度**：是否仍是 25 calls/day？有无变化？
2. **IEX Cloud**：credit 消耗比例，实际可用量
3. **Polygon.io 新定价**： Massive 收购后免费政策变化
4. **真实交易成本**：Alpaca 真实账户开户门槛

