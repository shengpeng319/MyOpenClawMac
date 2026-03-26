
---

## 八、中文信息来源解决方案（2026-03-26 更新）

### 8.1 SearXNG 中文引擎 ✅ 已启用

**配置位置**: `~/.docker/config/settings.yml`

**已启用的中文引擎**:
| 引擎 | 快捷命令 | 状态 |
|------|---------|------|
| 百度 | `baidu` 或 `bd` | ✅ 已启用 |
| 搜狗 | `sogou` | ✅ 已启用 |
| Bilibili | `bilibili` 或 `bil` | ✅ 已启用 |

**使用方法**:
```bash
# 直接搜索中文
curl -X POST "http://localhost:12613/search" \
  --data-urlencode "q=人工智能" \
  --data-urlencode "format=json" \
  --data-urlencode "engines=baidu,google"
```

**测试结果**:
```
- 人工智能(博士、硕士层次专业) - 百度百科
- 国务院关于深入实施"人工智能+"行动的意见
- 牢牢掌握人工智能发展和治理主动权
```

### 8.2 中文新闻 RSS 源

| 来源 | RSS 地址 | 说明 |
|------|---------|------|
| 澎湃新闻 | `https://www.thepaper.cn/list_25431.rss` | 深度报道 |
| 虎嗅 | `https://www.huxiu.com/rss/0.xml` | 科技商业 |
| 36氪 | `https://36kr.com/feed` | 创业投资 |
| 知乎日报 | `https://daily.zhihu.com/rss` | 精选问答 |
| 人民日报 | `https://www.people.com.cn/rss/politics.xml` | 时政要闻 |
| 新京报 | `https://www.bjnews.com.cn/rss/130.xml` | 综合新闻 |
| 参考消息 | `https://www.cankaoxiaoxi.com/rss/` | 国际资讯 |
| 财新 | `https://weekly.caixin.com/rss/` | 深度财经 |

**使用方式**:
```bash
# 获取虎嗅 RSS
curl -s "https://www.huxiu.com/rss/0.xml" | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
for item in tree.findall('.//item')[:5]:
    print('- ' + item.find('title').text)
"

# 获取澎湃新闻
curl -s "https://www.thepaper.cn/list_25431.rss" | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin)
for item in tree.findall('.//item')[:5]:
    print('- ' + item.find('title').text)
"
```

### 8.3 社交媒体中文平台

通过 `agent-reach` 支持:
| 平台 | 快捷命令 | 说明 |
|------|---------|------|
| 微博 | `weibo` | 热搜、话题 |
| 小红书 | `xhs` | 种草、笔记 |
| 微信公众号 | `wechat` | 图文内容 |
| 知乎 | `zhihu` | 问答社区 |
| 抖音 | `douyin` | 短视频 |
| B站 | `bilibili` | 视频、弹幕 |

---

## 九、SearXNG 配置信息

**服务地址**: `http://localhost:12613`
**容器名称**: `boring_colden`
**配置文件**: `~/.docker/config/settings.yml`
**重启命令**: `docker restart boring_colden`

**检查 SearXNG 状态**:
```bash
curl http://localhost:12613/healthz
# 返回: OK
```

**查看所有可用引擎**:
```bash
curl -s http://localhost:12613/config | python3 -c "
import json, sys
data = json.load(sys.stdin)
for e in data.get('engines', [])[:20]:
    if isinstance(e, dict):
        print(f\"{e.get('name')}: enabled={e.get('enabled', 'N/A')}, shortcut={e.get('shortcut', 'N/A')}\")
"
```

