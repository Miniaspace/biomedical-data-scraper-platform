# 美国国家人类基因组研究所基因组数据科学分析、可视化与信息学实验室空间 AnVIL (The NHGRI Genomic Data Science Analysis, Visualization, and Informatics Lab-space) Spider

## 基本信息

- **平台名称**: 美国国家人类基因组研究所基因组数据科学分析、可视化与信息学实验室空间 AnVIL (The NHGRI Genomic Data Science Analysis, Visualization, and Informatics Lab-space)
- **平台URL**: https://anvilproject.org/learn/accessing-data/requesting-data-access
- **Spider名称**: 美国国家人类基因组研究所基因组数据科学分析可视化与信息学实验室空间_anvil_the_nhgri_genomic_data_science_analysis_visualization_and_informatics_lab_space
- **采集方法**: scrapy
- **难度评级**: ⭐
- **预估开发时间**: 4

## 采集策略

通过检测页面底部的“Next”按钮，使用Scrapy的follow机制自动跟踪下一页链接，直到无下一页按钮为止。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul li a::text` |
| author | `ul li .author::text` |


## 文件下载

在详情页中解析PDF或补充材料的下载链接（通常为a标签href包含.pdf或相关文件后缀），使用Scrapy的FilesPipeline或自定义下载中间件进行文件下载和存储。

## 反爬应对

- 由于无登录、无验证码、无复杂反爬机制，保持合理的请求间隔即可避免被封禁。
- 设置User-Agent模拟常见浏览器，避免被简单的UA检测封禁。

## 注意事项

- 网站无API，且内容静态加载，无需使用Playwright等浏览器自动化工具，节省资源。
- 确认详情页链接格式稳定，避免因链接格式变化导致采集失败。
- 部分文件可能托管在第三方站点，需确认下载链接有效性。

## 使用方法

```bash
# 运行Spider
scrapy crawl 美国国家人类基因组研究所基因组数据科学分析可视化与信息学实验室空间_anvil_the_nhgri_genomic_data_science_analysis_visualization_and_informatics_lab_space

# 限制采集数量（测试用）
scrapy crawl 美国国家人类基因组研究所基因组数据科学分析可视化与信息学实验室空间_anvil_the_nhgri_genomic_data_science_analysis_visualization_and_informatics_lab_space -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 美国国家人类基因组研究所基因组数据科学分析可视化与信息学实验室空间_anvil_the_nhgri_genomic_data_science_analysis_visualization_and_informatics_lab_space -o output.jsonl
```

## 输出格式

- JSONL格式: `output/美国国家人类基因组研究所基因组数据科学分析可视化与信息学实验室空间_anvil_the_nhgri_genomic_data_science_analysis_visualization_and_informatics_lab_space_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/美国国家人类基因组研究所基因组数据科学分析可视化与信息学实验室空间_anvil_the_nhgri_genomic_data_science_analysis_visualization_and_informatics_lab_space_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/美国国家人类基因组研究所基因组数据科学分析可视化与信息学实验室空间_anvil_the_nhgri_genomic_data_science_analysis_visualization_and_informatics_lab_space/
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

- **生成时间**: 2026-01-18 06:16:11
- **生成工具**: Spider Generator v1.0
