# 慢性疲劳综合征研究平台 mapMECFS mapMECFS (Myalgic Encephalomyelitis/Chronic Fatigue Syndrome Research Platform) Spider

## 基本信息

- **平台名称**: 慢性疲劳综合征研究平台 mapMECFS mapMECFS (Myalgic Encephalomyelitis/Chronic Fatigue Syndrome Research Platform)
- **平台URL**: https://mapmecfs.org
- **Spider名称**: 慢性疲劳综合征研究平台_mapmecfs_mapmecfs_myalgic_encephalomyelitischronic_fatigue_syndrome_research_platform
- **采集方法**: scrapy
- **难度评级**: ⭐⭐⭐⭐⭐
- **预估开发时间**: 8

## 采集策略

无分页，网站结构简单但当前访问受限，无法获取分页信息

## 数据字段

暂无字段信息

## 文件下载

由于当前无法访问有效页面，无法确认文件下载链接。若后续发现PDF或补充材料链接，使用Scrapy的FilesPipeline或自定义下载中间件进行下载

## 反爬应对

- 当前403 Forbidden错误，可能IP被封或服务器限制，建议更换IP或使用代理
- 设置合理请求头（User-Agent等）模拟浏览器请求
- 控制请求频率，避免触发服务器安全策略

## 注意事项

- 网站当前返回403 Forbidden，需确认访问权限或联系网站管理员获取授权
- 无登录，无API，无JavaScript渲染，采集难度主要在于突破访问限制
- 后续若网站结构有更新或开放API，需重新评估采集方案

## 使用方法

```bash
# 运行Spider
scrapy crawl 慢性疲劳综合征研究平台_mapmecfs_mapmecfs_myalgic_encephalomyelitischronic_fatigue_syndrome_research_platform

# 限制采集数量（测试用）
scrapy crawl 慢性疲劳综合征研究平台_mapmecfs_mapmecfs_myalgic_encephalomyelitischronic_fatigue_syndrome_research_platform -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 慢性疲劳综合征研究平台_mapmecfs_mapmecfs_myalgic_encephalomyelitischronic_fatigue_syndrome_research_platform -o output.jsonl
```

## 输出格式

- JSONL格式: `output/慢性疲劳综合征研究平台_mapmecfs_mapmecfs_myalgic_encephalomyelitischronic_fatigue_syndrome_research_platform_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/慢性疲劳综合征研究平台_mapmecfs_mapmecfs_myalgic_encephalomyelitischronic_fatigue_syndrome_research_platform_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/慢性疲劳综合征研究平台_mapmecfs_mapmecfs_myalgic_encephalomyelitischronic_fatigue_syndrome_research_platform/
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

- **生成时间**: 2026-01-18 06:43:17
- **生成工具**: Spider Generator v1.0
