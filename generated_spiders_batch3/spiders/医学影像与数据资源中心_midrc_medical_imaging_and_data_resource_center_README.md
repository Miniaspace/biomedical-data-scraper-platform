# 医学影像与数据资源中心 MIDRC (Medical Imaging and Data Resource Center) Spider

## 基本信息

- **平台名称**: 医学影像与数据资源中心 MIDRC (Medical Imaging and Data Resource Center)
- **平台URL**: https://midrc.org
- **Spider名称**: 医学影像与数据资源中心_midrc_medical_imaging_and_data_resource_center
- **采集方法**: scrapy
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动(infinite_scroll)分页，使用Scrapy结合中间件或自定义中间件模拟滚动加载。通过分析网络请求，捕获加载更多数据的XHR请求参数，循环发送请求直到无新数据返回。若无XHR请求，则使用Playwright模拟滚动加载后抓取完整列表。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > h2, li > .title, li > a` |
| author | `li .author, li .meta .author` |
| date | `li .date, li .meta .date` |
| description | `li .description, li p` |
| pdf_link | `li a[href$='.pdf']` |


## 文件下载

采集到PDF或补充材料链接后，使用Scrapy的FilesPipeline或自定义下载逻辑进行文件下载，确保文件命名规范并支持断点续传。对于动态生成的下载链接，需先访问详情页获取真实下载地址。

## 反爬应对

- 针对验证码，尝试绕过或人工辅助识别，若验证码频繁出现，降低请求频率并增加随机延时。
- 设置合理User-Agent和请求头，模拟真实浏览器访问。
- 控制请求速率，避免触发验证码。
- 使用代理IP池分散请求来源，降低被封风险。

## 注意事项

- 网站无登录但存在验证码，需重点关注验证码触发条件，尽量避免频繁请求。
- 无限滚动分页可能导致数据量大，需合理设计采集批次和数据存储。
- 无公开API，数据需从HTML页面解析，需关注页面结构变化。

## 使用方法

```bash
# 运行Spider
scrapy crawl 医学影像与数据资源中心_midrc_medical_imaging_and_data_resource_center

# 限制采集数量（测试用）
scrapy crawl 医学影像与数据资源中心_midrc_medical_imaging_and_data_resource_center -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 医学影像与数据资源中心_midrc_medical_imaging_and_data_resource_center -o output.jsonl
```

## 输出格式

- JSONL格式: `output/医学影像与数据资源中心_midrc_medical_imaging_and_data_resource_center_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/医学影像与数据资源中心_midrc_medical_imaging_and_data_resource_center_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/医学影像与数据资源中心_midrc_medical_imaging_and_data_resource_center/
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

- **生成时间**: 2026-01-18 06:35:47
- **生成工具**: Spider Generator v1.0
