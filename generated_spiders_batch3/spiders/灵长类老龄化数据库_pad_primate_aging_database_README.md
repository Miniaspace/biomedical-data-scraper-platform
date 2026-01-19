# 灵长类老龄化数据库 PAD (Primate Aging Database) Spider

## 基本信息

- **平台名称**: 灵长类老龄化数据库 PAD (Primate Aging Database)
- **平台URL**: https://primatedatabase.org
- **Spider名称**: 灵长类老龄化数据库_pad_primate_aging_database
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无分页，页面一次性加载所有列表项，直接抓取当前页面所有数据

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li > a.title, ul li > div.title, ul li > h3` |
| author | `ul li span.author, ul li div.author` |
| publication_date | `ul li span.date, ul li div.date` |
| pdf_link | `ul li a[href$='.pdf']` |


## 文件下载

通过playwright模拟点击或直接请求PDF链接进行下载，需携带登录态Cookie，确保权限访问

## 反爬应对

- 模拟真实浏览器环境，使用Playwright自动处理登录，保持会话
- 合理控制请求频率，避免触发服务器异常
- 利用Playwright自动处理JavaScript渲染，确保页面数据完整

## 注意事项

- 必须先完成登录，登录流程需自动化处理，建议使用账号密码自动填充及提交
- 页面无分页，数据量较大时需注意内存和性能优化
- 无API接口，所有数据需从渲染后的HTML中提取

## 使用方法

```bash
# 运行Spider
scrapy crawl 灵长类老龄化数据库_pad_primate_aging_database

# 限制采集数量（测试用）
scrapy crawl 灵长类老龄化数据库_pad_primate_aging_database -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 灵长类老龄化数据库_pad_primate_aging_database -o output.jsonl
```

## 输出格式

- JSONL格式: `output/灵长类老龄化数据库_pad_primate_aging_database_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/灵长类老龄化数据库_pad_primate_aging_database_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/灵长类老龄化数据库_pad_primate_aging_database/
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

- **生成时间**: 2026-01-18 06:44:25
- **生成工具**: Spider Generator v1.0
