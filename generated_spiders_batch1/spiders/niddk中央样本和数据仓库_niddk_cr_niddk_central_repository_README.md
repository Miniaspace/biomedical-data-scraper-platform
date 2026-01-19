# NIDDK中央样本和数据仓库 NIDDK CR (NIDDK Central Repository) Spider

## 基本信息

- **平台名称**: NIDDK中央样本和数据仓库 NIDDK CR (NIDDK Central Repository)
- **平台URL**: https://repository.niddk.nih.gov/home
- **Spider名称**: niddk中央样本和数据仓库_niddk_cr_niddk_central_repository
- **采集方法**: scrapy
- **难度评级**: ⭐⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

无分页，因网站返回403 Forbidden，无法访问数据列表，需先解决访问权限问题

## 数据字段

暂无字段信息

## 文件下载

待获取有效页面后，根据文件链接进行直接HTTP请求下载，支持断点续传和重试机制

## 反爬应对

- 确认IP是否被封禁，尝试更换IP或使用代理
- 检查请求头，模拟浏览器User-Agent及Referer
- 尝试使用浏览器自动化工具（Playwright）模拟真实用户行为
- 联系网站管理员确认访问权限及数据开放政策

## 注意事项

- 当前访问主页返回403 Forbidden，说明存在访问限制，需先解决访问权限问题
- 无API接口及分页，数据结构未知，采集前需获取有效页面结构
- 无登录需求，反爬机制较弱，但访问受限可能为IP或区域限制
- 采集前建议先人工访问确认数据可见性及下载链接格式

## 使用方法

```bash
# 运行Spider
scrapy crawl niddk中央样本和数据仓库_niddk_cr_niddk_central_repository

# 限制采集数量（测试用）
scrapy crawl niddk中央样本和数据仓库_niddk_cr_niddk_central_repository -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl niddk中央样本和数据仓库_niddk_cr_niddk_central_repository -o output.jsonl
```

## 输出格式

- JSONL格式: `output/niddk中央样本和数据仓库_niddk_cr_niddk_central_repository_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/niddk中央样本和数据仓库_niddk_cr_niddk_central_repository_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/niddk中央样本和数据仓库_niddk_cr_niddk_central_repository/
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

- **生成时间**: 2026-01-18 06:14:18
- **生成工具**: Spider Generator v1.0
