# NIAID临床数据访问平台 ACD@NIAID (AccessClinicalData@NIAID) Spider

## 基本信息

- **平台名称**: NIAID临床数据访问平台 ACD@NIAID (AccessClinicalData@NIAID)
- **平台URL**: https://accessclinicaldata.niaid.nih.gov
- **Spider名称**: niaid临床数据访问平台_acdniaid_accessclinicaldataniaid
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

使用Playwright模拟用户滚动页面，触发无限滚动加载更多列表项，直到没有新数据加载为止。通过监听网络请求和DOM变化判断加载完成。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.study-title, xpath=//h1[contains(@class,'study-title')]` |
| study_id | `css=span.study-id, xpath=//span[contains(@class,'study-id')]` |
| status | `css=div.status, xpath=//div[contains(@class,'status')]` |
| start_date | `css=div.start-date, xpath=//div[contains(@class,'start-date')]` |
| completion_date | `css=div.completion-date, xpath=//div[contains(@class,'completion-date')]` |
| pdf_links | `css=a[href$='.pdf'], xpath=//a[contains(@href,'.pdf')]` |


## 文件下载

在详情页中定位所有PDF链接，使用Playwright拦截下载请求或直接通过requests库结合cookie/session下载PDF文件，确保登录状态有效。

## 反爬应对

- 保持登录状态，使用Playwright自动处理登录流程，避免频繁登录导致封禁。
- 模拟真实用户行为（如鼠标移动、随机等待）降低被检测风险。
- 合理控制请求频率，避免触发服务器异常流量检测。

## 注意事项

- 登录认证为必需，需处理登录表单及可能的多因素认证。
- 无公开API，所有数据均需通过页面渲染抓取。
- 无限滚动加载数据量较大，需合理设计滚动和数据存储策略，避免内存溢出。
- PDF文件下载需保证会话有效，可能需要动态cookie或token。

## 使用方法

```bash
# 运行Spider
scrapy crawl niaid临床数据访问平台_acdniaid_accessclinicaldataniaid

# 限制采集数量（测试用）
scrapy crawl niaid临床数据访问平台_acdniaid_accessclinicaldataniaid -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl niaid临床数据访问平台_acdniaid_accessclinicaldataniaid -o output.jsonl
```

## 输出格式

- JSONL格式: `output/niaid临床数据访问平台_acdniaid_accessclinicaldataniaid_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/niaid临床数据访问平台_acdniaid_accessclinicaldataniaid_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/niaid临床数据访问平台_acdniaid_accessclinicaldataniaid/
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

- **生成时间**: 2026-01-18 06:19:07
- **生成工具**: Spider Generator v1.0
