# 包容性神经发育数据平台 INCLUDE (INCLUDE 数据中心) INCLUDE (Inclusive Neurodevelopmental Data Platform INCLUDE (INCLUDE Data Hub)) Spider

## 基本信息

- **平台名称**: 包容性神经发育数据平台 INCLUDE (INCLUDE 数据中心) INCLUDE (Inclusive Neurodevelopmental Data Platform INCLUDE (INCLUDE Data Hub))
- **平台URL**: https://portal.includedcc.org/login?redirect_path=/dashboard
- **Spider名称**: 包容性神经发育数据平台_include_include_数据中心_include_inclusive_neurodevelopmental_data_platform_include_include_data_hub
- **采集方法**: hybrid
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无传统分页，利用API接口的参数（如offset/limit或page）进行分页请求，直到返回空数据或无更多数据标志

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `根据API返回的JSON字段提取，如data.title` |
| author | `根据API返回的JSON字段提取，如data.author` |
| publication_date | `根据API返回的JSON字段提取，如data.pub_date` |
| pdf_url | `根据API返回的JSON字段提取，如data.pdf_url` |
| supplementary_materials | `根据API返回的JSON字段提取，如data.supplementary_files` |


## 文件下载

通过解析API返回的文件URL，使用带登录状态的请求头（如Cookies或Token）进行文件下载，支持断点续传和重试机制

## 反爬应对

- 使用Playwright模拟登录，保持会话状态，避免频繁登录触发限制
- 合理控制请求频率，避免触发服务器异常检测
- 利用API接口数据，减少页面渲染和复杂DOM解析，降低被检测概率

## 注意事项

- 登录流程需模拟完整，包括验证码无但需处理多因素认证或动态token
- API请求可能包含动态签名或token，需分析请求头和参数，动态生成
- 确保文件下载时携带有效身份验证信息，避免403错误

## 使用方法

```bash
# 运行Spider
scrapy crawl 包容性神经发育数据平台_include_include_数据中心_include_inclusive_neurodevelopmental_data_platform_include_include_data_hub

# 限制采集数量（测试用）
scrapy crawl 包容性神经发育数据平台_include_include_数据中心_include_inclusive_neurodevelopmental_data_platform_include_include_data_hub -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 包容性神经发育数据平台_include_include_数据中心_include_inclusive_neurodevelopmental_data_platform_include_include_data_hub -o output.jsonl
```

## 输出格式

- JSONL格式: `output/包容性神经发育数据平台_include_include_数据中心_include_inclusive_neurodevelopmental_data_platform_include_include_data_hub_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/包容性神经发育数据平台_include_include_数据中心_include_inclusive_neurodevelopmental_data_platform_include_include_data_hub_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/包容性神经发育数据平台_include_include_数据中心_include_inclusive_neurodevelopmental_data_platform_include_include_data_hub/
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

- **生成时间**: 2026-01-18 06:27:19
- **生成工具**: Spider Generator v1.0
