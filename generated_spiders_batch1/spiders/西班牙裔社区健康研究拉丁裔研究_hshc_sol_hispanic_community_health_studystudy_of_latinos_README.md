# 西班牙裔社区健康研究/拉丁裔研究 HSHC-SOL (Hispanic Community Health Study/Study of Latinos) Spider

## 基本信息

- **平台名称**: 西班牙裔社区健康研究/拉丁裔研究 HSHC-SOL (Hispanic Community Health Study/Study of Latinos)
- **平台URL**: https://biolincc.nhlbi.nih.gov/studies/hchssol/
- **Spider名称**: 西班牙裔社区健康研究拉丁裔研究_hshc_sol_hispanic_community_health_studystudy_of_latinos
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于页面采用无限滚动加载，使用Scrapy结合中间件如 scrapy-splash 或 scrapy-playwright 来模拟滚动加载，或分析XHR请求模拟翻页加载；如果页面无XHR请求，采用Playwright自动滚动触发加载，直到所有数据加载完成后开始采集。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css: h1.page-title, or css: ul li a > text` |
| study_id | `css: ul li span.study-id` |
| description | `css: div.study-description` |
| pdf_links | `css: a[href$='.pdf']` |


## 文件下载

对所有采集到的PDF链接，使用Scrapy的FilesPipeline或自定义下载中间件进行文件下载，确保文件完整性和重试机制；文件命名建议使用研究ID或标题做唯一标识。

## 反爬应对

- 页面无验证码和Cloudflare，反爬较弱，保持合理请求频率避免触发服务器限制
- 设置User-Agent和Referer头模拟浏览器请求
- 使用IP代理池以防止IP封禁（预防性措施）

## 注意事项

- 确保无限滚动加载完全，避免数据截断
- PDF文件链接可能分布在详情页，需先采集详情页链接再访问详情页提取PDF
- 部分字段可能在详情页动态加载，若发现数据缺失，可考虑Playwright辅助渲染

## 使用方法

```bash
# 运行Spider
scrapy crawl 西班牙裔社区健康研究拉丁裔研究_hshc_sol_hispanic_community_health_studystudy_of_latinos

# 限制采集数量（测试用）
scrapy crawl 西班牙裔社区健康研究拉丁裔研究_hshc_sol_hispanic_community_health_studystudy_of_latinos -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 西班牙裔社区健康研究拉丁裔研究_hshc_sol_hispanic_community_health_studystudy_of_latinos -o output.jsonl
```

## 输出格式

- JSONL格式: `output/西班牙裔社区健康研究拉丁裔研究_hshc_sol_hispanic_community_health_studystudy_of_latinos_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/西班牙裔社区健康研究拉丁裔研究_hshc_sol_hispanic_community_health_studystudy_of_latinos_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/西班牙裔社区健康研究拉丁裔研究_hshc_sol_hispanic_community_health_studystudy_of_latinos/
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

- **生成时间**: 2026-01-18 06:12:21
- **生成工具**: Spider Generator v1.0
