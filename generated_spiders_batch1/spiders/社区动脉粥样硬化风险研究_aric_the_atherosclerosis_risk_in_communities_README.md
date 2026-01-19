# 社区动脉粥样硬化风险研究 ARIC (The Atherosclerosis Risk in Communities) Spider

## 基本信息

- **平台名称**: 社区动脉粥样硬化风险研究 ARIC (The Atherosclerosis Risk in Communities)
- **平台URL**: https://www5.cscc.unc.edu/aric9/
- **Spider名称**: 社区动脉粥样硬化风险研究_aric_the_atherosclerosis_risk_in_communities
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于网站采用无限滚动(infinite_scroll)分页，需模拟前端滚动加载行为。使用Scrapy结合中间件或扩展实现自动发送分页请求，或者通过分析网络请求参数构造翻页请求。若前端通过XHR请求加载更多数据，需抓包分析请求参数，模拟请求获取完整列表数据。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a::text` |
| detail_url | `li > a::attr(href)` |


## 文件下载

在详情页中定位所有指向xml文件的链接（如a标签href以.xml结尾），使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载，确保文件保存路径和命名规范。支持断点续传和重试机制。

## 反爬应对

- 合理设置下载延迟，避免过快请求导致服务器封禁
- 使用随机User-Agent和IP代理池分散请求来源
- 监控请求失败率，自动调整请求频率

## 注意事项

- 网站不需要登录且无复杂反爬机制，采集难度较低
- 无限滚动分页需重点解决，确保数据完整采集
- 需确认详情页中所有目标文件链接均可直接访问下载

## 使用方法

```bash
# 运行Spider
scrapy crawl 社区动脉粥样硬化风险研究_aric_the_atherosclerosis_risk_in_communities

# 限制采集数量（测试用）
scrapy crawl 社区动脉粥样硬化风险研究_aric_the_atherosclerosis_risk_in_communities -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 社区动脉粥样硬化风险研究_aric_the_atherosclerosis_risk_in_communities -o output.jsonl
```

## 输出格式

- JSONL格式: `output/社区动脉粥样硬化风险研究_aric_the_atherosclerosis_risk_in_communities_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/社区动脉粥样硬化风险研究_aric_the_atherosclerosis_risk_in_communities_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/社区动脉粥样硬化风险研究_aric_the_atherosclerosis_risk_in_communities/
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

- **生成时间**: 2026-01-18 06:11:06
- **生成工具**: Spider Generator v1.0
