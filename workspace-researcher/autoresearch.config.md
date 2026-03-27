# Autoresearch Config - 选股型自动化交易系统教程改进

## 任务目标
改进 Emily 的《选股型自动化交易系统数据源教程》，从 85 分提升到 90+ 分

## 当前问题（v1_baseline: 85/100）
1. **Sharpe Ratio 计算错误**：公式少减无风险利率
2. **缺 Benzinga**：新闻情绪数据源未收录
3. **缺 FMP vs Finnhub 对比**：财务数据源对比
4. **中文社区反馈缺失**：未调研国内用户实际使用反馈

## 目标评分
- 通过阈值：≥90/100
- 主要维度：数据准确性、技术完整性、实用性

## 验证方式
1. 对比各数据源实际 API 响应
2. 验证 Python 代码可运行性
3. 检查 Sharpe Ratio 公式正确性

## 成功标准
改进版本需包含：
- ✅ Sharpe Ratio 正确计算（含无风险利率）
- ✅ Benzinga 数据源说明
- ✅ FMP vs Finnhub 对比表
- ✅ 中文社区使用反馈（至少 1-2 个来源）

## 实验记录
- 分支：autoresearch/tutorial-improvement-20260327
- baseline：85/100
- 目标：90/100
