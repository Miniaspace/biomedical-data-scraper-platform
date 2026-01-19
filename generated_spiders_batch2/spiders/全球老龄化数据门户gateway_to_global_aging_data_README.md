# 全球老龄化数据门户GATEWAY TO GLOBAL AGING DATA Spider

## 基本信息

- **平台名称**: 全球老龄化数据门户GATEWAY TO GLOBAL AGING DATA
- **平台URL**: https://g2aging.org/
- **Spider名称**: 全球老龄化数据门户gateway_to_global_aging_data
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动（infinite_scroll）分页，使用Playwright模拟浏览器滚动页面，逐步加载更多内容，直到无新内容加载为止。通过监听网络请求或检测页面中table tbody tr元素数量变化判断加载结束。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `table tbody tr td:nth-child(1) a` |
| authors | `table tbody tr td:nth-child(2)` |
| publication_date | `table tbody tr td:nth-child(3)` |
| pdf_link | `table tbody tr td a[href$='.pdf']` |


## 文件下载

在解析列表或详情页时提取PDF文件链接，使用Playwright获取完整的下载URL后，结合requests或Playwright的API下载PDF文件，支持断点续传和重试机制，确保文件完整性。

## 反爬应对

- 针对网站的验证码机制，建议控制请求频率，模拟正常用户浏览行为，避免触发验证码。
- 使用Playwright的无头浏览器环境，保持合理的User-Agent和浏览器指纹，降低被识别风险。
- 设置适当的等待时间和随机延迟，避免快速连续请求。
- 必要时结合代理IP池轮换IP，防止IP封禁。

## 注意事项

- 网站不提供公开API，且内容通过表格展示，需精准定位表格行和列提取数据。
- 无限滚动分页需要动态加载数据，传统Scrapy不适用，Playwright更合适。
- 验证码可能在异常请求时触发，需设计异常处理和人工干预机制。
- PDF文件下载链接可能是相对路径，需拼接完整URL。

## 使用方法

```bash
# 运行Spider
scrapy crawl 全球老龄化数据门户gateway_to_global_aging_data

# 限制采集数量（测试用）
scrapy crawl 全球老龄化数据门户gateway_to_global_aging_data -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 全球老龄化数据门户gateway_to_global_aging_data -o output.jsonl
```

## 输出格式

- JSONL格式: `output/全球老龄化数据门户gateway_to_global_aging_data_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/全球老龄化数据门户gateway_to_global_aging_data_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/全球老龄化数据门户gateway_to_global_aging_data/
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

- **生成时间**: 2026-01-18 06:21:39
- **生成工具**: Spider Generator v1.0
