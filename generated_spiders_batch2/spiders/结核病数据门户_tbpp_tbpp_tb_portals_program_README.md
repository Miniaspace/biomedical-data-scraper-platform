# 结核病数据门户 TBPP TBPP (TB Portals Program) Spider

## 基本信息

- **平台名称**: 结核病数据门户 TBPP TBPP (TB Portals Program)
- **平台URL**: https://tbportals.niaid.nih.gov
- **Spider名称**: 结核病数据门户_tbpp_tbpp_tb_portals_program
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

无分页，所有数据均在单页面加载，直接解析列表即可，无需分页处理

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a::text` |
| detail_link | `li > a::attr(href)` |


## 文件下载

在详情页中定位PDF及补充材料链接，使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载，确保文件链接完整且可访问

## 反爬应对

- 由于无验证码、无登录、无Cloudflare及无明显限速，建议控制请求频率，避免过快请求导致IP被封
- 设置合理的下载延迟（如1秒）和并发请求数（如8）
- 使用随机User-Agent和请求头模拟正常浏览器访问

## 注意事项

- 确认详情页中PDF及补充材料的链接格式，确保能正确抓取并下载
- 部分链接指向外部域名（如hhs.gov），需处理跨域请求问题
- 页面结构较为简单，无复杂JS渲染，Scrapy足够应对

## 使用方法

```bash
# 运行Spider
scrapy crawl 结核病数据门户_tbpp_tbpp_tb_portals_program

# 限制采集数量（测试用）
scrapy crawl 结核病数据门户_tbpp_tbpp_tb_portals_program -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 结核病数据门户_tbpp_tbpp_tb_portals_program -o output.jsonl
```

## 输出格式

- JSONL格式: `output/结核病数据门户_tbpp_tbpp_tb_portals_program_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/结核病数据门户_tbpp_tbpp_tb_portals_program_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/结核病数据门户_tbpp_tbpp_tb_portals_program/
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

- **生成时间**: 2026-01-18 06:28:53
- **生成工具**: Spider Generator v1.0
