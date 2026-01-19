# 慢性阻塞性肺病遗传流行病学研究 COPDGene (The Genetic Epidemiology of COPD) Spider

## 基本信息

- **平台名称**: 慢性阻塞性肺病遗传流行病学研究 COPDGene (The Genetic Epidemiology of COPD)
- **平台URL**: http://www.copdgene.org/
- **Spider名称**: 慢性阻塞性肺病遗传流行病学研究_copdgene_the_genetic_epidemiology_of_copd
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 8

## 采集策略

无分页，直接采集首页所有列表项，若未来新增分页则需动态检测并调整

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `head > title::text` |
| link | `#site-navigation a::attr(href)` |
| pdf_links | `a[href$='.pdf']::attr(href)` |
| supplementary_materials | `a[href*='supplement']::attr(href)` |


## 文件下载

对采集到的PDF链接进行二次请求下载，保存到本地或云存储，确保文件完整性，使用Scrapy的FilesPipeline或自定义下载中间件

## 反爬应对

- 由于无明显反爬机制，保持适度请求频率避免服务器压力
- 使用合理的User-Agent头模拟浏览器请求

## 注意事项

- 网站无登录和API，数据结构简单，采集稳定性较高
- 需关注未来网站结构变动，尤其导航栏链接选择器

## 使用方法

```bash
# 运行Spider
scrapy crawl 慢性阻塞性肺病遗传流行病学研究_copdgene_the_genetic_epidemiology_of_copd

# 限制采集数量（测试用）
scrapy crawl 慢性阻塞性肺病遗传流行病学研究_copdgene_the_genetic_epidemiology_of_copd -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 慢性阻塞性肺病遗传流行病学研究_copdgene_the_genetic_epidemiology_of_copd -o output.jsonl
```

## 输出格式

- JSONL格式: `output/慢性阻塞性肺病遗传流行病学研究_copdgene_the_genetic_epidemiology_of_copd_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/慢性阻塞性肺病遗传流行病学研究_copdgene_the_genetic_epidemiology_of_copd_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/慢性阻塞性肺病遗传流行病学研究_copdgene_the_genetic_epidemiology_of_copd/
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

- **生成时间**: 2026-01-18 06:14:49
- **生成工具**: Spider Generator v1.0
