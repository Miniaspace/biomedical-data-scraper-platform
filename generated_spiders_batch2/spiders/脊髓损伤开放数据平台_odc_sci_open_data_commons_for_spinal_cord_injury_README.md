# 脊髓损伤开放数据平台 ODC-SCI (Open Data Commons for Spinal Cord Injury) Spider

## 基本信息

- **平台名称**: 脊髓损伤开放数据平台 ODC-SCI (Open Data Commons for Spinal Cord Injury)
- **平台URL**: https://odc-sci.org
- **Spider名称**: 脊髓损伤开放数据平台_odc_sci_open_data_commons_for_spinal_cord_injury
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

使用Playwright模拟用户滚动页面触发infinite scroll加载更多内容，循环检测新内容加载完成后继续滚动，直到无新内容加载为止

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `CSS选择器需基于详情页结构确定，如 'h1.article-title' 或类似元素` |
| author | `详情页中作者信息的CSS选择器，如 '.authors-list' 或 '.author-names'` |
| abstract | `详情页中摘要的选择器，如 '.abstract' 或 'section.abstract'` |
| publication_date | `详情页中日期选择器，如 '.pub-date'` |
| pdf_link | `详情页中PDF下载链接选择器，如 'a.pdf-download' 或 'a[href$='.pdf']'` |
| supplementary_materials | `详情页中补充材料链接选择器，如 '.supplementary a'` |


## 文件下载

在详情页解析PDF及补充材料链接后，通过Playwright获取带有登录态的请求头，使用Python requests或Playwright自带API下载文件，确保携带cookie和认证信息

## 反爬应对

- 使用Playwright模拟真实浏览器行为，执行JavaScript，避免因无JS执行导致数据缺失
- 保持登录状态，定期刷新cookie或重新登录以防会话过期
- 控制请求频率，避免触发潜在的速率限制

## 注意事项

- 登录流程需要自动化处理，可能涉及表单提交及验证码检测（目前无验证码）
- 详情页链接非标准链接（detail_link_pattern为'#'），需分析页面JS事件绑定或DOM结构，可能需要直接解析列表项中的隐藏数据或通过XHR请求获取详情数据
- 由于无公开API，所有数据均需通过页面渲染后抓取，增加采集复杂度

## 使用方法

```bash
# 运行Spider
scrapy crawl 脊髓损伤开放数据平台_odc_sci_open_data_commons_for_spinal_cord_injury

# 限制采集数量（测试用）
scrapy crawl 脊髓损伤开放数据平台_odc_sci_open_data_commons_for_spinal_cord_injury -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 脊髓损伤开放数据平台_odc_sci_open_data_commons_for_spinal_cord_injury -o output.jsonl
```

## 输出格式

- JSONL格式: `output/脊髓损伤开放数据平台_odc_sci_open_data_commons_for_spinal_cord_injury_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/脊髓损伤开放数据平台_odc_sci_open_data_commons_for_spinal_cord_injury_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/脊髓损伤开放数据平台_odc_sci_open_data_commons_for_spinal_cord_injury/
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

- **生成时间**: 2026-01-18 06:26:59
- **生成工具**: Spider Generator v1.0
