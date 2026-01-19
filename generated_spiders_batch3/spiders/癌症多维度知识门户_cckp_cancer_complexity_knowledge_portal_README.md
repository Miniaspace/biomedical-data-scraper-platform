# 癌症多维度知识门户 CCKP (Cancer Complexity Knowledge Portal) Spider

## 基本信息

- **平台名称**: 癌症多维度知识门户 CCKP (Cancer Complexity Knowledge Portal)
- **平台URL**: https://cancercomplexity.synapse.org
- **Spider名称**: 癌症多维度知识门户_cckp_cancer_complexity_knowledge_portal
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

使用Playwright模拟用户滚动页面触发无限加载，监听网络请求确保数据加载完成后再提取，直到无新数据加载为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `h2.dataset-title` |
| author | `span.dataset-author` |
| publication_date | `span.dataset-date` |
| description | `div.dataset-description` |
| pdf_links | `a[href$='.pdf']` |
| supplementary_materials | `a.supplementary-download` |


## 文件下载

通过Playwright捕获文件下载链接，使用会话cookie和授权头部进行文件请求，确保登录状态下下载所有PDF及补充材料，支持断点续传和重试机制。

## 反爬应对

- 模拟真实用户行为，设置合理的滚动间隔和随机等待时间，避免触发异常
- 保持登录状态，定期刷新token或重新登录，防止会话失效
- 限制并发请求数，避免过快访问导致账号封禁

## 注意事项

- 网站需要登录，需实现自动登录流程并管理cookie/session
- 无公开API，所有数据需通过页面渲染抓取
- 无限滚动分页需精准判断数据加载结束，避免遗漏或重复采集
- 文件下载需处理大文件和断点续传，保证数据完整性

## 使用方法

```bash
# 运行Spider
scrapy crawl 癌症多维度知识门户_cckp_cancer_complexity_knowledge_portal

# 限制采集数量（测试用）
scrapy crawl 癌症多维度知识门户_cckp_cancer_complexity_knowledge_portal -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 癌症多维度知识门户_cckp_cancer_complexity_knowledge_portal -o output.jsonl
```

## 输出格式

- JSONL格式: `output/癌症多维度知识门户_cckp_cancer_complexity_knowledge_portal_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/癌症多维度知识门户_cckp_cancer_complexity_knowledge_portal_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/癌症多维度知识门户_cckp_cancer_complexity_knowledge_portal/
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

- **生成时间**: 2026-01-18 06:31:44
- **生成工具**: Spider Generator v1.0
