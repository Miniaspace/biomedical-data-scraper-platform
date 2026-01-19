# 人类唾液蛋白质组维基 HSPW (Human Salivary Proteome Wiki) Spider

## 基本信息

- **平台名称**: 人类唾液蛋白质组维基 HSPW (Human Salivary Proteome Wiki)
- **平台URL**: https://salivaryproteome.org
- **Spider名称**: 人类唾液蛋白质组维基_hspw_human_salivary_proteome_wiki
- **采集方法**: hybrid
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

由于采用无限滚动（infinite_scroll），推荐使用Playwright模拟浏览器滚动触发加载更多数据，结合API接口分页参数请求数据，优先调用API获取数据列表以提升效率，Playwright负责登录和动态内容加载。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| institution | `ul li .institution` |


## 文件下载

PDF文件通过页面链接或API接口获取，登录态必须保持，下载时携带登录Cookie或Token，推荐使用requests会话或Playwright下载接口文件，支持断点续传和重试机制，确保文件完整性。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，执行JavaScript，避免因无JS环境被拦截。
- 保持登录状态，自动处理登录流程，避免因未登录导致数据无法访问。
- 控制请求频率，避免触发潜在的速率限制。
- 监控请求异常，自动重试失败请求。

## 注意事项

- 登录认证是采集前提，需实现自动登录及登录状态维持。
- API接口存在，优先调用API接口获取数据，减少页面渲染压力。
- 无限滚动加载需模拟滚动事件，确保数据全部加载。
- PDF文件下载需处理权限验证，确保下载链接有效。

## 使用方法

```bash
# 运行Spider
scrapy crawl 人类唾液蛋白质组维基_hspw_human_salivary_proteome_wiki

# 限制采集数量（测试用）
scrapy crawl 人类唾液蛋白质组维基_hspw_human_salivary_proteome_wiki -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 人类唾液蛋白质组维基_hspw_human_salivary_proteome_wiki -o output.jsonl
```

## 输出格式

- JSONL格式: `output/人类唾液蛋白质组维基_hspw_human_salivary_proteome_wiki_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/人类唾液蛋白质组维基_hspw_human_salivary_proteome_wiki_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/人类唾液蛋白质组维基_hspw_human_salivary_proteome_wiki/
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

- **生成时间**: 2026-01-18 06:37:47
- **生成工具**: Spider Generator v1.0
