# 脑数据科学平台 BDSP (Brain Data Science Platform) Spider

## 基本信息

- **平台名称**: 脑数据科学平台 BDSP (Brain Data Science Platform)
- **平台URL**: https://bdsp.io
- **Spider名称**: 脑数据科学平台_bdsp_brain_data_science_platform
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 16

## 采集策略

网站无分页，所有数据均在单页或通过详情页访问，无需分页处理

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `h1.page-title, div.title, or header h1 (需根据详情页实际结构调整)` |
| author | `div.author, span.author-name (需根据详情页实际结构调整)` |
| abstract | `div.abstract, section.abstract (需根据详情页实际结构调整)` |
| publication_date | `span.pub-date, div.date (需根据详情页实际结构调整)` |
| pdf_link | `a[href$='.pdf']` |
| supplementary_materials | `a.supplementary, a[href*='supplement']` |


## 文件下载

登录后通过Scrapy请求详情页，解析PDF及补充材料链接，使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载，确保携带登录cookie

## 反爬应对

- 使用Scrapy的CookieMiddleware管理登录状态，保持会话
- 设置合理的下载延迟和并发限制，避免触发服务器限制
- 模拟正常浏览器请求头，避免被识别为爬虫

## 注意事项

- 登录认证是采集前提，需实现登录表单提交并保持会话
- 无API接口，需解析HTML，字段选择器需根据详情页实际DOM结构调整
- 文件下载需确保登录态，防止403或重定向至登录页

## 使用方法

```bash
# 运行Spider
scrapy crawl 脑数据科学平台_bdsp_brain_data_science_platform

# 限制采集数量（测试用）
scrapy crawl 脑数据科学平台_bdsp_brain_data_science_platform -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 脑数据科学平台_bdsp_brain_data_science_platform -o output.jsonl
```

## 输出格式

- JSONL格式: `output/脑数据科学平台_bdsp_brain_data_science_platform_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/脑数据科学平台_bdsp_brain_data_science_platform_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/脑数据科学平台_bdsp_brain_data_science_platform/
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

- **生成时间**: 2026-01-18 06:19:50
- **生成工具**: Spider Generator v1.0
