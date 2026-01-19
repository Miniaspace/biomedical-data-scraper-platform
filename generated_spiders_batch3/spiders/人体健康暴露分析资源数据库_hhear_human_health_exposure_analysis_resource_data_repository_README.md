# 人体健康暴露分析资源数据库 HHEAR (Human Health Exposure Analysis Resource Data Repository) Spider

## 基本信息

- **平台名称**: 人体健康暴露分析资源数据库 HHEAR (Human Health Exposure Analysis Resource Data Repository)
- **平台URL**: https://hheardatacenter.mssm.edu
- **Spider名称**: 人体健康暴露分析资源数据库_hhear_human_health_exposure_analysis_resource_data_repository
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

无分页，页面一次性加载所有数据，直接抓取当前页面全部表格行

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| study_name | `table tbody tr td:nth-child(1)` |
| study_description | `table tbody tr td:nth-child(2)` |
| study_date | `table tbody tr td:nth-child(3)` |
| download_links | `table tbody tr td a[href$='.pdf'], table tbody tr td a[href$='.zip'], table tbody tr td a[href$='.csv']` |


## 文件下载

通过Playwright模拟点击下载链接，处理文件保存路径和命名，支持断点续传和重试机制

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免被Cloudflare拦截
- 登录时处理验证码，采用手动输入或第三方验证码识别服务
- 设置合理的请求间隔，避免触发反爬机制
- 使用代理IP池分散请求来源

## 注意事项

- 登录流程复杂，需实现动态验证码处理
- 网站无API，所有数据均需从页面解析
- 文件下载链接可能分散在表格不同列，需全面提取
- Cloudflare防护可能导致请求失败，需重试和异常捕获

## 使用方法

```bash
# 运行Spider
scrapy crawl 人体健康暴露分析资源数据库_hhear_human_health_exposure_analysis_resource_data_repository

# 限制采集数量（测试用）
scrapy crawl 人体健康暴露分析资源数据库_hhear_human_health_exposure_analysis_resource_data_repository -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 人体健康暴露分析资源数据库_hhear_human_health_exposure_analysis_resource_data_repository -o output.jsonl
```

## 输出格式

- JSONL格式: `output/人体健康暴露分析资源数据库_hhear_human_health_exposure_analysis_resource_data_repository_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/人体健康暴露分析资源数据库_hhear_human_health_exposure_analysis_resource_data_repository_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/人体健康暴露分析资源数据库_hhear_human_health_exposure_analysis_resource_data_repository/
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

- **生成时间**: 2026-01-18 06:36:26
- **生成工具**: Spider Generator v1.0
