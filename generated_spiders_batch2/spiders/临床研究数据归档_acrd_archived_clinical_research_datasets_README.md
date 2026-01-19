# 临床研究数据归档 ACRD (Archived Clinical Research Datasets) Spider

## 基本信息

- **平台名称**: 临床研究数据归档 ACRD (Archived Clinical Research Datasets)
- **平台URL**: https://ninds.nih.gov/current-research/research-funded-ninds/clinical-research/archived-clinical-research-datasets
- **Spider名称**: 临床研究数据归档_acrd_archived_clinical_research_datasets
- **采集方法**: scrapy
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 16

## 采集策略

无分页，页面内容无法访问，需先解决403 Forbidden访问限制问题

## 数据字段

暂无字段信息

## 文件下载

待页面正常访问后，根据页面中PDF及补充材料链接，使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载

## 反爬应对

- 403 Forbidden可能由IP封禁或User-Agent限制导致，尝试更换User-Agent模拟浏览器
- 使用代理IP池避免单IP访问频率过高
- 添加合理的请求间隔，避免触发服务器安全策略
- 检查请求头，模拟浏览器完整请求头信息

## 注意事项

- 当前页面返回403 Forbidden，需确认是否有地理位置限制或IP限制
- 无API接口，且页面无分页，采集难度较大
- 页面无JavaScript渲染需求，故无需Playwright
- 需联系网站管理员确认数据开放政策及访问权限

## 使用方法

```bash
# 运行Spider
scrapy crawl 临床研究数据归档_acrd_archived_clinical_research_datasets

# 限制采集数量（测试用）
scrapy crawl 临床研究数据归档_acrd_archived_clinical_research_datasets -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 临床研究数据归档_acrd_archived_clinical_research_datasets -o output.jsonl
```

## 输出格式

- JSONL格式: `output/临床研究数据归档_acrd_archived_clinical_research_datasets_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/临床研究数据归档_acrd_archived_clinical_research_datasets_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/临床研究数据归档_acrd_archived_clinical_research_datasets/
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

- **生成时间**: 2026-01-18 06:28:36
- **生成工具**: Spider Generator v1.0
