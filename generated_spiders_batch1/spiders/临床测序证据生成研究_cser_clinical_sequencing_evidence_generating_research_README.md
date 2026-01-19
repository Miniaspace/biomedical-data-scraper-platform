# 临床测序证据生成研究 CSER (Clinical Sequencing Evidence-Generating Research) Spider

## 基本信息

- **平台名称**: 临床测序证据生成研究 CSER (Clinical Sequencing Evidence-Generating Research)
- **平台URL**: https://genome.gov/Funded-Programs-Projects/CSER
- **Spider名称**: 临床测序证据生成研究_cser_clinical_sequencing_evidence_generating_research
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于页面采用无限滚动加载，使用Scrapy结合Splash或Playwright模拟滚动加载，直到加载完所有列表项，或者通过分析网络请求模拟分页参数进行请求，若无API则采用自动滚动加载方式。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a::text` |
| detail_url | `li > a::attr(href)` |


## 文件下载

在详情页中解析所有PDF及补充材料链接，使用Scrapy的文件下载管道进行下载，确保文件链接为绝对路径，支持断点续传和重试机制。

## 反爬应对

- 控制请求频率，避免过快请求导致封禁
- 设置合理User-Agent，模拟真实浏览器
- 使用IP代理池以防止IP被封禁

## 注意事项

- 页面不依赖JavaScript渲染核心内容，Scrapy即可满足需求
- 无限滚动需结合浏览器模拟或Splash，增加开发复杂度
- 无登录和验证码，降低反爬难度

## 使用方法

```bash
# 运行Spider
scrapy crawl 临床测序证据生成研究_cser_clinical_sequencing_evidence_generating_research

# 限制采集数量（测试用）
scrapy crawl 临床测序证据生成研究_cser_clinical_sequencing_evidence_generating_research -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 临床测序证据生成研究_cser_clinical_sequencing_evidence_generating_research -o output.jsonl
```

## 输出格式

- JSONL格式: `output/临床测序证据生成研究_cser_clinical_sequencing_evidence_generating_research_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/临床测序证据生成研究_cser_clinical_sequencing_evidence_generating_research_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/临床测序证据生成研究_cser_clinical_sequencing_evidence_generating_research/
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

- **生成时间**: 2026-01-18 06:17:52
- **生成工具**: Spider Generator v1.0
