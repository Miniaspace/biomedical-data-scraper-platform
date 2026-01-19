# 临床试验数据共享平台 TS TS (TrialShare) Spider

## 基本信息

- **平台名称**: 临床试验数据共享平台 TS TS (TrialShare)
- **平台URL**: https://itntrialshare.org/login/home/login.view?returnUrl=%2Fhome%2Fproject-start.view%3F
- **Spider名称**: 临床试验数据共享平台_ts_ts_trialshare
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无分页，所有数据均在单页面表格中展示，直接抓取全部表格行数据。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| study_id | `table tbody tr td:nth-child(1)` |
| study_name | `table tbody tr td:nth-child(2)` |
| status | `table tbody tr td:nth-child(3)` |
| start_date | `table tbody tr td:nth-child(4)` |
| end_date | `table tbody tr td:nth-child(5)` |
| pdf_link | `table tbody tr td a[href$='.pdf']` |


## 文件下载

通过Playwright模拟点击或直接请求PDF链接，确保登录状态下访问，保存PDF文件到本地。

## 反爬应对

- 使用Playwright模拟真实浏览器环境，执行JavaScript，确保页面正常加载。
- 保持登录状态，管理好Cookie和会话信息，避免重复登录。
- 控制请求频率，避免触发潜在的速率限制。

## 注意事项

- 登录过程需要处理表单提交，可能需要验证码外的额外验证步骤，需手动确认登录流程。
- 页面数据无分页，数据量较大时需注意内存和性能优化。
- PDF文件下载需确保链接有效且在登录状态下可访问。

## 使用方法

```bash
# 运行Spider
scrapy crawl 临床试验数据共享平台_ts_ts_trialshare

# 限制采集数量（测试用）
scrapy crawl 临床试验数据共享平台_ts_ts_trialshare -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 临床试验数据共享平台_ts_ts_trialshare -o output.jsonl
```

## 输出格式

- JSONL格式: `output/临床试验数据共享平台_ts_ts_trialshare_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/临床试验数据共享平台_ts_ts_trialshare_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/临床试验数据共享平台_ts_ts_trialshare/
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

- **生成时间**: 2026-01-18 06:30:48
- **生成工具**: Spider Generator v1.0
