# 全球阿尔茨海默病协会互动网络 GAAIN (Global Alzheimer’s Association Interactive Network) Spider

## 基本信息

- **平台名称**: 全球阿尔茨海默病协会互动网络 GAAIN (Global Alzheimer’s Association Interactive Network)
- **平台URL**: https://gaaindata.org
- **Spider名称**: 全球阿尔茨海默病协会互动网络_gaain_global_alzheimers_association_interactive_network
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

网站无分页，所有数据在单页面或通过筛选加载，直接采集当前页面所有列表项，无需分页处理。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `h1.page-title, div.detail-header > h1` |
| author | `div.authors > span.author-name` |
| publication_date | `div.pub-date` |
| abstract | `div.abstract` |
| pdf_link | `a[href$='.pdf']` |
| supplementary_materials | `a.supplementary-download` |


## 文件下载

检测页面中所有PDF及补充材料下载链接，使用Scrapy的FilesPipeline或自定义下载中间件批量下载，确保链接完整性和重试机制。

## 反爬应对

- 合理设置下载延迟，避免短时间内大量请求导致IP封禁
- 使用随机User-Agent池，模拟多浏览器请求头
- 监控异常响应，自动重试失败请求

## 注意事项

- 网站无登录和JavaScript渲染，Scrapy即可满足需求
- 需确认所有数据是否均在HTML中，若部分数据通过异步请求加载，需进一步分析接口
- 确保下载文件链接有效，避免断链

## 使用方法

```bash
# 运行Spider
scrapy crawl 全球阿尔茨海默病协会互动网络_gaain_global_alzheimers_association_interactive_network

# 限制采集数量（测试用）
scrapy crawl 全球阿尔茨海默病协会互动网络_gaain_global_alzheimers_association_interactive_network -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 全球阿尔茨海默病协会互动网络_gaain_global_alzheimers_association_interactive_network -o output.jsonl
```

## 输出格式

- JSONL格式: `output/全球阿尔茨海默病协会互动网络_gaain_global_alzheimers_association_interactive_network_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/全球阿尔茨海默病协会互动网络_gaain_global_alzheimers_association_interactive_network_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/全球阿尔茨海默病协会互动网络_gaain_global_alzheimers_association_interactive_network/
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

- **生成时间**: 2026-01-18 06:36:06
- **生成工具**: Spider Generator v1.0
