# 帕金森病生物标志物计划 PDBP (Parkinson's Disease Biomarker Program) Spider

## 基本信息

- **平台名称**: 帕金森病生物标志物计划 PDBP (Parkinson's Disease Biomarker Program)
- **平台URL**: https://pdbp.ninds.nih.gov
- **Spider名称**: 帕金森病生物标志物计划_pdbp_parkinsons_disease_biomarker_program
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

由于采用无限滚动(infinite scroll)，使用Playwright模拟页面滚动，等待新内容加载，直到无新数据加载为止。通过监听网络请求或DOM变化判断加载完成。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li .title, ul li h3, ul li a.title` |
| author | `ul li .author, ul li .meta .author` |
| date | `ul li .date, ul li .meta .date` |
| summary | `ul li .summary, ul li .description` |
| pdf_link | `ul li a[href$='.pdf']` |


## 文件下载

针对PDF及补充材料链接，使用Playwright获取完整下载URL，结合登录状态发送带Cookie的请求下载文件，支持断点续传和重试机制。

## 反爬应对

- 模拟真实用户行为，控制滚动速度和间隔，避免触发异常
- 保持登录状态，管理好Cookie和Session
- 设置合理请求间隔，防止服务器压力过大

## 注意事项

- 登录流程复杂，需处理验证码或多因素认证（若存在）
- 网站基于Drupal 10，页面结构可能动态变化，需定期维护选择器
- 无公开API，所有数据需通过页面渲染抓取
- 文件下载需鉴权，确保请求头携带登录信息

## 使用方法

```bash
# 运行Spider
scrapy crawl 帕金森病生物标志物计划_pdbp_parkinsons_disease_biomarker_program

# 限制采集数量（测试用）
scrapy crawl 帕金森病生物标志物计划_pdbp_parkinsons_disease_biomarker_program -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 帕金森病生物标志物计划_pdbp_parkinsons_disease_biomarker_program -o output.jsonl
```

## 输出格式

- JSONL格式: `output/帕金森病生物标志物计划_pdbp_parkinsons_disease_biomarker_program_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/帕金森病生物标志物计划_pdbp_parkinsons_disease_biomarker_program_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/帕金森病生物标志物计划_pdbp_parkinsons_disease_biomarker_program/
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

- **生成时间**: 2026-01-18 06:23:15
- **生成工具**: Spider Generator v1.0
