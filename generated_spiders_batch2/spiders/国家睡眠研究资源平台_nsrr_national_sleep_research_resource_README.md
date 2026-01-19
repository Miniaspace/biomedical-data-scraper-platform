# 国家睡眠研究资源平台 NSRR (National Sleep Research Resource) Spider

## 基本信息

- **平台名称**: 国家睡眠研究资源平台 NSRR (National Sleep Research Resource)
- **平台URL**: https://sleepdata.org
- **Spider名称**: 国家睡眠研究资源平台_nsrr_national_sleep_research_resource
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

无分页，需遍历首页所有列表项，若数据量大需结合登录后动态加载或筛选功能进行分批采集

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.page-title, xpath=//h1[contains(@class,'page-title')]` |
| authors | `css=.author-list, xpath=//div[contains(@class,'author-list')]` |
| abstract | `css=.abstract, xpath=//section[contains(@class,'abstract')]` |
| publication_date | `css=.pub-date, xpath=//time[contains(@class,'pub-date')]` |
| pdf_link | `css=a[href$='.pdf'], xpath=//a[contains(@href,'.pdf')]` |
| supplementary_materials | `css=a.supplementary, xpath=//a[contains(@class,'supplementary')]` |


## 文件下载

通过Playwright模拟登录后，使用页面中直接可访问的PDF和补充材料链接进行文件下载，确保带上登录cookie和header，避免重定向到登录页

## 反爬应对

- 使用Playwright模拟真实浏览器行为，自动处理登录和验证码弹窗
- 针对验证码，尝试人工打码或集成第三方验证码识别服务
- 控制请求频率，模拟正常用户浏览节奏，避免触发异常检测

## 注意事项

- 登录是必须步骤，需稳定实现登录流程并维护会话
- 验证码可能在登录或关键操作时出现，需预留人工干预接口
- 网站无API，数据结构较简单但需处理登录和验证码，采集难度较高

## 使用方法

```bash
# 运行Spider
scrapy crawl 国家睡眠研究资源平台_nsrr_national_sleep_research_resource

# 限制采集数量（测试用）
scrapy crawl 国家睡眠研究资源平台_nsrr_national_sleep_research_resource -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国家睡眠研究资源平台_nsrr_national_sleep_research_resource -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国家睡眠研究资源平台_nsrr_national_sleep_research_resource_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国家睡眠研究资源平台_nsrr_national_sleep_research_resource_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国家睡眠研究资源平台_nsrr_national_sleep_research_resource/
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

- **生成时间**: 2026-01-18 06:20:53
- **生成工具**: Spider Generator v1.0
