# 失语症语言数据库 AB (AphasiaBank) Spider

## 基本信息

- **平台名称**: 失语症语言数据库 AB (AphasiaBank)
- **平台URL**: https://aphasia.talkbank.org
- **Spider名称**: 失语症语言数据库_ab_aphasiabank
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无分页，所有数据集中展示或通过登录后导航访问各研究条目，需模拟登录后遍历所有研究详情页面链接

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css: h1.title, h2.article-title, 或 xpath: //h1[contains(@class,'title')]` |
| author | `css: div.authors, span.author-name, 或 xpath: //div[contains(@class,'author')]//span` |
| publication_date | `css: span.pub-date, time.pub-date, 或 xpath: //time[contains(@class,'pub-date')]` |
| abstract | `css: div.abstract, section.abstract, 或 xpath: //div[contains(@class,'abstract')]` |
| pdf_link | `css: a[href$='.pdf']` |
| docx_link | `css: a[href$='.docx']` |


## 文件下载

登录后使用Playwright保持会话状态，直接访问PDF和DOCX链接进行下载，确保请求头带上Cookie和Referer，避免403错误

## 反爬应对

- 使用Playwright模拟真实浏览器环境，完成登录流程，保持会话
- 合理控制请求频率，避免触发登录限制
- 处理登录失败和会话过期，自动重试登录

## 注意事项

- 登录流程依赖外部域名的JS模块，需确保Playwright支持模块加载
- 无API接口，数据需从HTML中解析，需登录后才能访问完整数据
- 网站编码为ISO-8859-1，需正确处理字符编码

## 使用方法

```bash
# 运行Spider
scrapy crawl 失语症语言数据库_ab_aphasiabank

# 限制采集数量（测试用）
scrapy crawl 失语症语言数据库_ab_aphasiabank -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 失语症语言数据库_ab_aphasiabank -o output.jsonl
```

## 输出格式

- JSONL格式: `output/失语症语言数据库_ab_aphasiabank_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/失语症语言数据库_ab_aphasiabank_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/失语症语言数据库_ab_aphasiabank/
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

- **生成时间**: 2026-01-18 06:32:30
- **生成工具**: Spider Generator v1.0
