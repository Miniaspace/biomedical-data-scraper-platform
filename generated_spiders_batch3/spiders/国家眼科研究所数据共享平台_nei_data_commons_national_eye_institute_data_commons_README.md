# 国家眼科研究所数据共享平台 NEI Data Commons (National Eye Institute Data Commons) Spider

## 基本信息

- **平台名称**: 国家眼科研究所数据共享平台 NEI Data Commons (National Eye Institute Data Commons)
- **平台URL**: https://neidatacommons.nei.nih.gov
- **Spider名称**: 国家眼科研究所数据共享平台_nei_data_commons_national_eye_institute_data_commons
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 16

## 采集策略

由于采用无限滚动加载更多列表项，使用Scrapy结合中间件（如scrapy-selenium或scrapy-playwright）模拟滚动加载，循环触发页面滚动事件，直到加载完全部列表项后停止采集。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css: h1.page-title, xpath: //h1[contains(@class, 'page-title')]` |
| authors | `css: div.authors, xpath: //div[contains(@class, 'authors')]` |
| abstract | `css: div.abstract, xpath: //div[contains(@class, 'abstract')]` |
| publication_date | `css: span.pub-date, xpath: //span[contains(@class, 'pub-date')]` |
| pdf_link | `css: a[href$='.pdf'], xpath: //a[contains(@href, '.pdf')]` |
| supplementary_materials | `css: a.supplementary, xpath: //a[contains(@class, 'supplementary')]` |


## 文件下载

对所有详情页中检测到的PDF链接及补充材料链接，使用Scrapy的FilesPipeline或自定义下载中间件进行文件下载，确保文件完整性和重试机制。

## 反爬应对

- 由于无验证码、无明显限速，保持合理请求间隔（如1-2秒）避免触发服务器限制
- 设置合理User-Agent，模拟常见浏览器请求头
- 使用IP代理池以防止IP封禁（可选）

## 注意事项

- 页面JavaScript加载较少，Scrapy直接请求即可，无需Playwright
- 无限滚动需模拟前端行为，推荐使用scrapy-playwright或scrapy-selenium辅助
- 注意详情页链接为相对路径，需拼接完整URL

## 使用方法

```bash
# 运行Spider
scrapy crawl 国家眼科研究所数据共享平台_nei_data_commons_national_eye_institute_data_commons

# 限制采集数量（测试用）
scrapy crawl 国家眼科研究所数据共享平台_nei_data_commons_national_eye_institute_data_commons -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国家眼科研究所数据共享平台_nei_data_commons_national_eye_institute_data_commons -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国家眼科研究所数据共享平台_nei_data_commons_national_eye_institute_data_commons_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国家眼科研究所数据共享平台_nei_data_commons_national_eye_institute_data_commons_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国家眼科研究所数据共享平台_nei_data_commons_national_eye_institute_data_commons/
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

- **生成时间**: 2026-01-18 06:39:23
- **生成工具**: Spider Generator v1.0
