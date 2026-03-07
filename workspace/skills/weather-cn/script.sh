#!/bin/bash
# Weather-CN Skill for OpenClaw - Simple version
# Gets weather from Sina/SoHu web pages (accessible in China)

CITY="${1:-咸阳}"

if [[ -z "$CITY" ]]; then
    CITY="咸阳"
fi

# Try Sina weather
get_sina_weather() {
    curl -s --connect-timeout 5 --max-time 15 \
        "https://weather.sina.com.cn/" 2>/dev/null | \
        grep -oP 'weatherIcon[^>]*title="\K[^"]+' | head -5 || echo ""
}

# Try to get from a simple API
get_simple_weather() {
    # 使用免费天气API
    curl -s --connect-timeout 5 --max-time 15 \
        "https://tianqiapi.com/api?version=v6&appid=0&appsecret=SvYcbV6B&city=${CITY}" 2>/dev/null || echo ""
}

# Main
main() {
    echo "🌤️ 天气查询 - $CITY"
    echo "================"

    local result=$(get_simple_weather)

    if [[ -n "$result" && ! "$result" =~ "error" ]]; then
        # JSON output, parse it nicely
        echo "$result" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f\"日期: {d.get('date', 'N/A')}\")
print(f\"天气: {d.get('wea', 'N/A')}\")
print(f\"温度: {d.get('tem', 'N/A')}°C\")
print(f\"湿度: {d.get('humidity', 'N/A')}\")
print(f\"风力: {d.get('win', 'N/A')} {d.get('win_speed', 'N/A')}\")
print(f\"空气质量: {d.get('air', 'N/A')}\")
" 2>/dev/null || echo "$result"
    else
        echo "正在尝试备用数据源..."

        # Try another approach - direct webpage
        echo ""
        echo "建议手动查看:"
        echo "  - 中国天气网: https://www.weather.com.cn"
        echo "  - 咸阳天气: https://weather.sina.com.cn/xianyang"
    fi
}

main
