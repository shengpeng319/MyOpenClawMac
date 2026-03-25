#!/bin/bash
# 研报评分脚本
# 评估维度:
# 1. 数据完整性 (25分)
# 2. 分析深度 (25分)
# 3. 投资建议质量 (25分)
# 4. 信息时效性 (15分)
# 5. 结构与可读性 (10分)

REPORT_FILE="$1"
TOTAL=0

echo "=== Emily 研报质量评分系统 ==="
echo ""

# 1. 数据完整性 (25分)
DATA_SCORE=0
echo "【1. 数据完整性】(满分25分)"

# 检查是否包含关键指数数据
if grep -qi "S&P 500\|标普500\|SPY" "$REPORT_FILE"; then
    DATA_SCORE=$((DATA_SCORE + 5))
    echo "  ✓ 包含标普500数据 (+5)"
else
    echo "  ✗ 缺少标普500数据"
fi

if grep -qi "Dow Jones\|道指\|DJI\|道琼斯" "$REPORT_FILE"; then
    DATA_SCORE=$((DATA_SCORE + 5))
    echo "  ✓ 包含道琼斯数据 (+5)"
else
    echo "  ✗ 缺少道琼斯数据"
fi

if grep -qi "Nasdaq\|纳斯达克" "$REPORT_FILE"; then
    DATA_SCORE=$((DATA_SCORE + 5))
    echo "  ✓ 包含纳斯达克数据 (+5)"
else
    echo "  ✗ 缺少纳斯达克数据"
fi

if grep -qiE "oil|原油|Brent|WTI|\$[0-9]+" "$REPORT_FILE"; then
    DATA_SCORE=$((DATA_SCORE + 5))
    echo "  ✓ 包含大宗商品/价格数据 (+5)"
else
    echo "  ✗ 缺少大宗商品数据"
fi

if grep -qiE "Fed|美联储|利率|3\.[0-9]+%|federation funds" "$REPORT_FILE"; then
    DATA_SCORE=$((DATA_SCORE + 5))
    echo "  ✓ 包含美联储/利率数据 (+5)"
else
    echo "  ✗ 缺少美联储/利率数据"
fi

echo "  小计: $DATA_SCORE/25"
TOTAL=$((TOTAL + DATA_SCORE))
echo ""

# 2. 分析深度 (25分)
DEPTH_SCORE=0
echo "【2. 分析深度】(满分25分)"

if grep -qiE "宏观|macro|经济增长|GDP|cpi|inflation" "$REPORT_FILE"; then
    DEPTH_SCORE=$((DEPTH_SCORE + 5))
    echo "  ✓ 包含宏观分析 (+5)"
else
    echo "  ✗ 缺少宏观分析"
fi

if grep -qiE "资金面|流动性|liquidity|VIX|资金流向" "$REPORT_FILE"; then
    DEPTH_SCORE=$((DEPTH_SCORE + 5))
    echo "  ✓ 包含资金面分析 (+5)"
else
    echo "  ✗ 缺少资金面分析"
fi

if grep -qiE "基本面|估值|PE|P/E|盈利|营收|利润" "$REPORT_FILE"; then
    DEPTH_SCORE=$((DEPTH_SCORE + 5))
    echo "  ✓ 包含基本面分析 (+5)"
else
    echo "  ✗ 缺少基本面分析"
fi

if grep -qiE "技术面|技术分析|MA|MACD|RSI|均线|趋势" "$REPORT_FILE"; then
    DEPTH_SCORE=$((DEPTH_SCORE + 5))
    echo "  ✓ 包含技术面分析 (+5)"
else
    echo "  ✗ 缺少技术面分析"
fi

if grep -qiE "地缘|战争|伊朗|伊朗|政治|地缘政治" "$REPORT_FILE"; then
    DEPTH_SCORE=$((DEPTH_SCORE + 5))
    echo "  ✓ 包含地缘政治分析 (+5)"
else
    echo "  ✗ 缺少地缘政治分析"
fi

echo "  小计: $DEPTH_SCORE/25"
TOTAL=$((TOTAL + DEPTH_SCORE))
echo ""

# 3. 投资建议质量 (25分)
ADVICE_SCORE=0
echo "【3. 投资建议质量】(满分25分)"

if grep -qiE "建议|配置|仓位|strategy|recommend|分配" "$REPORT_FILE"; then
    ADVICE_SCORE=$((ADVICE_SCORE + 8))
    echo "  ✓ 包含明确建议 (+8)"
else
    echo "  ✗ 缺少明确建议"
fi

if grep -qiE "风险|警示|注意|风险提示|warning|risk" "$REPORT_FILE"; then
    ADVICE_SCORE=$((ADVICE_SCORE + 7))
    echo "  ✓ 包含风险提示 (+7)"
else
    echo "  ✗ 缺少风险提示"
fi

if grep -qiE "支撑|阻力|点位|level|target|目标" "$REPORT_FILE"; then
    ADVICE_SCORE=$((ADVICE_SCORE + 5))
    echo "  ✓ 包含具体点位/目标 (+5)"
else
    echo "  ✗ 缺少具体点位"
fi

if grep -qiE "板块|行业|sector|industry" "$REPORT_FILE"; then
    ADVICE_SCORE=$((ADVICE_SCORE + 5))
    echo "  ✓ 包含板块/行业分析 (+5)"
else
    echo "  ✗ 缺少板块分析"
fi

echo "  小计: $ADVICE_SCORE/25"
TOTAL=$((TOTAL + ADVICE_SCORE))
echo ""

# 4. 信息时效性 (15分)
TIME_SCORE=0
echo "【4. 信息时效性】(满分15分)"

if grep -qi "3月.*2026\|2026年3月\|March 2026" "$REPORT_FILE"; then
    TIME_SCORE=$((TIME_SCORE + 8))
    echo "  ✓ 标注日期为2026年3月 (+8)"
else
    echo "  ✗ 缺少日期标注或日期非最新"
fi

if grep -qiE "3月24|3月25|3月23|March 24|March 25" "$REPORT_FILE"; then
    TIME_SCORE=$((TIME_SCORE + 7))
    echo "  ✓ 包含近两日数据 (+7)"
else
    echo "  ✗ 数据可能过时"
fi

echo "  小计: $TIME_SCORE/15"
TOTAL=$((TOTAL + TIME_SCORE))
echo ""

# 5. 结构与可读性 (10分)
READ_SCORE=0
echo "【5. 结构与可读性】(满分10分)"

# 检查是否有清晰的章节结构
SECTION_COUNT=$(grep -cE "^## |^### |^【|^\|" "$REPORT_FILE" 2>/dev/null || echo 0)
if [ "$SECTION_COUNT" -ge 5 ]; then
    READ_SCORE=$((READ_SCORE + 4))
    echo "  ✓ 章节结构清晰 (+4) - 约$SECTION_COUNT个章节"
else
    echo "  ✗ 章节结构较弱"
fi

# 检查是否有表格
if grep -qiE "\|.*\|.*\|" "$REPORT_FILE"; then
    READ_SCORE=$((READ_SCORE + 3))
    echo "  ✓ 使用表格呈现数据 (+3)"
else
    echo "  ✗ 缺少表格"
fi

# 检查是否使用emoji或格式化
if grep -qiE "📊|📈|📉|⚠️|✅|✗|🔥" "$REPORT_FILE"; then
    READ_SCORE=$((READ_SCORE + 3))
    echo "  ✓ 使用emoji增强可读性 (+3)"
else
    echo "  ✗ 未使用emoji"
fi

echo "  小计: $READ_SCORE/10"
TOTAL=$((TOTAL + READ_SCORE))
echo ""

# 最终评分
echo "========================================"
echo "【总评分】"
echo "  $TOTAL / 100 分"
echo "========================================"

# 输出评级
if [ "$TOTAL" -ge 90 ]; then
    echo "  评级: ⭐⭐⭐⭐⭐ 卓越"
elif [ "$TOTAL" -ge 80 ]; then
    echo "  评级: ⭐⭐⭐⭐ 优秀"
elif [ "$TOTAL" -ge 70 ]; then
    echo "  评级: ⭐⭐⭐ 良好"
elif [ "$TOTAL" -ge 60 ]; then
    echo "  评级: ⭐⭐ 及格"
else
    echo "  评级: ⭐ 需改进"
fi

echo ""
echo "=== 评分完成 ==="

# 输出总分供脚本提取
echo "QUALITY_SCORE:$TOTAL"
