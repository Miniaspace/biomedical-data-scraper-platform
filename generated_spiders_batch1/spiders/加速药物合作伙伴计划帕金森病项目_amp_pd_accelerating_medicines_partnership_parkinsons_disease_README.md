# 加速药物合作伙伴计划帕金森病项目 AMP PD (Accelerating Medicines Partnership Parkinson's Disease) Spider

## 基本信息

- **平台名称**: 加速药物合作伙伴计划帕金森病项目 AMP PD (Accelerating Medicines Partnership Parkinson's Disease)
- **平台URL**: https://amp-pd.org
- **Spider名称**: 加速药物合作伙伴计划帕金森病项目_amp_pd_accelerating_medicines_partnership_parkinsons_disease
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于网站采用无限滚动（infinite_scroll），通过模拟滚动页面触发加载更多内容。Scrapy本身不支持JS渲染，建议结合Splash或Playwright中间件实现页面滚动，或者分析网络请求模拟加载接口实现分页数据抓取。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.page-title::text` |
| authors | `css=.field--name-field-authors .field__item::text` |
| abstract | `css=.field--name-field-abstract .field__item::text` |
| publication_date | `css=.field--name-field-publication-date .field__item::text` |
| pdf_link | `css=a[href$='.pdf']::attr(href)` |
| supplementary_materials | `css=a.supplementary-material::attr(href)` |


## 文件下载

针对PDF及补充材料链接，提取href后使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载，确保文件名和存储路径合理，支持断点续传和重复文件检测。

## 反爬应对

- 设置合理的下载延迟和并发数，避免触发服务器限制
- 使用随机User-Agent和请求头模拟正常浏览器行为
- 监控异常响应，自动重试失败请求

## 注意事项

- 网站无登录和复杂反爬，采集相对简单，但需处理无限滚动加载
- 无检测到API接口，需基于页面HTML解析数据
- 注意PDF及补充材料链接可能为相对路径，需拼接完整URL

## 使用方法

```bash
# 运行Spider
scrapy crawl 加速药物合作伙伴计划帕金森病项目_amp_pd_accelerating_medicines_partnership_parkinsons_disease

# 限制采集数量（测试用）
scrapy crawl 加速药物合作伙伴计划帕金森病项目_amp_pd_accelerating_medicines_partnership_parkinsons_disease -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 加速药物合作伙伴计划帕金森病项目_amp_pd_accelerating_medicines_partnership_parkinsons_disease -o output.jsonl
```

## 输出格式

- JSONL格式: `output/加速药物合作伙伴计划帕金森病项目_amp_pd_accelerating_medicines_partnership_parkinsons_disease_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/加速药物合作伙伴计划帕金森病项目_amp_pd_accelerating_medicines_partnership_parkinsons_disease_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/加速药物合作伙伴计划帕金森病项目_amp_pd_accelerating_medicines_partnership_parkinsons_disease/
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

- **生成时间**: 2026-01-18 06:16:36
- **生成工具**: Spider Generator v1.0
