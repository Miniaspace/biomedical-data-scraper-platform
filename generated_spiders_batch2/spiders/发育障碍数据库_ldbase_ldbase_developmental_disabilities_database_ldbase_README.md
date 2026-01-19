# 发育障碍数据库 LDbase LDbase (Developmental Disabilities Database LDbase) Spider

## 基本信息

- **平台名称**: 发育障碍数据库 LDbase LDbase (Developmental Disabilities Database LDbase)
- **平台URL**: https://ldbase.org
- **Spider名称**: 发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动(infinite_scroll)分页，使用Playwright模拟用户滚动页面到底部，等待新数据加载，循环此过程直到没有新数据加载为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `css=ul li .title, xpath=./descendant::*[contains(@class,'title')]` |
| author | `css=ul li .author, xpath=./descendant::*[contains(@class,'author')]` |
| date | `css=ul li .date, xpath=./descendant::*[contains(@class,'date')]` |
| description | `css=ul li .description, xpath=./descendant::*[contains(@class,'description')]` |
| pdf_link | `css=ul li a[href$='.pdf']` |
| supplementary_material_link | `css=ul li a.supplementary-material` |


## 文件下载

登录后通过Playwright获取文件下载链接，使用带有登录状态的会话进行文件下载。对PDF及补充材料链接进行请求并保存。支持断点续传和重试机制。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免因无头浏览器特征被识别。
- 合理设置滚动和请求间隔，避免触发服务器异常。
- 登录时保存并复用cookie，减少频繁登录。
- 监控页面变化，若出现登录失效或验证码提示，自动报警或暂停采集。

## 注意事项

- 网站需要登录，需实现自动登录流程并处理登录失败。
- 无公开API，所有数据需通过页面解析获取。
- 无限滚动分页需确保滚动到底部后等待数据加载完成，避免遗漏数据。
- 文件下载需保证登录态有效，避免下载失败。
- 部分数据字段可能不固定，需根据实际页面结构灵活调整选择器。

## 使用方法

```bash
# 运行Spider
scrapy crawl 发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase

# 限制采集数量（测试用）
scrapy crawl 发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase -o output.jsonl
```

## 输出格式

- JSONL格式: `output/发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase/
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

- **生成时间**: 2026-01-18 06:29:55
- **生成工具**: Spider Generator v1.0
