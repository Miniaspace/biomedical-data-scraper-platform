# 身体活动分子传感器联盟 MoTrPAC (Molecular Transducers of Physical Activity Consortium) Spider

## 基本信息

- **平台名称**: 身体活动分子传感器联盟 MoTrPAC (Molecular Transducers of Physical Activity Consortium)
- **平台URL**: https://motrpac-data.org
- **Spider名称**: 身体活动分子传感器联盟_motrpac_molecular_transducers_of_physical_activity_consortium
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐⭐
- **预估开发时间**: 40

## 采集策略

使用Playwright模拟用户滚动页面，触发页面的infinite scroll加载更多数据。通过监听网络请求或等待新列表元素加载完成，循环滚动直到无新数据加载。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `li .title, li h3, li a.title` |
| author | `li .author, li .meta .author` |
| date | `li .date, li .meta .date` |
| description | `li .description, li p.summary` |


## 文件下载

在详情页通过Playwright点击下载链接或直接请求文件URL，结合登录状态保持cookies和headers，支持PDF及补充材料的下载。下载时保存文件名和目录结构，避免重复下载。

## 反爬应对

- 使用Playwright模拟真实浏览器行为，加载JavaScript，避免因无JS导致数据缺失
- 保持登录状态，自动刷新或重新登录，防止会话过期
- 控制滚动频率，模拟人类操作节奏，避免触发反爬检测
- 设置合理请求间隔，防止被封禁

## 注意事项

- 登录流程复杂，需实现自动化登录并处理多因素认证（如有）
- 网站无公开API，所有数据依赖前端渲染，必须使用浏览器自动化
- 文件下载链接可能动态生成，需在详情页完整加载后提取
- 无限滚动可能导致内存占用高，需设计合理的滚动和数据存储策略

## 使用方法

```bash
# 运行Spider
scrapy crawl 身体活动分子传感器联盟_motrpac_molecular_transducers_of_physical_activity_consortium

# 限制采集数量（测试用）
scrapy crawl 身体活动分子传感器联盟_motrpac_molecular_transducers_of_physical_activity_consortium -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 身体活动分子传感器联盟_motrpac_molecular_transducers_of_physical_activity_consortium -o output.jsonl
```

## 输出格式

- JSONL格式: `output/身体活动分子传感器联盟_motrpac_molecular_transducers_of_physical_activity_consortium_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/身体活动分子传感器联盟_motrpac_molecular_transducers_of_physical_activity_consortium_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/身体活动分子传感器联盟_motrpac_molecular_transducers_of_physical_activity_consortium/
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

- **生成时间**: 2026-01-18 06:32:52
- **生成工具**: Spider Generator v1.0
