# 慢性阻塞性肺病亚群及中间结局指标研究 SPIROMICS (The Subpopulations and Intermediate Outcome Measures in COPD Study) Spider

## 基本信息

- **平台名称**: 慢性阻塞性肺病亚群及中间结局指标研究 SPIROMICS (The Subpopulations and Intermediate Outcome Measures in COPD Study)
- **平台URL**: https://www.spiromics.org/spiromics/
- **Spider名称**: 慢性阻塞性肺病亚群及中间结局指标研究_spiromics_the_subpopulations_and_intermediate_outcome_measures_in_copd_study
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

使用Playwright模拟页面滚动触发无限加载，监听新内容加载完成后继续滚动，直到无新数据加载为止

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=h1.page-title, xpath=//h1[contains(@class,'page-title')]` |
| authors | `css=.field--name-field-authors, xpath=//div[contains(@class,'field--name-field-authors')]` |
| publication_date | `css=.field--name-field-publication-date, xpath=//div[contains(@class,'field--name-field-publication-date')]` |
| abstract | `css=.field--name-field-abstract, xpath=//div[contains(@class,'field--name-field-abstract')]` |
| pdf_link | `css=a[href$='.pdf'], xpath=//a[contains(@href,'.pdf')]` |


## 文件下载

通过Playwright获取PDF文件链接后，使用Scrapy或requests结合登录会话cookie进行文件下载，确保权限验证通过

## 反爬应对

- 模拟真实浏览器行为，使用Playwright自动化登录并保持登录状态
- 控制滚动速度和请求频率，避免触发异常流量检测
- 使用随机User-Agent和合理延时，降低被识别风险

## 注意事项

- 登录流程需要处理可能的多因素验证或登录验证码（目前未检测到），需预留接口
- 无限滚动加载可能存在加载失败或超时情况，需增加重试和异常处理机制
- PDF文件下载需保证cookie或token有效，避免403拒绝访问

## 使用方法

```bash
# 运行Spider
scrapy crawl 慢性阻塞性肺病亚群及中间结局指标研究_spiromics_the_subpopulations_and_intermediate_outcome_measures_in_copd_study

# 限制采集数量（测试用）
scrapy crawl 慢性阻塞性肺病亚群及中间结局指标研究_spiromics_the_subpopulations_and_intermediate_outcome_measures_in_copd_study -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 慢性阻塞性肺病亚群及中间结局指标研究_spiromics_the_subpopulations_and_intermediate_outcome_measures_in_copd_study -o output.jsonl
```

## 输出格式

- JSONL格式: `output/慢性阻塞性肺病亚群及中间结局指标研究_spiromics_the_subpopulations_and_intermediate_outcome_measures_in_copd_study_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/慢性阻塞性肺病亚群及中间结局指标研究_spiromics_the_subpopulations_and_intermediate_outcome_measures_in_copd_study_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/慢性阻塞性肺病亚群及中间结局指标研究_spiromics_the_subpopulations_and_intermediate_outcome_measures_in_copd_study/
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

- **生成时间**: 2026-01-18 06:12:39
- **生成工具**: Spider Generator v1.0
