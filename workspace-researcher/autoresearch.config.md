# Autoresearch Configuration - Emily 研报审核

## Goal
通过迭代审核流程，提升 Emily 投资研报质量，达到 production-ready 标准（≥90分）。

## Metric
- **Name**: 研报评分 (0-100)
- **Direction**: 越高越好
- **评估维度**:
  - 数据准确性 (25分)
  - 技术分析完整性 (25分)
  - 投资建议可操作性 (25分)
  - 格式规范/预测跟踪 (25分)

## Target Files
- Emily 研报: `/Users/shengpeng319/.openclaw/workspace-financialadvisor/results/report_YYYYMMDD.md`
- Emily 框架模板: `/Users/shengpeng319/.openclaw/workspace-financialadvisor/MARKET_ANALYSIS_FRAMEWORK.md`

## Read-Only Files
- Yahoo Finance 数据源 (只读)
- 我的审核标准和反馈意见

## Run Command
Emily 根据反馈修订报告，生成新版本 (v3.3, v3.4...)

## Time Budget
- **每次迭代**: 5-10 分钟 (Emily 修订)
- **Kill timeout**: 15 分钟

## Constraints
- 不修改 Yahoo Finance 数据获取逻辑
- 只审核已生成的报告
- 反馈必须具体、可操作

## Branch
`autoresearch/emily-report-review-20260327`

## Notes
- 审核对象: Emily 2026-03-27 研报
- 当前版本得分: 75/100
- 待解决问题: RSI 计算修复、具体价位、预测跟踪表
