# 人口研究数据共享平台 DSDR (Data Sharing for Demographic Research) Spider

## 基本信息

- **平台名称**: 人口研究数据共享平台 DSDR (Data Sharing for Demographic Research)
- **平台URL**: https://icpsr.umich.edu/web/pages/DSDR/discover.html
- **Spider名称**: 人口研究数据共享平台_dsdr_data_sharing_for_demographic_research
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

采用Playwright模拟用户滚动页面触发infinite scroll加载更多数据，直到页面不再加载新内容或达到预设最大条数。通过监听网络请求和DOM变化判断加载完成。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.study-title, xpath=//h1[contains(@class,'study-title')]` |
| author | `css=div.author-list span.author-name, xpath=//div[contains(@class,'author-list')]//span[contains(@class,'author-name')]` |
| publication_date | `css=div.pub-date, xpath=//div[contains(@class,'pub-date')]` |
| abstract | `css=section.abstract, xpath=//section[contains(@class,'abstract')]` |
| pdf_links | `css=a[href$='.pdf'], xpath=//a[contains(@href,'.pdf')]` |
| supplementary_materials | `css=a.supplementary-material, xpath=//a[contains(@class,'supplementary-material')]` |


## 文件下载

在详情页解析所有PDF及补充材料链接，使用Playwright获取真实下载链接后，结合cookie和登录状态通过requests或Playwright下载文件，支持断点续传和重试机制。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免被Cloudflare拦截
- 保持登录状态，定期刷新cookie，防止会话过期
- 控制请求频率，模拟人类操作节奏，避免触发反爬机制

## 注意事项

- 登录流程复杂，需实现自动化登录并处理多因素认证（如有）
- 无公开API，所有数据需通过页面渲染获取
- 页面JavaScript渲染较多，纯Scrapy难以完成，必须使用Playwright

## 使用方法

```bash
# 运行Spider
scrapy crawl 人口研究数据共享平台_dsdr_data_sharing_for_demographic_research

# 限制采集数量（测试用）
scrapy crawl 人口研究数据共享平台_dsdr_data_sharing_for_demographic_research -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 人口研究数据共享平台_dsdr_data_sharing_for_demographic_research -o output.jsonl
```

## 输出格式

- JSONL格式: `output/人口研究数据共享平台_dsdr_data_sharing_for_demographic_research_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/人口研究数据共享平台_dsdr_data_sharing_for_demographic_research_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/人口研究数据共享平台_dsdr_data_sharing_for_demographic_research/
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

- **生成时间**: 2026-01-18 06:14:05
- **生成工具**: Spider Generator v1.0
