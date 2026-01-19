# 阿尔茨海默病知识门户 AD Knowledge Portal (Alzheimer's Disease Knowledge Portal) Spider

## 基本信息

- **平台名称**: 阿尔茨海默病知识门户 AD Knowledge Portal (Alzheimer's Disease Knowledge Portal)
- **平台URL**: https://adknowledgeportal.synapse.org
- **Spider名称**: 阿尔茨海默病知识门户_ad_knowledge_portal_alzheimers_disease_knowledge_portal
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于页面采用无限滚动(infinite scroll)加载数据，使用Playwright模拟用户滚动页面，等待新数据加载完成后继续滚动，直到页面不再加载新数据为止，确保采集所有列表项。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `td:nth-child(1) a` |
| author | `td:nth-child(2)` |
| date | `td:nth-child(3)` |
| status | `td:nth-child(4)` |


## 文件下载

在采集到的列表或详情页中定位PDF文件及补充材料的下载链接，使用Playwright模拟点击或直接请求下载链接进行文件下载。登录态需保持，且下载时需处理可能的重定向和断点续传。

## 反爬应对

- 保持登录态，使用Playwright模拟真实浏览器环境，避免被识别为爬虫。
- 控制滚动和请求频率，避免触发服务器异常。
- 使用随机延时和适度并发，模拟正常用户行为。

## 注意事项

- 登录流程需要实现自动化，可能涉及多步验证，需提前准备账号和密码。
- 页面无公开API，所有数据需通过渲染后的页面DOM提取。
- 文件下载链接可能动态生成，需在页面完全加载后提取。

## 使用方法

```bash
# 运行Spider
scrapy crawl 阿尔茨海默病知识门户_ad_knowledge_portal_alzheimers_disease_knowledge_portal

# 限制采集数量（测试用）
scrapy crawl 阿尔茨海默病知识门户_ad_knowledge_portal_alzheimers_disease_knowledge_portal -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 阿尔茨海默病知识门户_ad_knowledge_portal_alzheimers_disease_knowledge_portal -o output.jsonl
```

## 输出格式

- JSONL格式: `output/阿尔茨海默病知识门户_ad_knowledge_portal_alzheimers_disease_knowledge_portal_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/阿尔茨海默病知识门户_ad_knowledge_portal_alzheimers_disease_knowledge_portal_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/阿尔茨海默病知识门户_ad_knowledge_portal_alzheimers_disease_knowledge_portal/
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

- **生成时间**: 2026-01-18 06:24:06
- **生成工具**: Spider Generator v1.0
