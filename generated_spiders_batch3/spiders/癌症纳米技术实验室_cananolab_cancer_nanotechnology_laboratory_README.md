# 癌症纳米技术实验室 caNanoLab (Cancer Nanotechnology Laboratory) Spider

## 基本信息

- **平台名称**: 癌症纳米技术实验室 caNanoLab (Cancer Nanotechnology Laboratory)
- **平台URL**: https://cananolab.cancer.gov/#
- **Spider名称**: 癌症纳米技术实验室_cananolab_cancer_nanotechnology_laboratory
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

由于采用无限滚动(infinite_scroll)，使用Playwright模拟浏览器滚动页面，触发动态加载更多内容。通过循环执行页面底部滚动，等待新内容加载完成，直到无新内容加载或达到预设最大条数。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li .title, ul li h3, ul li a.title-link` |
| author | `ul li .author, ul li .authors` |
| publication_date | `ul li .date, ul li .pub-date` |
| abstract | `ul li .abstract, ul li .summary` |
| pdf_link | `ul li a[href$='.pdf']` |
| supplementary_material_link | `ul li a.supplementary, ul li a[href*='supplement']` |


## 文件下载

识别页面中所有PDF及补充材料链接，使用Playwright获取真实下载链接，结合登录状态发送带cookie的请求下载文件。支持断点续传和重试机制，文件命名采用唯一ID+原始文件名。

## 反爬应对

- 模拟真实用户行为，控制滚动速度和间隔，避免触发异常访问
- 保持登录状态，自动处理登录cookie和session
- 设置合理请求间隔，避免短时间内大量请求
- 使用Playwright无头浏览器，保证JavaScript正常执行，防止页面内容缺失

## 注意事项

- 登录流程复杂，需支持账号密码自动登录并验证登录成功
- 页面内容动态加载，需等待网络请求完成后再提取数据
- 无公开API，所有数据需通过页面渲染抓取
- 文件下载链接可能需要额外请求跳转或验证，需处理重定向和cookie

## 使用方法

```bash
# 运行Spider
scrapy crawl 癌症纳米技术实验室_cananolab_cancer_nanotechnology_laboratory

# 限制采集数量（测试用）
scrapy crawl 癌症纳米技术实验室_cananolab_cancer_nanotechnology_laboratory -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 癌症纳米技术实验室_cananolab_cancer_nanotechnology_laboratory -o output.jsonl
```

## 输出格式

- JSONL格式: `output/癌症纳米技术实验室_cananolab_cancer_nanotechnology_laboratory_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/癌症纳米技术实验室_cananolab_cancer_nanotechnology_laboratory_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/癌症纳米技术实验室_cananolab_cancer_nanotechnology_laboratory/
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

- **生成时间**: 2026-01-18 06:33:33
- **生成工具**: Spider Generator v1.0
