# 生物医学信息学研究中心与知识系统 BRICS (Biomedical Research Informatics Center and Knowledge Systems) Spider

## 基本信息

- **平台名称**: 生物医学信息学研究中心与知识系统 BRICS (Biomedical Research Informatics Center and Knowledge Systems)
- **平台URL**: https://brics.nei.nih.gov
- **Spider名称**: 生物医学信息学研究中心与知识系统_brics_biomedical_research_informatics_center_and_knowledge_systems
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无分页，页面一次性加载所有列表项，无需分页处理

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a::text` |
| detail_url | `li > a::attr(href)` |


## 文件下载

通过Playwright模拟登录后，访问详情页，解析PDF文件链接，使用Playwright下载或通过requests附带登录cookie下载PDF文件

## 反爬应对

- 使用Playwright模拟真实浏览器行为，绕过Cloudflare防护
- 保持登录状态，管理会话cookie，避免频繁重新登录
- 控制请求频率，避免触发潜在的访问限制

## 注意事项

- 登录流程需处理表单提交，可能涉及CSRF token，需动态获取
- Cloudflare防护可能导致初次访问延迟，需设置合理等待时间
- 详情页链接跳转至外部域名，需处理跨域请求和文件下载

## 使用方法

```bash
# 运行Spider
scrapy crawl 生物医学信息学研究中心与知识系统_brics_biomedical_research_informatics_center_and_knowledge_systems

# 限制采集数量（测试用）
scrapy crawl 生物医学信息学研究中心与知识系统_brics_biomedical_research_informatics_center_and_knowledge_systems -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 生物医学信息学研究中心与知识系统_brics_biomedical_research_informatics_center_and_knowledge_systems -o output.jsonl
```

## 输出格式

- JSONL格式: `output/生物医学信息学研究中心与知识系统_brics_biomedical_research_informatics_center_and_knowledge_systems_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/生物医学信息学研究中心与知识系统_brics_biomedical_research_informatics_center_and_knowledge_systems_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/生物医学信息学研究中心与知识系统_brics_biomedical_research_informatics_center_and_knowledge_systems/
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

- **生成时间**: 2026-01-18 06:20:27
- **生成工具**: Spider Generator v1.0
