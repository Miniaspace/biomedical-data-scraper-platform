# 创伤性脑损伤开放数据平台 ODC-TBI (Open Data Commons - Traumatic Brain Injury) Spider

## 基本信息

- **平台名称**: 创伤性脑损伤开放数据平台 ODC-TBI (Open Data Commons - Traumatic Brain Injury)
- **平台URL**: https://odc-tbi.org
- **Spider名称**: 创伤性脑损伤开放数据平台_odc_tbi_open_data_commons_traumatic_brain_injury
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

由于采用无限滚动(infinite scroll)，使用Playwright模拟用户滚动页面，等待新数据加载，直到无新数据出现或达到预设最大条目数。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `CSS选择器示例: li .title 或 li h3` |
| author | `CSS选择器示例: li .author` |
| date | `CSS选择器示例: li .date` |
| description | `CSS选择器示例: li .description` |
| pdf_link | `CSS选择器示例: li a[href$='.pdf']` |


## 文件下载

在详情页或列表页中定位PDF或补充材料链接，使用Playwright获取完整下载URL，结合Python requests或Playwright自身下载接口进行文件下载，需处理登录态和cookie传递。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，执行JavaScript，避免因无JS执行而无法加载内容
- 保持登录状态，模拟正常用户操作，避免触发登录验证
- 控制请求频率，避免短时间内大量请求导致封禁
- 使用随机等待时间和滚动间隔，模拟真实用户浏览行为

## 注意事项

- 登录流程需要先分析，可能涉及验证码或多因素认证，需人工辅助或模拟登录
- 无限滚动可能加载大量数据，需设置合理的最大采集条数或时间限制
- 详情页链接为'#'，说明详情信息可能在列表页动态展开或通过AJAX加载，需分析网络请求抓取数据
- 无公开API，需通过页面渲染抓取，数据结构可能动态变化，需定期维护选择器

## 使用方法

```bash
# 运行Spider
scrapy crawl 创伤性脑损伤开放数据平台_odc_tbi_open_data_commons_traumatic_brain_injury

# 限制采集数量（测试用）
scrapy crawl 创伤性脑损伤开放数据平台_odc_tbi_open_data_commons_traumatic_brain_injury -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 创伤性脑损伤开放数据平台_odc_tbi_open_data_commons_traumatic_brain_injury -o output.jsonl
```

## 输出格式

- JSONL格式: `output/创伤性脑损伤开放数据平台_odc_tbi_open_data_commons_traumatic_brain_injury_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/创伤性脑损伤开放数据平台_odc_tbi_open_data_commons_traumatic_brain_injury_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/创伤性脑损伤开放数据平台_odc_tbi_open_data_commons_traumatic_brain_injury/
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

- **生成时间**: 2026-01-18 06:44:02
- **生成工具**: Spider Generator v1.0
