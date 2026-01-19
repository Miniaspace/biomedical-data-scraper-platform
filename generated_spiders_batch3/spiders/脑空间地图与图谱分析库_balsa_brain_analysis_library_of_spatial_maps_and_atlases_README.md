# 脑空间地图与图谱分析库 BALSA (Brain Analysis Library of Spatial Maps and Atlases) Spider

## 基本信息

- **平台名称**: 脑空间地图与图谱分析库 BALSA (Brain Analysis Library of Spatial Maps and Atlases)
- **平台URL**: https://balsa.wustl.edu
- **Spider名称**: 脑空间地图与图谱分析库_balsa_brain_analysis_library_of_spatial_maps_and_atlases
- **采集方法**: scrapy+playwright (hybrid)
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

通过点击页面底部的“Next”按钮进行分页，使用Playwright模拟点击操作，等待页面加载完成后抓取下一页数据，直到“Next”按钮不可用或不存在为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `td:nth-child(1) a::text` |
| detail_link | `td:nth-child(1) a::attr(href)` |
| author | `td:nth-child(2)::text` |
| date | `td:nth-child(3)::text` |
| status | `td:nth-child(4)::text` |


## 文件下载

在详情页中定位PDF文件及补充材料的下载链接，使用Scrapy的文件下载管道结合Playwright处理登录态和权限验证后，异步下载文件。文件下载前需确保已登录且有访问权限。

## 反爬应对

- 使用Playwright模拟登录，保持登录态，避免频繁登录导致账号异常。
- 合理设置请求间隔，避免触发服务器的访问频率限制。
- 使用代理池分散请求来源，降低被封风险。
- 监控页面变化，动态调整选择器，防止因页面结构调整导致采集失败。

## 注意事项

- 登录过程需要处理表单提交，可能包含CSRF token，需动态获取并提交。
- 网站无API，数据需通过页面解析获取，且无明显JavaScript渲染，Playwright主要用于登录和分页点击。
- 文件下载链接可能是动态生成或带有权限校验，需保持登录状态并使用Playwright抓取最终下载链接。
- 无验证码和Cloudflare，反爬门槛较低，但仍需注意账号安全和访问频率。

## 使用方法

```bash
# 运行Spider
scrapy crawl 脑空间地图与图谱分析库_balsa_brain_analysis_library_of_spatial_maps_and_atlases

# 限制采集数量（测试用）
scrapy crawl 脑空间地图与图谱分析库_balsa_brain_analysis_library_of_spatial_maps_and_atlases -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 脑空间地图与图谱分析库_balsa_brain_analysis_library_of_spatial_maps_and_atlases -o output.jsonl
```

## 输出格式

- JSONL格式: `output/脑空间地图与图谱分析库_balsa_brain_analysis_library_of_spatial_maps_and_atlases_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/脑空间地图与图谱分析库_balsa_brain_analysis_library_of_spatial_maps_and_atlases_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/脑空间地图与图谱分析库_balsa_brain_analysis_library_of_spatial_maps_and_atlases/
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

- **生成时间**: 2026-01-18 06:43:03
- **生成工具**: Spider Generator v1.0
