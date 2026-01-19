# 伊芙分析 EA (Eve Analytics) Spider

## 基本信息

- **平台名称**: 伊芙分析 EA (Eve Analytics)
- **平台URL**: https://eveanalytics.com
- **Spider名称**: 伊芙分析_ea_eve_analytics
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动分页，使用Playwright模拟用户滚动页面，等待新数据加载完成后继续滚动，直到加载完全部数据或达到预设的最大条数。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li div.title` |
| author | `ul li div.author` |
| date | `ul li div.date` |
| summary | `ul li div.summary` |


## 文件下载

在数据项中检测PDF文件或补充材料的下载链接，使用Playwright模拟点击或直接请求文件URL进行下载，需保持登录状态和cookie，支持断点续传和重试机制。

## 反爬应对

- 使用Playwright保证JavaScript渲染，模拟真实浏览器行为，避免因无JS渲染导致数据缺失。
- 保持登录状态，使用cookie/session持久化，避免频繁登录触发安全检测。
- 控制滚动和请求频率，模拟正常用户行为，防止触发潜在的速率限制。

## 注意事项

- 网站无公开API，需全程模拟浏览器操作完成数据加载和交互。
- 登录流程复杂，需提前准备账号密码，处理可能的登录验证码或多因素认证。
- 无限滚动可能导致内存占用较高，需设计合理的分批处理和数据存储方案。

## 使用方法

```bash
# 运行Spider
scrapy crawl 伊芙分析_ea_eve_analytics

# 限制采集数量（测试用）
scrapy crawl 伊芙分析_ea_eve_analytics -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 伊芙分析_ea_eve_analytics -o output.jsonl
```

## 输出格式

- JSONL格式: `output/伊芙分析_ea_eve_analytics_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/伊芙分析_ea_eve_analytics_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/伊芙分析_ea_eve_analytics/
├── main_file/
│   └── {track_id}.pdf
├── SI_file/
│   └── {track_id}/
│       ├── sup_1.pdf
│       └── sup_2.xlsx
├── PR_file/
│   └── {track_id}/
│       └── pr_1.pdf
└── images/
    └── {track_id}/
        └── {sha256}.png
```

## 生成信息

- **生成时间**: 2026-01-18 06:43:37
- **生成工具**: Spider Generator v1.0
