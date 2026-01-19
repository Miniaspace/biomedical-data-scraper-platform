# 面部发育数据库平台 FB FB (FaceBase Database Platform) Spider

## 基本信息

- **平台名称**: 面部发育数据库平台 FB FB (FaceBase Database Platform)
- **平台URL**: https://facebase.org
- **Spider名称**: 面部发育数据库平台_fb_fb_facebase_database_platform
- **采集方法**: playwright
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

无分页，直接采集首页所有列表项；若未来出现分页，需动态检测分页按钮并通过Playwright点击加载更多

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `h1.article-title, h2.title, header h1` |
| author | `.author-name, .authors li, .byline` |
| publication_date | `.pub-date, time[datetime]` |
| abstract | `.abstract, .summary, #abstract` |
| pdf_link | `a[href$='.pdf']` |
| supplementary_materials | `a[href*='supplementary'], a[href*='supplemental']` |


## 文件下载

通过Playwright捕获页面中所有PDF及补充材料链接，使用requests或Playwright直接下载，确保文件完整性，支持断点续传

## 反爬应对

- 使用Playwright模拟真实浏览器环境，执行JavaScript，绕过JS渲染限制
- 控制请求频率，避免触发潜在的速率限制
- 设置合理的User-Agent和Headers，模拟正常用户访问

## 注意事项

- 网站无登录和验证码，采集门槛较低
- 需重点关注JavaScript渲染内容，纯Scrapy无法直接采集
- 注意PDF及补充材料链接可能分散在不同页面或动态加载

## 使用方法

```bash
# 运行Spider
scrapy crawl 面部发育数据库平台_fb_fb_facebase_database_platform

# 限制采集数量（测试用）
scrapy crawl 面部发育数据库平台_fb_fb_facebase_database_platform -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 面部发育数据库平台_fb_fb_facebase_database_platform -o output.jsonl
```

## 输出格式

- JSONL格式: `output/面部发育数据库平台_fb_fb_facebase_database_platform_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/面部发育数据库平台_fb_fb_facebase_database_platform_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/面部发育数据库平台_fb_fb_facebase_database_platform/
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

- **生成时间**: 2026-01-18 06:32:09
- **生成工具**: Spider Generator v1.0
