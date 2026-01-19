# 额颞叶变性（FTLD）类型综合性研究ALLFTD Spider

## 基本信息

- **平台名称**: 额颞叶变性（FTLD）类型综合性研究ALLFTD
- **平台URL**: https://www.allftd.org/data
- **Spider名称**: 额颞叶变性ftld类型综合性研究allftd
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

由于采用无限滚动(infinite_scroll)，使用Playwright模拟页面滚动操作，触发动态加载更多数据，直到页面不再加载新内容或达到预设最大条数。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `ul > li > div.title, ul > li > div > h3` |
| pdf_link | `ul > li a[href$='.pdf']` |


## 文件下载

通过Playwright捕获PDF文件链接，使用异步HTTP请求下载PDF文件，确保文件完整性，支持断点续传。若PDF链接为动态生成，需在页面加载后提取。

## 反爬应对

- 针对验证码，采用人工识别或集成第三方验证码识别服务，必要时设置采集频率，避免触发验证码。
- 模拟真实用户行为，如合理滚动速度、随机停顿，避免快速连续请求。
- 使用代理IP池分散请求，降低被封风险。

## 注意事项

- 网站不需要登录，但存在验证码，需提前设计验证码处理流程。
- 页面JavaScript渲染较少，但无限滚动需完整执行JS，确保数据加载。
- 无API接口，所有数据需从页面DOM中提取，字段较少，需根据实际页面结构调整选择器。

## 使用方法

```bash
# 运行Spider
scrapy crawl 额颞叶变性ftld类型综合性研究allftd

# 限制采集数量（测试用）
scrapy crawl 额颞叶变性ftld类型综合性研究allftd -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 额颞叶变性ftld类型综合性研究allftd -o output.jsonl
```

## 输出格式

- JSONL格式: `output/额颞叶变性ftld类型综合性研究allftd_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/额颞叶变性ftld类型综合性研究allftd_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/额颞叶变性ftld类型综合性研究allftd/
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

- **生成时间**: 2026-01-18 06:34:16
- **生成工具**: Spider Generator v1.0
