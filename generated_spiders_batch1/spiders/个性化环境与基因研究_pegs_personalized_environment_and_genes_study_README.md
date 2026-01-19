# 个性化环境与基因研究 PEGS (Personalized Environment and Genes Study) Spider

## 基本信息

- **平台名称**: 个性化环境与基因研究 PEGS (Personalized Environment and Genes Study)
- **平台URL**: https://niehs.nih.gov/research/atniehs/labs/crb/studies/pegs
- **Spider名称**: 个性化环境与基因研究_pegs_personalized_environment_and_genes_study
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

无分页，直接采集单页面所有可见内容

## 数据字段

暂无字段信息

## 文件下载

通过Playwright模拟浏览器环境，等待页面完全加载后，定位PDF及补充材料链接，使用Playwright的下载功能或requests库结合cookies进行文件下载

## 反爬应对

- 使用Playwright模拟真实浏览器行为，绕过Cloudflare的JS挑战
- 合理设置请求间隔，避免触发验证码
- 启用代理IP池，分散访问压力
- 自动识别并等待Cloudflare挑战页面通过后再进行数据抓取

## 注意事项

- 页面被Cloudflare保护，普通Scrapy无法直接访问，必须使用Playwright或类似工具
- 页面无API接口，数据需从渲染后的HTML中提取
- 页面无分页，数据量可能有限，但需确保页面完全加载
- 验证码存在，若触发需人工干预或采用第三方验证码识别服务

## 使用方法

```bash
# 运行Spider
scrapy crawl 个性化环境与基因研究_pegs_personalized_environment_and_genes_study

# 限制采集数量（测试用）
scrapy crawl 个性化环境与基因研究_pegs_personalized_environment_and_genes_study -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 个性化环境与基因研究_pegs_personalized_environment_and_genes_study -o output.jsonl
```

## 输出格式

- JSONL格式: `output/个性化环境与基因研究_pegs_personalized_environment_and_genes_study_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/个性化环境与基因研究_pegs_personalized_environment_and_genes_study_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/个性化环境与基因研究_pegs_personalized_environment_and_genes_study/
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

- **生成时间**: 2026-01-18 06:16:51
- **生成工具**: Spider Generator v1.0
