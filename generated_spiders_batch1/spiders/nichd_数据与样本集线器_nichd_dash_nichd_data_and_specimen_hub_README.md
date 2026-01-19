# NICHD 数据与样本集线器 NICHD DASH (NICHD Data and Specimen Hub) Spider

## 基本信息

- **平台名称**: NICHD 数据与样本集线器 NICHD DASH (NICHD Data and Specimen Hub)
- **平台URL**: https://dash.nichd.nih.gov
- **Spider名称**: nichd_数据与样本集线器_nichd_dash_nichd_data_and_specimen_hub
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 8

## 采集策略

无分页，所有数据均在单一页面内加载，无需分页处理。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a::text` |
| detail_url | `li > a::attr(href)` |


## 文件下载

在详情页中定位PDF或补充材料链接，使用Scrapy的文件下载管道进行下载，确保链接为绝对路径，若为相对路径则拼接完整URL后下载。

## 反爬应对

- 由于无验证码、无登录、无JavaScript渲染及无Cloudflare防护，反爬机制较弱，建议合理设置下载延时和并发数，避免过快请求导致服务器封禁。
- 使用随机User-Agent和请求头模拟正常浏览器访问，防止被简单的UA检测拦截。

## 注意事项

- 详情页链接指向外部域名https://www.hhs.gov/，需确保跨域请求时处理好请求头和Cookies（如有）以保证访问成功。
- 部分文件可能需要额外权限或特殊请求头，需在测试阶段确认文件下载的可行性。
- Drupal 10网站结构稳定，CSS选择器较为可靠，但需关注未来页面结构变化。

## 使用方法

```bash
# 运行Spider
scrapy crawl nichd_数据与样本集线器_nichd_dash_nichd_data_and_specimen_hub

# 限制采集数量（测试用）
scrapy crawl nichd_数据与样本集线器_nichd_dash_nichd_data_and_specimen_hub -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl nichd_数据与样本集线器_nichd_dash_nichd_data_and_specimen_hub -o output.jsonl
```

## 输出格式

- JSONL格式: `output/nichd_数据与样本集线器_nichd_dash_nichd_data_and_specimen_hub_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/nichd_数据与样本集线器_nichd_dash_nichd_data_and_specimen_hub_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/nichd_数据与样本集线器_nichd_dash_nichd_data_and_specimen_hub/
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

- **生成时间**: 2026-01-18 06:18:09
- **生成工具**: Spider Generator v1.0
