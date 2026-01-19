# 联邦机构创伤性脑损伤研究数据库系统 FITBIR (Federal Interagency Traumatic Brain Injury Research Informatics System) Spider

## 基本信息

- **平台名称**: 联邦机构创伤性脑损伤研究数据库系统 FITBIR (Federal Interagency Traumatic Brain Injury Research Informatics System)
- **平台URL**: https://fitbir.nih.gov/content/access-data
- **Spider名称**: 联邦机构创伤性脑损伤研究数据库系统_fitbir_federal_interagency_traumatic_brain_injury_research_informatics_system
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于页面采用无限滚动(infinite_scroll)加载所有列表项，建议通过分析页面加载机制，模拟滚动触发更多数据加载，或直接请求完整列表页（若无API）。若页面数据一次性加载完毕，则直接采集即可，无需分页处理。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li a::text` |
| detail_url | `ul li a::attr(href)` |


## 文件下载

在详情页中定位PDF文件链接（通常为a标签，href以.pdf结尾），使用Scrapy的文件下载管道或自定义请求下载PDF文件，保存时保持文件名或用唯一ID命名，确保文件完整性。

## 反爬应对

- 无明显反爬机制，保持合理请求频率，避免过快访问。
- 设置User-Agent模拟真实浏览器，避免被简单封禁。
- 使用Scrapy默认的重试和延迟中间件，保证稳定采集。

## 注意事项

- 页面不依赖JavaScript渲染，Scrapy即可完成采集，无需Playwright。
- 确认所有PDF链接均可直接访问，若有权限限制需额外处理。
- 注意列表项中可能存在无效链接或重复数据，需做数据清洗。

## 使用方法

```bash
# 运行Spider
scrapy crawl 联邦机构创伤性脑损伤研究数据库系统_fitbir_federal_interagency_traumatic_brain_injury_research_informatics_system

# 限制采集数量（测试用）
scrapy crawl 联邦机构创伤性脑损伤研究数据库系统_fitbir_federal_interagency_traumatic_brain_injury_research_informatics_system -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 联邦机构创伤性脑损伤研究数据库系统_fitbir_federal_interagency_traumatic_brain_injury_research_informatics_system -o output.jsonl
```

## 输出格式

- JSONL格式: `output/联邦机构创伤性脑损伤研究数据库系统_fitbir_federal_interagency_traumatic_brain_injury_research_informatics_system_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/联邦机构创伤性脑损伤研究数据库系统_fitbir_federal_interagency_traumatic_brain_injury_research_informatics_system_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/联邦机构创伤性脑损伤研究数据库系统_fitbir_federal_interagency_traumatic_brain_injury_research_informatics_system/
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

- **生成时间**: 2026-01-18 06:17:38
- **生成工具**: Spider Generator v1.0
