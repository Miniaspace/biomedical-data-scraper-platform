# NIH数据共享云计划 NIH DC (NIH Data Commons) Spider

## 基本信息

- **平台名称**: NIH数据共享云计划 NIH DC (NIH Data Commons)
- **平台URL**: https://commonfund.nih.gov/commons
- **Spider名称**: nih数据共享云计划_nih_dc_nih_data_commons
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

无分页，页面一次性加载所有列表项，直接抓取全部li元素即可，无需额外分页处理。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a::text` |
| detail_url | `li > a::attr(href)` |
| description | `li > p::text` |
| pdf_links | `a[href$='.pdf']::attr(href)` |
| supplementary_materials | `a.supplementary-material::attr(href)` |


## 文件下载

针对PDF及补充材料链接，使用Scrapy的FilesPipeline或自定义下载中间件进行文件下载，确保文件完整性和重试机制。

## 反爬应对

- 由于网站使用Cloudflare，建议设置合理的下载延迟和并发限制，模拟正常用户访问频率。
- 使用Scrapy自带的User-Agent中间件，随机切换User-Agent，避免被简单封禁。
- 开启自动重试机制，处理因Cloudflare防护导致的偶发请求失败。

## 注意事项

- 网站基于Drupal 10构建，结构相对稳定，CSS选择器较为可靠。
- 无登录和动态加载需求，Scrapy即可满足采集需求，无需Playwright。
- 注意采集时尊重robots.txt及网站使用条款，避免过度请求。

## 使用方法

```bash
# 运行Spider
scrapy crawl nih数据共享云计划_nih_dc_nih_data_commons

# 限制采集数量（测试用）
scrapy crawl nih数据共享云计划_nih_dc_nih_data_commons -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl nih数据共享云计划_nih_dc_nih_data_commons -o output.jsonl
```

## 输出格式

- JSONL格式: `output/nih数据共享云计划_nih_dc_nih_data_commons_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/nih数据共享云计划_nih_dc_nih_data_commons_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/nih数据共享云计划_nih_dc_nih_data_commons/
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

- **生成时间**: 2026-01-18 06:21:17
- **生成工具**: Spider Generator v1.0
