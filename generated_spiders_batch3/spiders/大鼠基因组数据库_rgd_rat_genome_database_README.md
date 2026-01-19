# 大鼠基因组数据库 RGD (Rat Genome Database) Spider

## 基本信息

- **平台名称**: 大鼠基因组数据库 RGD (Rat Genome Database)
- **平台URL**: https://rgd.mcw.edu
- **Spider名称**: 大鼠基因组数据库_rgd_rat_genome_database
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于网站采用无限滚动（infinite_scroll）分页，需使用Playwright模拟浏览器滚动页面，等待新数据加载，直到页面底部无新内容加载为止。通过监听网络请求或DOM变化判断加载完成。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `td:nth-child(1) a` |
| authors | `td:nth-child(2)` |
| publication_date | `td:nth-child(3)` |
| journal | `td:nth-child(4)` |
| pdf_link | `td:nth-child(1) a[href$='.pdf']` |


## 文件下载

通过提取PDF文件链接（通常在a标签href中以.pdf结尾），使用Playwright或requests库进行文件下载。确保下载时带上必要的请求头（如Referer）以防止防盗链。

## 反爬应对

- 使用Playwright模拟真实浏览器，绕过Cloudflare防护。
- 设置合理的请求间隔，避免触发速率限制。
- 使用随机User-Agent和代理IP池（如必要）增加请求多样性。

## 注意事项

- 网站不需要登录，简化采集流程。
- 无检测到API，需通过页面解析获取数据。
- 无限滚动可能导致大量数据加载，需控制滚动次数和数据量，避免内存溢出。

## 使用方法

```bash
# 运行Spider
scrapy crawl 大鼠基因组数据库_rgd_rat_genome_database

# 限制采集数量（测试用）
scrapy crawl 大鼠基因组数据库_rgd_rat_genome_database -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 大鼠基因组数据库_rgd_rat_genome_database -o output.jsonl
```

## 输出格式

- JSONL格式: `output/大鼠基因组数据库_rgd_rat_genome_database_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/大鼠基因组数据库_rgd_rat_genome_database_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/大鼠基因组数据库_rgd_rat_genome_database/
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

- **生成时间**: 2026-01-18 06:35:25
- **生成工具**: Spider Generator v1.0
