# 罕见病治疗加速器数据平台 RDCA-DAP (Rare Disease Cures Accelerator - Data and Analytics Platform) Spider

## 基本信息

- **平台名称**: 罕见病治疗加速器数据平台 RDCA-DAP (Rare Disease Cures Accelerator - Data and Analytics Platform)
- **平台URL**: https://portal.rdca.c-path.org
- **Spider名称**: 罕见病治疗加速器数据平台_rdca_dap_rare_disease_cures_accelerator_data_and_analytics_platform
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

无分页，全部数据在单页面加载，直接抓取全部列表项

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li > div.title, ul li > h3.title` |
| author | `ul li > div.author, ul li > span.author` |
| date | `ul li > div.date, ul li > span.date` |
| pdf_link | `ul li a[href$='.pdf']` |
| supplementary_material_link | `ul li a.supplementary` |


## 文件下载

通过Playwright模拟点击或直接请求PDF及补充材料链接，保持登录态，使用流式下载保存文件

## 反爬应对

- 使用Playwright模拟真实浏览器环境，执行JavaScript，绕过Cloudflare防护
- 保持登录状态，管理cookie和会话，避免重复登录
- 设置合理的请求间隔，避免触发潜在的速率限制
- 使用代理IP池分散请求，防止IP封禁

## 注意事项

- 登录认证是必须步骤，需实现自动登录并处理登录失败情况
- 页面内容依赖JavaScript渲染，必须使用Playwright或类似工具
- 无API接口，需从页面DOM解析所有数据
- 文件下载需保持登录态，避免下载链接失效
- 页面结构可能动态变化，需定期维护选择器

## 使用方法

```bash
# 运行Spider
scrapy crawl 罕见病治疗加速器数据平台_rdca_dap_rare_disease_cures_accelerator_data_and_analytics_platform

# 限制采集数量（测试用）
scrapy crawl 罕见病治疗加速器数据平台_rdca_dap_rare_disease_cures_accelerator_data_and_analytics_platform -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 罕见病治疗加速器数据平台_rdca_dap_rare_disease_cures_accelerator_data_and_analytics_platform -o output.jsonl
```

## 输出格式

- JSONL格式: `output/罕见病治疗加速器数据平台_rdca_dap_rare_disease_cures_accelerator_data_and_analytics_platform_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/罕见病治疗加速器数据平台_rdca_dap_rare_disease_cures_accelerator_data_and_analytics_platform_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/罕见病治疗加速器数据平台_rdca_dap_rare_disease_cures_accelerator_data_and_analytics_platform/
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

- **生成时间**: 2026-01-18 06:18:28
- **生成工具**: Spider Generator v1.0
