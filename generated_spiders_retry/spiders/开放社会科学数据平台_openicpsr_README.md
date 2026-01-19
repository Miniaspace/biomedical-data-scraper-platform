# 开放社会科学数据平台 openICPSR Spider

## 基本信息

- **平台名称**: 开放社会科学数据平台 openICPSR
- **平台URL**: https://openicpsr.org
- **Spider名称**: 开放社会科学数据平台_openicpsr
- **采集方法**: scrapy
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无分页，因网站访问受限，无法确认分页结构，需先解决访问限制问题后再设计分页策略。

## 数据字段

暂无字段信息

## 文件下载

由于当前无法访问网站内容，无法确定文件下载链接和结构。待访问权限恢复后，采用Scrapy的文件下载中间件，结合文件链接的CSS或XPath选择器进行下载。

## 反爬应对

- 当前页面显示访问被拒绝，可能存在IP封禁或访问限制，建议更换IP或使用代理池。
- 模拟正常浏览器请求头，避免被服务器识别为爬虫。
- 考虑与网站管理员沟通获取合法访问权限或API接口。

## 注意事项

- 当前网站访问被拒绝，需先解决访问权限问题。
- 无登录需求，无JavaScript渲染，理论上Scrapy即可满足采集需求。
- 无检测到API，需通过页面解析获取数据。
- 无分页，或分页结构未知，需确认后设计采集流程。

## 使用方法

```bash
# 运行Spider
scrapy crawl 开放社会科学数据平台_openicpsr

# 限制采集数量（测试用）
scrapy crawl 开放社会科学数据平台_openicpsr -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 开放社会科学数据平台_openicpsr -o output.jsonl
```

## 输出格式

- JSONL格式: `output/开放社会科学数据平台_openicpsr_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/开放社会科学数据平台_openicpsr_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/开放社会科学数据平台_openicpsr/
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

- **生成时间**: 2026-01-18 07:40:51
- **生成工具**: Spider Generator v1.0
