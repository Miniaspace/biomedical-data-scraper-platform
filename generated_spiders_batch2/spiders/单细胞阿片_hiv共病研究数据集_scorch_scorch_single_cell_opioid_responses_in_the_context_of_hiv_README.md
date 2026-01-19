# 单细胞阿片-HIV共病研究数据集 SCORCH SCORCH (Single Cell Opioid Responses in the Context of HIV) Spider

## 基本信息

- **平台名称**: 单细胞阿片-HIV共病研究数据集 SCORCH SCORCH (Single Cell Opioid Responses in the Context of HIV)
- **平台URL**: https://nida.nih.gov/about-nida/organization/divisions/division-neuroscience-behavior-dnb/basic-research-hiv-substance-use-disorder/scorch-program
- **Spider名称**: 单细胞阿片_hiv共病研究数据集_scorch_scorch_single_cell_opioid_responses_in_the_context_of_hiv
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 8

## 采集策略

由于页面采用无限滚动加载，但检测到页面内容为静态HTML且无API支持，建议通过Scrapy抓取初始页面所有ul li元素，若内容动态加载则需结合Playwright模拟滚动加载后抓取完整内容。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li > a::text` |
| link | `ul li > a::attr(href)` |


## 文件下载

页面未检测到可下载文件链接，若后续详情页或列表中出现PDF或补充材料链接，使用Scrapy的FilesPipeline或requests模块下载，需确保链接为完整URL或拼接域名后下载。

## 反爬应对

- 无验证码和明显反爬限制，保持合理请求间隔避免触发服务器限流
- 设置User-Agent模拟浏览器请求，避免被简单封禁

## 注意事项

- 页面内容较为静态，无需执行JavaScript，Scrapy即可满足需求
- 列表项链接pattern为“/”，需确认详情页链接是否存在，若无详情页，直接采集列表信息
- 因无API支持，且内容量较大（130条），建议分批抓取，避免请求超时

## 使用方法

```bash
# 运行Spider
scrapy crawl 单细胞阿片_hiv共病研究数据集_scorch_scorch_single_cell_opioid_responses_in_the_context_of_hiv

# 限制采集数量（测试用）
scrapy crawl 单细胞阿片_hiv共病研究数据集_scorch_scorch_single_cell_opioid_responses_in_the_context_of_hiv -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 单细胞阿片_hiv共病研究数据集_scorch_scorch_single_cell_opioid_responses_in_the_context_of_hiv -o output.jsonl
```

## 输出格式

- JSONL格式: `output/单细胞阿片_hiv共病研究数据集_scorch_scorch_single_cell_opioid_responses_in_the_context_of_hiv_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/单细胞阿片_hiv共病研究数据集_scorch_scorch_single_cell_opioid_responses_in_the_context_of_hiv_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/单细胞阿片_hiv共病研究数据集_scorch_scorch_single_cell_opioid_responses_in_the_context_of_hiv/
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

- **生成时间**: 2026-01-18 06:29:34
- **生成工具**: Spider Generator v1.0
