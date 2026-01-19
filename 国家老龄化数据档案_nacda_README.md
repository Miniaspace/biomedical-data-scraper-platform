# 国家老龄化数据档案 NACDA Spider

## 基本信息

- **平台名称**: 国家老龄化数据档案 NACDA
- **平台URL**: https://www.icpsr.umich.edu/web/pages/NACDA/
- **Spider名称**: 国家老龄化数据档案_nacda
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

由于采用无限滚动(infinite_scroll)分页，使用Playwright模拟用户滚动页面，等待新内容加载，直到无新内容出现或达到预设最大条数。结合网络请求监听，确保所有数据加载完成后再进行数据提取。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.title, xpath=//h1[contains(@class, 'title')]` |
| author | `css=span.author, xpath=//span[contains(@class, 'author')]` |
| publication_date | `css=span.pub-date, xpath=//span[contains(@class, 'pub-date')]` |
| abstract | `css=div.abstract, xpath=//div[contains(@class, 'abstract')]` |
| pdf_link | `css=a.pdf-download, xpath=//a[contains(@href, '.pdf')]` |
| supplementary_materials | `css=a.supplementary, xpath=//a[contains(text(), 'Supplementary')]` |


## 文件下载

对所有PDF及补充材料链接进行统一下载，使用Playwright获取下载链接后通过Python requests或Playwright直接下载。登录态需保持，下载时带上相应cookies和header。对大文件采用断点续传策略，避免下载中断。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免被Cloudflare检测为机器人。
- 合理控制请求频率，模拟人类浏览节奏，防止触发反爬限制。
- 登录后保持会话状态，自动处理登录cookie和token。
- 启用代理池，分散请求来源，降低被封风险。

## 注意事项

- 登录流程复杂，需实现自动化登录并处理可能的多因素认证。
- 页面内容动态加载，需等待JS渲染完成后再抓取数据。
- Cloudflare防护较强，需使用无头浏览器并模拟真实用户行为。
- 数据结构可能不固定，需设计灵活的字段提取规则。

## 使用方法

```bash
# 运行Spider
scrapy crawl 国家老龄化数据档案_nacda

# 限制采集数量（测试用）
scrapy crawl 国家老龄化数据档案_nacda -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国家老龄化数据档案_nacda -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国家老龄化数据档案_nacda_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国家老龄化数据档案_nacda_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国家老龄化数据档案_nacda/
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

- **生成时间**: 2026-01-18 07:45:30
- **生成工具**: Spider Generator v1.0
