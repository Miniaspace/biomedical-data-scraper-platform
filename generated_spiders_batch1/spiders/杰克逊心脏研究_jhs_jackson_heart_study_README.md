# 杰克逊心脏研究 JHS (Jackson Heart Study) Spider

## 基本信息

- **平台名称**: 杰克逊心脏研究 JHS (Jackson Heart Study)
- **平台URL**: https://www.jacksonheartstudy.org/
- **Spider名称**: 杰克逊心脏研究_jhs_jackson_heart_study
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 6

## 采集策略

网站无分页，所有列表项均在单页内加载，直接采集完整列表，无需分页处理。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li > a::text` |
| detail_link | `ul li > a::attr(href)` |


## 文件下载

在详情页中解析所有PDF及补充材料链接，使用Scrapy的文件下载管道或自定义下载逻辑，确保文件完整保存。文件链接一般为以.pdf结尾的URL，需结合详情页链接构造完整URL。

## 反爬应对

- 网站无验证码和复杂反爬机制，保持合理请求频率，避免过快访问。
- 设置User-Agent模拟浏览器请求，防止部分简单的UA屏蔽。

## 注意事项

- 网站结构较为简单，无API接口，需通过HTML解析获取数据。
- 部分链接可能为相对路径，需拼接域名确保正确访问。
- 确认所有目标文件链接是否直接可访问，若有重定向需处理。

## 使用方法

```bash
# 运行Spider
scrapy crawl 杰克逊心脏研究_jhs_jackson_heart_study

# 限制采集数量（测试用）
scrapy crawl 杰克逊心脏研究_jhs_jackson_heart_study -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 杰克逊心脏研究_jhs_jackson_heart_study -o output.jsonl
```

## 输出格式

- JSONL格式: `output/杰克逊心脏研究_jhs_jackson_heart_study_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/杰克逊心脏研究_jhs_jackson_heart_study_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/杰克逊心脏研究_jhs_jackson_heart_study/
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

- **生成时间**: 2026-01-18 06:12:06
- **生成工具**: Spider Generator v1.0
