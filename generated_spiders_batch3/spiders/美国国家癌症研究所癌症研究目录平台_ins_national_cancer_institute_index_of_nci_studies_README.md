# 美国国家癌症研究所癌症研究目录平台 INS (National Cancer Institute Index of NCI Studies) Spider

## 基本信息

- **平台名称**: 美国国家癌症研究所癌症研究目录平台 INS (National Cancer Institute Index of NCI Studies)
- **平台URL**: https://studycatalog.cancer.gov
- **Spider名称**: 美国国家癌症研究所癌症研究目录平台_ins_national_cancer_institute_index_of_nci_studies
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

采用Playwright模拟用户滚动页面，触发页面的infinite scroll机制，等待新内容加载完成后继续提取，直到无新内容加载为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.study-title, xpath=//h1[contains(@class,'study-title')]` |
| authors | `css=div.authors, xpath=//div[contains(@class,'authors')]` |
| publication_date | `css=span.pub-date, xpath=//span[contains(@class,'pub-date')]` |
| abstract | `css=div.abstract, xpath=//div[contains(@class,'abstract')]` |
| pdf_link | `css=a[href$='.pdf'], xpath=//a[contains(@href,'.pdf')]` |


## 文件下载

通过Playwright拦截PDF链接请求，或直接抓取PDF链接并使用HTTP客户端下载，确保文件完整性和重试机制。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，加载JavaScript，避免因无JS环境导致内容缺失。
- 控制请求频率，模拟人类浏览节奏，避免触发潜在的速率限制。
- 设置合理的User-Agent和浏览器头信息，防止被简单的UA检测屏蔽。

## 注意事项

- 页面采用hash路由（#/home），需处理单页应用的动态内容加载。
- 无公开API，需完全依赖前端渲染数据，确保Playwright等待数据加载完成。
- PDF文件链接可能动态生成，需动态解析页面元素获取最新链接。

## 使用方法

```bash
# 运行Spider
scrapy crawl 美国国家癌症研究所癌症研究目录平台_ins_national_cancer_institute_index_of_nci_studies

# 限制采集数量（测试用）
scrapy crawl 美国国家癌症研究所癌症研究目录平台_ins_national_cancer_institute_index_of_nci_studies -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 美国国家癌症研究所癌症研究目录平台_ins_national_cancer_institute_index_of_nci_studies -o output.jsonl
```

## 输出格式

- JSONL格式: `output/美国国家癌症研究所癌症研究目录平台_ins_national_cancer_institute_index_of_nci_studies_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/美国国家癌症研究所癌症研究目录平台_ins_national_cancer_institute_index_of_nci_studies_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/美国国家癌症研究所癌症研究目录平台_ins_national_cancer_institute_index_of_nci_studies/
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

- **生成时间**: 2026-01-18 06:34:56
- **生成工具**: Spider Generator v1.0
