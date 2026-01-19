# 营养科学数据与生物样本资源门户 NSDBRP (Nutrition Science Data and Biospecimen Resources Portal) Spider

## 基本信息

- **平台名称**: 营养科学数据与生物样本资源门户 NSDBRP (Nutrition Science Data and Biospecimen Resources Portal)
- **平台URL**: https://dpcpsi.nih.gov/onr/onr-nutrition-science-data-and-biospecimen-resources-portal
- **Spider名称**: 营养科学数据与生物样本资源门户_nsdbrp_nutrition_science_data_and_biospecimen_resources_portal
- **采集方法**: playwright
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于采用无限滚动(infinite scroll)分页，使用Playwright模拟页面滚动，等待新内容加载，直到无新数据加载为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a` |
| description | `li > p, li > div.description` |
| detail_url | `li > a::attr(href)` |
| pdf_links | `a[href$='.pdf']` |


## 文件下载

在详情页或列表页中定位所有PDF链接，使用Playwright拦截下载请求或直接通过requests下载，保存文件时根据标题或唯一ID命名，确保文件完整且无重复。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免触发Cloudflare的反爬机制。
- 设置合理的请求间隔，避免短时间内大量请求导致封禁。
- 使用随机User-Agent和浏览器指纹，模拟真实用户访问。

## 注意事项

- 网站基于Drupal 10，结构相对稳定，但需关注动态加载内容。
- 目标数据中PDF和补充材料链接可能分散在详情页多个位置，需全面提取。
- Cloudflare保护可能导致请求失败，Playwright的无头浏览器模式更适合绕过。

## 使用方法

```bash
# 运行Spider
scrapy crawl 营养科学数据与生物样本资源门户_nsdbrp_nutrition_science_data_and_biospecimen_resources_portal

# 限制采集数量（测试用）
scrapy crawl 营养科学数据与生物样本资源门户_nsdbrp_nutrition_science_data_and_biospecimen_resources_portal -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 营养科学数据与生物样本资源门户_nsdbrp_nutrition_science_data_and_biospecimen_resources_portal -o output.jsonl
```

## 输出格式

- JSONL格式: `output/营养科学数据与生物样本资源门户_nsdbrp_nutrition_science_data_and_biospecimen_resources_portal_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/营养科学数据与生物样本资源门户_nsdbrp_nutrition_science_data_and_biospecimen_resources_portal_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/营养科学数据与生物样本资源门户_nsdbrp_nutrition_science_data_and_biospecimen_resources_portal/
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

- **生成时间**: 2026-01-18 06:27:49
- **生成工具**: Spider Generator v1.0
