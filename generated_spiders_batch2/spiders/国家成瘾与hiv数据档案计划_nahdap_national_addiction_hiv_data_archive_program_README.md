# 国家成瘾与HIV数据档案计划 NAHDAP (National Addiction & HIV Data Archive Program) Spider

## 基本信息

- **平台名称**: 国家成瘾与HIV数据档案计划 NAHDAP (National Addiction & HIV Data Archive Program)
- **平台URL**: https://icpsr.umich.edu/web/pages/NAHDAP/data/index.html
- **Spider名称**: 国家成瘾与hiv数据档案计划_nahdap_national_addiction_hiv_data_archive_program
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动(infinite scroll)，使用Playwright模拟用户滚动页面，等待新内容加载，直到所有数据加载完成或达到预设最大条数。结合页面元素变化判断加载结束。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li > a > h3, ul li > a > div.title, or ul li > a (根据具体结构调整)` |
| author | `ul li .author, ul li .contributor (需根据实际DOM确认)` |
| description | `ul li .description, ul li p.summary` |
| download_links | `a[href$='.pdf'], a[href*='supplemental'], a.download-link` |


## 文件下载

拦截页面中的文件下载链接，结合Playwright的下载API进行文件下载。对PDF和补充材料链接单独处理，确保文件完整性。支持断点续传和重试机制。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免简单UA检测
- 合理设置请求间隔，避免触发Cloudflare防护
- 登录环节采用自动化填写表单和Cookie持久化，减少重复登录
- 使用代理池分散请求IP，降低被封风险

## 注意事项

- 登录是必须步骤，需提前获取有效账号和密码
- Cloudflare防护可能导致请求延迟，需设置合理超时和重试
- 无限滚动加载可能导致内存占用较高，需分批保存数据
- 页面结构可能动态变化，需定期维护选择器

## 使用方法

```bash
# 运行Spider
scrapy crawl 国家成瘾与hiv数据档案计划_nahdap_national_addiction_hiv_data_archive_program

# 限制采集数量（测试用）
scrapy crawl 国家成瘾与hiv数据档案计划_nahdap_national_addiction_hiv_data_archive_program -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国家成瘾与hiv数据档案计划_nahdap_national_addiction_hiv_data_archive_program -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国家成瘾与hiv数据档案计划_nahdap_national_addiction_hiv_data_archive_program_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国家成瘾与hiv数据档案计划_nahdap_national_addiction_hiv_data_archive_program_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国家成瘾与hiv数据档案计划_nahdap_national_addiction_hiv_data_archive_program/
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

- **生成时间**: 2026-01-18 06:28:17
- **生成工具**: Spider Generator v1.0
