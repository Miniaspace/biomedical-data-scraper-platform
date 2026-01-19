# 美国国家癌症研究所试验性新药数据库 NCI-IND (NCI Investigational New Drug Database) Spider

## 基本信息

- **平台名称**: 美国国家癌症研究所试验性新药数据库 NCI-IND (NCI Investigational New Drug Database)
- **平台URL**: https://cipinddirectory.cancer.gov
- **Spider名称**: 美国国家癌症研究所试验性新药数据库_nci_ind_nci_investigational_new_drug_database
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

网站无分页，所有数据在单一页面的表格中加载，直接抓取全部表格行即可，无需分页处理。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| study_title | `table tbody tr td:nth-child(1)` |
| study_id | `table tbody tr td:nth-child(2)` |
| status | `table tbody tr td:nth-child(3)` |
| phase | `table tbody tr td:nth-child(4)` |
| study_type | `table tbody tr td:nth-child(5)` |
| start_date | `table tbody tr td:nth-child(6)` |
| completion_date | `table tbody tr td:nth-child(7)` |
| detail_link | `table tbody tr td a[href^='https://pubmed.ncbi.nlm.nih.gov/']::attr(href)` |


## 文件下载

页面未检测到直接的PDF或补充材料下载链接。若详情页或外部链接（如PubMed）提供PDF文件，需在详情页解析对应下载链接后使用Scrapy的文件下载管道或requests下载文件。

## 反爬应对

- 由于无验证码、无JavaScript渲染、无Cloudflare保护，建议控制请求频率，避免过快访问导致IP被封。
- 设置合理的下载延迟和并发数，模拟正常用户访问。
- 使用随机User-Agent切换，防止简单的UA封禁。

## 注意事项

- 详情链接指向外部PubMed网站，需额外处理跨域请求和数据抓取。
- 部分数据字段可能为空或格式不统一，需做好数据清洗和异常处理。
- 若后续发现详情页含有PDF或补充材料，需动态扩展文件下载逻辑。

## 使用方法

```bash
# 运行Spider
scrapy crawl 美国国家癌症研究所试验性新药数据库_nci_ind_nci_investigational_new_drug_database

# 限制采集数量（测试用）
scrapy crawl 美国国家癌症研究所试验性新药数据库_nci_ind_nci_investigational_new_drug_database -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 美国国家癌症研究所试验性新药数据库_nci_ind_nci_investigational_new_drug_database -o output.jsonl
```

## 输出格式

- JSONL格式: `output/美国国家癌症研究所试验性新药数据库_nci_ind_nci_investigational_new_drug_database_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/美国国家癌症研究所试验性新药数据库_nci_ind_nci_investigational_new_drug_database_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/美国国家癌症研究所试验性新药数据库_nci_ind_nci_investigational_new_drug_database/
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

- **生成时间**: 2026-01-18 06:30:20
- **生成工具**: Spider Generator v1.0
