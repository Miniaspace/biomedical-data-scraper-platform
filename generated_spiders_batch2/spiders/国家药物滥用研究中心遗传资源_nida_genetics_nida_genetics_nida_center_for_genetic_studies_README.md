# 国家药物滥用研究中心遗传资源 NIDA Genetics (NIDA Genetics (NIDA Center for Genetic Studies)) Spider

## 基本信息

- **平台名称**: 国家药物滥用研究中心遗传资源 NIDA Genetics (NIDA Genetics (NIDA Center for Genetic Studies))
- **平台URL**: https://nidagenetics.org
- **Spider名称**: 国家药物滥用研究中心遗传资源_nida_genetics_nida_genetics_nida_center_for_genetic_studies
- **采集方法**: scrapy
- **难度评级**: ⭐⭐
- **预估开发时间**: 8

## 采集策略

由于页面采用无限滚动(infinite_scroll)且无API支持，建议通过模拟滚动加载更多数据，结合Scrapy的中间件或扩展实现动态内容抓取，或结合Playwright辅助实现页面滚动后抓取完整表格数据。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| all_fields | `td` |


## 文件下载

检测表格中是否含有文件下载链接（如PDF、补充材料），通过提取对应的<a>标签href属性进行文件下载，使用Scrapy的FilesPipeline或自定义下载逻辑保存文件。

## 反爬应对

- 由于无明显反爬机制，保持适当抓取频率避免触发服务器限制
- 设置合理User-Agent，避免默认爬虫标识
- 使用IP代理池可选，防止IP封禁风险

## 注意事项

- 页面内容为静态HTML，无需执行JavaScript，减少复杂度
- 无限滚动加载可能需要结合Playwright或Splash辅助实现完整数据采集
- 无登录，采集门槛较低

## 使用方法

```bash
# 运行Spider
scrapy crawl 国家药物滥用研究中心遗传资源_nida_genetics_nida_genetics_nida_center_for_genetic_studies

# 限制采集数量（测试用）
scrapy crawl 国家药物滥用研究中心遗传资源_nida_genetics_nida_genetics_nida_center_for_genetic_studies -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 国家药物滥用研究中心遗传资源_nida_genetics_nida_genetics_nida_center_for_genetic_studies -o output.jsonl
```

## 输出格式

- JSONL格式: `output/国家药物滥用研究中心遗传资源_nida_genetics_nida_genetics_nida_center_for_genetic_studies_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/国家药物滥用研究中心遗传资源_nida_genetics_nida_genetics_nida_center_for_genetic_studies_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/国家药物滥用研究中心遗传资源_nida_genetics_nida_genetics_nida_center_for_genetic_studies/
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

- **生成时间**: 2026-01-18 06:20:07
- **生成工具**: Spider Generator v1.0
