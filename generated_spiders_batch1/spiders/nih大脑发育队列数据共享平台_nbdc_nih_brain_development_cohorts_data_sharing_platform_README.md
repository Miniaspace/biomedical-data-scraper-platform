# NIH大脑发育队列数据共享平台 NBDC (NIH Brain Development Cohorts Data Sharing Platform) Spider

## 基本信息

- **平台名称**: NIH大脑发育队列数据共享平台 NBDC (NIH Brain Development Cohorts Data Sharing Platform)
- **平台URL**: https://sharing.nih.gov/accessing-data/NIH-security-best-practices
- **Spider名称**: nih大脑发育队列数据共享平台_nbdc_nih_brain_development_cohorts_data_sharing_platform
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 16

## 采集策略

无分页，所有数据均在单页table中展示，无需分页处理

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `td:nth-child(1)` |
| description | `td:nth-child(2)` |
| pdf_link | `td a[href$='.pdf']` |


## 文件下载

通过Playwright登录后，直接访问PDF链接进行下载，保持登录状态以确保权限，支持断点续传和重试机制

## 反爬应对

- 使用Playwright模拟真实浏览器行为，绕过Cloudflare防护
- 保持登录会话，避免频繁登录导致封禁
- 控制请求频率，避免触发潜在的速率限制

## 注意事项

- 登录流程需处理NIH身份验证，可能涉及多因素认证，需提前准备账号和凭证
- Cloudflare防护可能会动态变化，需定期维护Playwright脚本
- PDF文件下载需确保权限验证，避免无权限访问导致下载失败

## 使用方法

```bash
# 运行Spider
scrapy crawl nih大脑发育队列数据共享平台_nbdc_nih_brain_development_cohorts_data_sharing_platform

# 限制采集数量（测试用）
scrapy crawl nih大脑发育队列数据共享平台_nbdc_nih_brain_development_cohorts_data_sharing_platform -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl nih大脑发育队列数据共享平台_nbdc_nih_brain_development_cohorts_data_sharing_platform -o output.jsonl
```

## 输出格式

- JSONL格式: `output/nih大脑发育队列数据共享平台_nbdc_nih_brain_development_cohorts_data_sharing_platform_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/nih大脑发育队列数据共享平台_nbdc_nih_brain_development_cohorts_data_sharing_platform_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/nih大脑发育队列数据共享平台_nbdc_nih_brain_development_cohorts_data_sharing_platform/
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

- **生成时间**: 2026-01-18 06:17:22
- **生成工具**: Spider Generator v1.0
