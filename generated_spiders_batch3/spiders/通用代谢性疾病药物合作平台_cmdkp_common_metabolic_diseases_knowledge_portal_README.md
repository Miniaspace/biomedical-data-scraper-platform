# 通用代谢性疾病药物合作平台 CMDKP (Common Metabolic Diseases Knowledge Portal) Spider

## 基本信息

- **平台名称**: 通用代谢性疾病药物合作平台 CMDKP (Common Metabolic Diseases Knowledge Portal)
- **平台URL**: https://hugeamp.org
- **Spider名称**: 通用代谢性疾病药物合作平台_cmdkp_common_metabolic_diseases_knowledge_portal
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

由于采用无限滚动(infinite_scroll)分页，使用Playwright模拟页面滚动，等待新内容加载，直到无新数据或达到预设最大条数。通过监听DOM变化或滚动条位置判断加载完成。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li .title, ul li h3, ul li a.title` |
| author | `ul li .author, ul li .meta .author` |
| date | `ul li .date, ul li .meta .date` |
| summary | `ul li .summary, ul li p.summary` |
| pdf_link | `ul li a[href$='.pdf']` |


## 文件下载

对页面中检测到的PDF或补充材料链接，使用Playwright获取完整URL后，通过requests或Playwright的API进行文件下载，支持断点续传和重试机制，保存到指定目录。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免因无头浏览器特征被识别
- 合理控制滚动和请求频率，避免触发速率限制
- 登录环节使用Playwright自动化填写账号密码，保持会话有效
- 使用随机User-Agent和代理IP池（如有必要）

## 注意事项

- 登录必须，需提前准备账号密码，且登录后cookie/session需保持
- 页面大量依赖JavaScript渲染，传统Scrapy无法直接抓取
- 无公开API，所有数据需从前端渲染内容中提取
- 文件下载链接可能动态生成，需在详情页或列表页动态获取

## 使用方法

```bash
# 运行Spider
scrapy crawl 通用代谢性疾病药物合作平台_cmdkp_common_metabolic_diseases_knowledge_portal

# 限制采集数量（测试用）
scrapy crawl 通用代谢性疾病药物合作平台_cmdkp_common_metabolic_diseases_knowledge_portal -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 通用代谢性疾病药物合作平台_cmdkp_common_metabolic_diseases_knowledge_portal -o output.jsonl
```

## 输出格式

- JSONL格式: `output/通用代谢性疾病药物合作平台_cmdkp_common_metabolic_diseases_knowledge_portal_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/通用代谢性疾病药物合作平台_cmdkp_common_metabolic_diseases_knowledge_portal_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/通用代谢性疾病药物合作平台_cmdkp_common_metabolic_diseases_knowledge_portal/
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

- **生成时间**: 2026-01-18 06:37:22
- **生成工具**: Spider Generator v1.0
