# 衰老研究生物样本库 ARB (Aging Research Biobank) Spider

## 基本信息

- **平台名称**: 衰老研究生物样本库 ARB (Aging Research Biobank)
- **平台URL**: https://agingresearchbiobank.nia.nih.gov
- **Spider名称**: 衰老研究生物样本库_arb_aging_research_biobank
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于网站采用无限滚动(infinite_scroll)分页且无API接口，建议通过模拟浏览器滚动行为获取更多数据。考虑到JavaScript执行量较小且无复杂反爬，使用Scrapy结合Splash或Scrapy-Selenium模拟滚动加载，直到无新数据加载为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li > strong, ul li > a, ul li > span` |
| pdf_link | `ul li a[href$='.pdf']` |


## 文件下载

通过解析列表项中PDF文件的直接链接，使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载，确保文件名和路径合理保存。下载前可进行HEAD请求确认文件大小及类型。

## 反爬应对

- 网站无验证码、无登录、无明显速率限制，建议合理设置下载延时和并发数，避免过快请求导致IP封禁。
- 使用随机User-Agent和请求头模拟真实浏览器请求，降低被识别风险。

## 注意事项

- detail_link_pattern为“#”，说明无详情页，所有信息均在列表页内，采集时需充分解析列表页内容。
- 部分数据可能嵌入在文本或HTML标签中，需根据实际HTML结构灵活调整选择器。
- 无限滚动加载数据量较大时，需控制爬取深度和数据量，避免资源浪费。

## 使用方法

```bash
# 运行Spider
scrapy crawl 衰老研究生物样本库_arb_aging_research_biobank

# 限制采集数量（测试用）
scrapy crawl 衰老研究生物样本库_arb_aging_research_biobank -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 衰老研究生物样本库_arb_aging_research_biobank -o output.jsonl
```

## 输出格式

- JSONL格式: `output/衰老研究生物样本库_arb_aging_research_biobank_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/衰老研究生物样本库_arb_aging_research_biobank_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/衰老研究生物样本库_arb_aging_research_biobank/
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

- **生成时间**: 2026-01-18 06:29:17
- **生成工具**: Spider Generator v1.0
