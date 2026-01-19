# 大脑倡议数据档案库 DABI (Data Archive for the BRAIN Initiative) Spider

## 基本信息

- **平台名称**: 大脑倡议数据档案库 DABI (Data Archive for the BRAIN Initiative)
- **平台URL**: https://dabi.loni.usc.edu
- **Spider名称**: 大脑倡议数据档案库_dabi_data_archive_for_the_brain_initiative
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

使用Playwright模拟用户滚动页面，触发infinite scroll加载更多数据，直到加载完所有数据或达到预设的最大条数。通过监听网络请求或DOM变化确认新数据加载完成。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `h1.record-title` |
| authors | `div.authors-list > span.author-name` |
| publication_date | `span.pub-date` |
| abstract | `div.abstract-section > p` |
| pdf_link | `a.download-pdf[href$='.pdf']` |
| supplementary_materials | `a.supplementary-download` |


## 文件下载

通过Playwright拦截下载链接，结合登录态请求PDF及补充材料文件，保存到本地。对大文件采用分块下载或断点续传策略，确保文件完整性。

## 反爬应对

- 模拟真实用户行为，控制滚动速度和间隔，避免触发异常检测
- 保持登录态Cookie和Session，定期刷新登录状态
- 设置合理的请求间隔，避免频繁请求导致账号封禁

## 注意事项

- 登录流程需要处理多因素认证或验证码时需额外开发对应模块
- 页面数据依赖JavaScript渲染，纯Scrapy无法有效采集
- 文件下载链接可能动态生成，需在详情页完全加载后提取

## 使用方法

```bash
# 运行Spider
scrapy crawl 大脑倡议数据档案库_dabi_data_archive_for_the_brain_initiative

# 限制采集数量（测试用）
scrapy crawl 大脑倡议数据档案库_dabi_data_archive_for_the_brain_initiative -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 大脑倡议数据档案库_dabi_data_archive_for_the_brain_initiative -o output.jsonl
```

## 输出格式

- JSONL格式: `output/大脑倡议数据档案库_dabi_data_archive_for_the_brain_initiative_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/大脑倡议数据档案库_dabi_data_archive_for_the_brain_initiative_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/大脑倡议数据档案库_dabi_data_archive_for_the_brain_initiative/
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

- **生成时间**: 2026-01-18 06:18:50
- **生成工具**: Spider Generator v1.0
