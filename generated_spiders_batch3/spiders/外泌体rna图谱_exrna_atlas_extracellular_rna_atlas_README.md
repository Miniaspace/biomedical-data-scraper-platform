# 外泌体RNA图谱 exRNA Atlas (Extracellular RNA Atlas) Spider

## 基本信息

- **平台名称**: 外泌体RNA图谱 exRNA Atlas (Extracellular RNA Atlas)
- **平台URL**: https://exrna.org
- **Spider名称**: 外泌体rna图谱_exrna_atlas_extracellular_rna_atlas
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 12

## 采集策略

由于网站采用无限滚动（infinite_scroll），通过模拟页面滚动触发加载更多内容。Scrapy本身不支持JS渲染，建议结合Splash或Playwright中间件实现滚动加载，或分析网络请求模拟分页参数请求数据。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.article-title, xpath=//h1[contains(@class,'article-title')]` |
| authors | `css=div.authors-list, xpath=//div[contains(@class,'authors-list')]` |
| abstract | `css=div.abstract, xpath=//div[contains(@class,'abstract')]` |
| publication_date | `css=div.pub-date, xpath=//div[contains(@class,'pub-date')]` |
| pdf_link | `xpath=//a[contains(text(),'PDF') or contains(@href,'.pdf')]/@href` |
| supplementary_materials | `xpath=//a[contains(text(),'Supplementary') or contains(text(),'Supplemental')]/@href` |


## 文件下载

解析详情页中PDF及补充材料链接，使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载，确保链接为绝对URL，若为相对路径则拼接域名。

## 反爬应对

- 设置合理的下载延迟和并发数，避免过快请求导致封禁
- 使用随机User-Agent和请求头模拟正常浏览器行为
- 监控请求失败率，自动重试失败请求

## 注意事项

- 网站无登录和复杂反爬，采集难度较低，但需处理无限滚动加载
- 无检测到API接口，需基于页面解析数据
- 文件下载链接需确认是否直接可访问，避免跳转或权限限制

## 使用方法

```bash
# 运行Spider
scrapy crawl 外泌体rna图谱_exrna_atlas_extracellular_rna_atlas

# 限制采集数量（测试用）
scrapy crawl 外泌体rna图谱_exrna_atlas_extracellular_rna_atlas -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 外泌体rna图谱_exrna_atlas_extracellular_rna_atlas -o output.jsonl
```

## 输出格式

- JSONL格式: `output/外泌体rna图谱_exrna_atlas_extracellular_rna_atlas_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/外泌体rna图谱_exrna_atlas_extracellular_rna_atlas_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/外泌体rna图谱_exrna_atlas_extracellular_rna_atlas/
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

- **生成时间**: 2026-01-18 06:40:19
- **生成工具**: Spider Generator v1.0
