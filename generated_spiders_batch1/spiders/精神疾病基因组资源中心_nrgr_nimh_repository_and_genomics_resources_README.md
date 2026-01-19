# 精神疾病基因组资源中心 NRGR (NIMH Repository and Genomics Resources) Spider

## 基本信息

- **平台名称**: 精神疾病基因组资源中心 NRGR (NIMH Repository and Genomics Resources)
- **平台URL**: https://nimhgenetics.org
- **Spider名称**: 精神疾病基因组资源中心_nrgr_nimh_repository_and_genomics_resources
- **采集方法**: scrapy
- **难度评级**: ⭐
- **预估开发时间**: 4

## 采集策略

网站无分页，所有数据均在单一页面或少量页面中直接展示，无需分页处理。

## 数据字段

暂无字段信息

## 文件下载

直接解析页面中所有可见的PDF文件链接或补充材料链接，使用Scrapy的文件下载管道或自定义请求进行下载，确保文件URL完整有效。

## 反爬应对

- 无验证码，无Cloudflare，无JavaScript渲染需求，故无特殊反爬处理必要。
- 合理设置请求间隔，避免过快请求导致服务器限制。

## 注意事项

- 网站当前无API，且无动态内容，直接静态HTML解析即可。
- 目标数据结构未明确，需根据实际页面内容灵活调整选择器。

## 使用方法

```bash
# 运行Spider
scrapy crawl 精神疾病基因组资源中心_nrgr_nimh_repository_and_genomics_resources

# 限制采集数量（测试用）
scrapy crawl 精神疾病基因组资源中心_nrgr_nimh_repository_and_genomics_resources -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 精神疾病基因组资源中心_nrgr_nimh_repository_and_genomics_resources -o output.jsonl
```

## 输出格式

- JSONL格式: `output/精神疾病基因组资源中心_nrgr_nimh_repository_and_genomics_resources_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/精神疾病基因组资源中心_nrgr_nimh_repository_and_genomics_resources_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/精神疾病基因组资源中心_nrgr_nimh_repository_and_genomics_resources/
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

- **生成时间**: 2026-01-18 06:17:04
- **生成工具**: Spider Generator v1.0
