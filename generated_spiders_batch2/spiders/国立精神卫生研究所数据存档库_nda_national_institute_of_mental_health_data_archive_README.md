# 国立精神卫生研究所数据存档库 NDA (National Institute of Mental Health Data Archive) Spider

## 基本信息

- **平台名称**: 国立精神卫生研究所数据存档库 NDA (National Institute of Mental Health Data Archive)
- **平台URL**: https://nda.nih.gov/nda/access-data-info.html
- **Spider名称**: 国立精神卫生研究所数据存档库_nda_national_institute_of_mental_health_data_archive
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动（infinite_scroll）分页，使用Playwright模拟浏览器滚动页面，等待新内容加载后继续滚动，直到页面不再加载新数据或达到预设最大条数。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li > strong, ul li > a, ul li > span` |
| description | `ul li > p, ul li > span.description` |
| date | `ul li > time, ul li > span.date` |
| pdf_link | `ul li a[href$='.pdf']` |


## 文件下载

采集到PDF或补充材料链接后，使用Playwright获取完整下载链接，结合登录状态发送带cookie的请求下载文件，支持断点续传和重试机制。

## 反爬应对

- 模拟真实用户行为，控制滚动速度和间隔，避免触发异常访问
- 保持登录状态，定期刷新cookie或重新登录
- 合理设置请求间隔，防止服务器压力过大

## 注意事项

- 登录流程需自动化处理，可能涉及多因素认证或验证码，需提前确认登录接口和流程
- 页面无API接口，所有数据需通过渲染后的DOM提取
- 部分文件下载链接可能需要额外请求头或Referer，需抓包确认

## 使用方法

```bash
# 运行Spider
scrapy crawl 国立精神卫生研究所数据存档库_nda_national_institute_of_mental_health_data_archive

# 限制采集数量（测试用）
scrapy crawl 国立精神卫生研究所数据存档库_nda_national_institute_of_mental_health_data_archive -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国立精神卫生研究所数据存档库_nda_national_institute_of_mental_health_data_archive -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国立精神卫生研究所数据存档库_nda_national_institute_of_mental_health_data_archive_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国立精神卫生研究所数据存档库_nda_national_institute_of_mental_health_data_archive_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国立精神卫生研究所数据存档库_nda_national_institute_of_mental_health_data_archive/
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

- **生成时间**: 2026-01-18 06:26:25
- **生成工具**: Spider Generator v1.0
