# 国家老龄化研究所阿尔茨海默病遗传学数据存储站点 NIAGADS (National Institute on Aging Genetics of Alzheimer's Disease Data Storage Site) Spider

## 基本信息

- **平台名称**: 国家老龄化研究所阿尔茨海默病遗传学数据存储站点 NIAGADS (National Institute on Aging Genetics of Alzheimer's Disease Data Storage Site)
- **平台URL**: https://www.niagads.org/
- **Spider名称**: 国家老龄化研究所阿尔茨海默病遗传学数据存储站点_niagads_national_institute_on_aging_genetics_of_alzheimers_disease_data_storage_site
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动(infinite_scroll)分页，使用Playwright模拟页面滚动，触发动态加载，直到页面不再加载新内容或达到设定的最大条目数，结合等待网络空闲或元素加载完成判断加载结束。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.page-title, xpath=//h1[contains(@class,'page-title')]` |
| authors | `css=div.authors, xpath=//div[contains(@class,'authors')]` |
| abstract | `css=div.abstract, xpath=//div[contains(@class,'abstract')]` |
| publication_date | `css=span.pub-date, xpath=//span[contains(@class,'pub-date')]` |
| pdf_link | `css=a[href$='.pdf'], xpath=//a[contains(@href,'.pdf')]` |
| supplementary_materials | `css=a.supplementary, xpath=//a[contains(@class,'supplementary')]` |


## 文件下载

对采集到的PDF及补充材料链接，使用Playwright或requests进行文件下载，确保请求头中带上必要的Referer和User-Agent，支持断点续传和重试机制，保存文件时使用有意义的命名规则（如标题+日期）。

## 反爬应对

- Cloudflare防护：使用Playwright的无头浏览器模拟真实用户行为，自动处理JS挑战。
- 合理设置请求间隔，避免短时间内大量请求导致封禁。
- 使用随机User-Agent和代理IP池（如必要）以分散请求来源。

## 注意事项

- 网站无登录需求，减少认证复杂度。
- 无限滚动加载可能导致内存占用较高，需合理控制滚动次数和数据量。
- 部分数据字段可能存在缺失或格式不统一，需做好异常处理。

## 使用方法

```bash
# 运行Spider
scrapy crawl 国家老龄化研究所阿尔茨海默病遗传学数据存储站点_niagads_national_institute_on_aging_genetics_of_alzheimers_disease_data_storage_site

# 限制采集数量（测试用）
scrapy crawl 国家老龄化研究所阿尔茨海默病遗传学数据存储站点_niagads_national_institute_on_aging_genetics_of_alzheimers_disease_data_storage_site -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国家老龄化研究所阿尔茨海默病遗传学数据存储站点_niagads_national_institute_on_aging_genetics_of_alzheimers_disease_data_storage_site -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国家老龄化研究所阿尔茨海默病遗传学数据存储站点_niagads_national_institute_on_aging_genetics_of_alzheimers_disease_data_storage_site_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国家老龄化研究所阿尔茨海默病遗传学数据存储站点_niagads_national_institute_on_aging_genetics_of_alzheimers_disease_data_storage_site_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国家老龄化研究所阿尔茨海默病遗传学数据存储站点_niagads_national_institute_on_aging_genetics_of_alzheimers_disease_data_storage_site/
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

- **生成时间**: 2026-01-18 06:33:56
- **生成工具**: Spider Generator v1.0
