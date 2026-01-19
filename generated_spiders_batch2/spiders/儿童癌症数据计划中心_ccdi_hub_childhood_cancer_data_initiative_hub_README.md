# 儿童癌症数据计划中心 CCDI Hub (Childhood Cancer Data Initiative Hub) Spider

## 基本信息

- **平台名称**: 儿童癌症数据计划中心 CCDI Hub (Childhood Cancer Data Initiative Hub)
- **平台URL**: https://ccdi.cancer.gov/home
- **Spider名称**: 儿童癌症数据计划中心_ccdi_hub_childhood_cancer_data_initiative_hub
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 16

## 采集策略

采用Playwright模拟浏览器自动滚动页面，触发infinite scroll加载更多内容。通过监听页面DOM变化或定时滚动到底部，直到无新内容加载为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1, xpath=//h1` |
| author | `css=.author, xpath=//*[contains(@class, 'author')]` |
| publication_date | `css=.pub-date, xpath=//*[contains(@class, 'pub-date')]` |
| abstract | `css=.abstract, xpath=//*[contains(@class, 'abstract')]` |
| pdf_link | `css=a[href$='.pdf'], xpath=//a[contains(@href, '.pdf')]` |
| supplementary_materials | `css=a.supplementary, xpath=//a[contains(@class, 'supplementary')]` |


## 文件下载

对页面中所有PDF链接和补充材料链接进行提取，使用Playwright或requests结合cookie/session头部进行文件下载，确保文件完整。支持断点续传和重试机制。

## 反爬应对

- 使用Playwright模拟真实浏览器环境，执行JavaScript，避免因无JS执行导致页面内容缺失
- 控制请求频率，避免触发潜在的速率限制
- 设置合理User-Agent和Headers，模拟真实用户访问
- 启用代理池以防IP封禁（虽然当前无明显限制，但预防性措施）

## 注意事项

- 网站无登录，无API，且数据通过JavaScript动态加载，必须使用支持JS渲染的工具
- 分页为无限滚动，需精确控制滚动触发加载，避免漏采或重复采集
- PDF和补充材料链接可能分散在详情页不同位置，需全面提取
- 部分字段可能缺失或格式不统一，需容错处理

## 使用方法

```bash
# 运行Spider
scrapy crawl 儿童癌症数据计划中心_ccdi_hub_childhood_cancer_data_initiative_hub

# 限制采集数量（测试用）
scrapy crawl 儿童癌症数据计划中心_ccdi_hub_childhood_cancer_data_initiative_hub -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 儿童癌症数据计划中心_ccdi_hub_childhood_cancer_data_initiative_hub -o output.jsonl
```

## 输出格式

- JSONL格式: `output/儿童癌症数据计划中心_ccdi_hub_childhood_cancer_data_initiative_hub_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/儿童癌症数据计划中心_ccdi_hub_childhood_cancer_data_initiative_hub_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/儿童癌症数据计划中心_ccdi_hub_childhood_cancer_data_initiative_hub/
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

- **生成时间**: 2026-01-18 06:24:23
- **生成工具**: Spider Generator v1.0
