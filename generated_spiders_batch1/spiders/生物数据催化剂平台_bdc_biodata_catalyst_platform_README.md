# 生物数据催化剂平台 BDC (BioData Catalyst Platform) Spider

## 基本信息

- **平台名称**: 生物数据催化剂平台 BDC (BioData Catalyst Platform)
- **平台URL**: https://biodatacatalyst.nhlbi.nih.gov
- **Spider名称**: 生物数据催化剂平台_bdc_biodata_catalyst_platform
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

无传统分页，需通过动态加载或滚动加载方式采集，Playwright模拟用户操作触发数据加载

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `待定，需根据具体页面结构用CSS或XPath定位，如 //h1 或 .title` |
| author | `待定，类似 //div[@class='author'] 或 .author` |
| publication_date | `待定` |
| abstract | `待定` |
| pdf_link | `a[href$='.pdf']` |
| supplementary_materials | `a[href*='supplement']` |


## 文件下载

通过Playwright捕获页面中PDF及补充材料的下载链接，使用Playwright或requests结合cookie和header完成文件下载，避免直接暴露下载地址导致反爬

## 反爬应对

- 使用Playwright模拟真实浏览器环境，执行JavaScript，绕过JS验证
- 针对验证码，结合手动或第三方验证码识别服务，或采用人工辅助方式
- 控制请求频率，避免触发验证码和封禁
- 使用代理池分散访问IP

## 注意事项

- 网站强制人机验证，自动化采集难度大，需结合人工辅助
- 无公开API，需逆向分析动态加载数据接口
- 文件下载需保持登录态或验证态，确保链接有效
- 采集前需确认版权及使用合规性

## 使用方法

```bash
# 运行Spider
scrapy crawl 生物数据催化剂平台_bdc_biodata_catalyst_platform

# 限制采集数量（测试用）
scrapy crawl 生物数据催化剂平台_bdc_biodata_catalyst_platform -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 生物数据催化剂平台_bdc_biodata_catalyst_platform -o output.jsonl
```

## 输出格式

- JSONL格式: `output/生物数据催化剂平台_bdc_biodata_catalyst_platform_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/生物数据催化剂平台_bdc_biodata_catalyst_platform_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/生物数据催化剂平台_bdc_biodata_catalyst_platform/
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

- **生成时间**: 2026-01-18 06:14:33
- **生成工具**: Spider Generator v1.0
