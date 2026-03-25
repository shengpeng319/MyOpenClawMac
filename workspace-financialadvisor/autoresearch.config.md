# Autoresearch Configuration

## Goal
优化金融投资研报的生成质量，通过系统性实验找到最优的报告生成方法

## Metric
- **Name**: report_quality_score
- **Direction**: higher is better
- **Extract command**: 从评分脚本输出中提取总分 (0-100分)
- **评分维度**:
  1. 数据完整性 (25分) - 关键数据是否齐全（指数点位、油价、利率、个股）
  2. 分析深度 (25分) - 宏观/资金/基本面/技术面分析是否到位
  3. 投资建议质量 (25分) - 建议是否清晰、可操作、风险提示充分
  4. 信息时效性 (15分) - 数据是否为最新（当日/昨日）
  5. 结构与可读性 (10分) - 排版清晰、层次分明

## Target Files
- `KNOWLEDGE/MARKET_ANALYSIS_FRAMEWORK.md` - 市场分析框架
- `KNOWLEDGE/INVESTMENT_PRINCIPLES.md` - 投资原则
- `KNOWLEDGE/RISK_MANAGEMENT.md` - 风险管理
- 报告生成prompts和模板结构

## Read-Only Files
- `AGENTS.md`, `SOUL.md`, `IDENTITY.md` - 身份和核心规则文件

## Run Command
```bash
# 生成研报并评分
cd ~/.openclaw/workspace-financialadvisor && \
./scripts/generate_and_score_report.sh <日期> > results/report_<timestamp>.txt 2>&1
```

## Time Budget
- **Per experiment**: 10分钟
- **Kill timeout**: 20分钟

## Constraints
1. 报告必须包含：指数数据、油价、美联储政策、至少3只个股分析
2. 必须有明确的投资建议和风险提示
3. 数据必须有时效性（24小时内）
4. 每次实验只改变一个变量（如prompt措辞、结构顺序、数据来源等）

## Branch
autoresearch/financial-report-quality

## Notes
这是金融研报生成质量的优化实验。当前基线研报存在以下不足：
1. 数据获取依赖搜索，可能不够实时
2. 分析框架可能不够系统
3. 个股分析深度不足
4. 投资建议可能过于泛泛
5. 缺少量化指标和技术面具体点位
