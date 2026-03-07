---
name: weather-cn
description: Get China weather forecast using QWeather (和风天气) API or Netease (网易) weather.
homepage: https://dev.qweather.com/
metadata:
  openclaw:
    emoji: 🌤️
    requires:
      bins: ["curl"]
      env: ["QWEATHER_API_KEY"]  # Optional: 和风天气 API Key
---

# Weather-CN (中国天气)

Get weather forecast for China cities.

## Setup

### Option 1: QWeather API (Recommended)
1. Register at https://dev.qweather.com/
2. Get free API key
3. Set environment variable: `QWEATHER_API_KEY`
4. Or pass key directly in command

### Option 2: Netease (Fallback)
Free, no key needed.

## Usage

### QWeather (和风天气)
```bash
# Get current weather
weather-cn "咸阳" --type current

# Get 7-day forecast
weather-cn "咸阳" --type forecast

# With API key
weather-cn "咸阳" --key YOUR_API_KEY --type forecast
```

### Netease (网易) - No Key Required
```bash
# Get weather (auto-detects city)
weather-cn "咸阳" --source netease

# Force netease source
weather-cn "咸阳" --netease
```

## City Format
- City name: `咸阳`, `北京`, `上海`
- Full name: `陕西省咸阳市`

## Output Format
- Default: Human readable
- JSON: `--json` flag
