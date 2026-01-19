# 国家酒精滥用与酒精中毒研究所数据档案 NIAAA-DA (National Institute on Alcohol Abuse and Alcoholism Data Archive) Spider

## 基本信息

- **平台名称**: 国家酒精滥用与酒精中毒研究所数据档案 NIAAA-DA (National Institute on Alcohol Abuse and Alcoholism Data Archive)
- **平台URL**: https://nda.nih.gov/niaaa
- **Spider名称**: 国家酒精滥用与酒精中毒研究所数据档案_niaaa_da_national_institute_on_alcohol_abuse_and_alcoholism_data_archive
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无分页，页面全部数据一次性加载，无需分页处理

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li > a > text()` |
| link | `li > a::attr(href)` |


## 文件下载

登录后通过Playwright模拟用户点击下载链接，自动处理文件保存路径和重命名，支持断点续传和重试机制

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免因无头浏览器特征被识别
- 合理设置请求间隔，避免触发登录会话异常
- 保存和复用登录状态Cookies，减少重复登录次数

## 注意事项

- 必须先完成登录，登录流程可能涉及多因素认证，需人工辅助或预置账号信息
- 页面无API接口，需解析HTML，结构较简单但需确保登录状态有效
- 文件下载链接可能动态生成，需在登录状态下动态抓取

## 使用方法

```bash
# 运行Spider
scrapy crawl 国家酒精滥用与酒精中毒研究所数据档案_niaaa_da_national_institute_on_alcohol_abuse_and_alcoholism_data_archive

# 限制采集数量（测试用）
scrapy crawl 国家酒精滥用与酒精中毒研究所数据档案_niaaa_da_national_institute_on_alcohol_abuse_and_alcoholism_data_archive -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国家酒精滥用与酒精中毒研究所数据档案_niaaa_da_national_institute_on_alcohol_abuse_and_alcoholism_data_archive -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国家酒精滥用与酒精中毒研究所数据档案_niaaa_da_national_institute_on_alcohol_abuse_and_alcoholism_data_archive_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国家酒精滥用与酒精中毒研究所数据档案_niaaa_da_national_institute_on_alcohol_abuse_and_alcoholism_data_archive_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国家酒精滥用与酒精中毒研究所数据档案_niaaa_da_national_institute_on_alcohol_abuse_and_alcoholism_data_archive/
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

- **生成时间**: 2026-01-18 06:25:54
- **生成工具**: Spider Generator v1.0
