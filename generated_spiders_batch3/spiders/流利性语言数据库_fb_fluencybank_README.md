# 流利性语言数据库 FB (FluencyBank) Spider

## 基本信息

- **平台名称**: 流利性语言数据库 FB (FluencyBank)
- **平台URL**: https://fluency.talkbank.org
- **Spider名称**: 流利性语言数据库_fb_fluencybank
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 24

## 采集策略

网站无分页，所有内容集中展示或通过筛选条件加载，需登录后确认是否存在动态加载或筛选分页，若有则通过Playwright模拟点击加载更多或筛选操作

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| title | `CSS选择器 h1.article-title 或 XPath //h1[contains(@class,'article-title')]` |
| author | `CSS选择器 div.authors 或 XPath //div[contains(@class,'authors')]` |
| publication_date | `CSS选择器 span.pub-date 或 XPath //span[contains(@class,'pub-date')]` |
| abstract | `CSS选择器 div.abstract 或 XPath //div[contains(@class,'abstract')]` |
| pdf_link | `CSS选择器 a[href$='.pdf'] 或 XPath //a[contains(@href,'.pdf')]` |
| docx_link | `CSS选择器 a[href$='.docx'] 或 XPath //a[contains(@href,'.docx')]` |
| supplementary_materials | `CSS选择器 div.supplementary a 或 XPath //div[contains(@class,'supplementary')]//a` |


## 文件下载

通过Playwright登录后，抓取文件链接（pdf/docx），使用Playwright的页面请求拦截或直接通过Python requests携带登录cookie进行文件下载，确保文件完整性和正确命名

## 反爬应对

- 使用Playwright模拟真实浏览器行为，避免因无JavaScript执行导致页面加载不全
- 合理设置请求间隔，避免触发服务器异常
- 登录状态保持，避免频繁登录导致账号异常

## 注意事项

- 登录流程依赖外部authUI模块，需调试登录流程，确保cookie/session正确获取
- 无API接口，所有数据需通过页面渲染抓取，需确认页面结构稳定性
- 文件下载链接可能为动态生成，需在登录状态下抓取

## 使用方法

```bash
# 运行Spider
scrapy crawl 流利性语言数据库_fb_fluencybank

# 限制采集数量（测试用）
scrapy crawl 流利性语言数据库_fb_fluencybank -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 流利性语言数据库_fb_fluencybank -o output.jsonl
```

## 输出格式

- JSONL格式: `output/流利性语言数据库_fb_fluencybank_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/流利性语言数据库_fb_fluencybank_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/流利性语言数据库_fb_fluencybank/
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

- **生成时间**: 2026-01-18 06:36:51
- **生成工具**: Spider Generator v1.0
