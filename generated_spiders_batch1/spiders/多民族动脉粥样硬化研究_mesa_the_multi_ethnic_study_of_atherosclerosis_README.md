# 多民族动脉粥样硬化研究 MESA (The Multi-Ethnic Study of Atherosclerosis) Spider

## 基本信息

- **平台名称**: 多民族动脉粥样硬化研究 MESA (The Multi-Ethnic Study of Atherosclerosis)
- **平台URL**: https://www.mesa-nhlbi.org/
- **Spider名称**: 多民族动脉粥样硬化研究_mesa_the_multi_ethnic_study_of_atherosclerosis
- **采集方法**: playwright
- **难度评级**: ⭐⭐⭐
- **预估开发时间**: 16

## 采集策略

网站无分页，直接采集首页所有列表项。若后续发现分页或动态加载，则需模拟点击加载更多或翻页。

## 数据字段

| 字段名 | 选择器 |
|--------|--------|
| author | `ul li .author, ul li span.author` |


## 文件下载

登录后访问详情页或列表页中PDF及补充材料链接，使用Playwright模拟浏览器环境下载文件。确保携带登录cookie和header。对文件链接进行正则匹配，自动识别并下载。

## 反爬应对

- 使用Playwright模拟真实浏览器，避免因无JavaScript环境导致数据缺失
- 保持登录状态，定期刷新cookie，避免登录失效
- 控制请求频率，避免触发服务器异常

## 注意事项

- 登录流程需要模拟表单提交，可能涉及CSRF token，需动态获取
- 网站基于Drupal 11，页面结构可能动态变化，需定期维护选择器
- 无API接口，所有数据需通过页面解析获取

## 使用方法

```bash
# 运行Spider
scrapy crawl 多民族动脉粥样硬化研究_mesa_the_multi_ethnic_study_of_atherosclerosis

# 限制采集数量（测试用）
scrapy crawl 多民族动脉粥样硬化研究_mesa_the_multi_ethnic_study_of_atherosclerosis -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl 多民族动脉粥样硬化研究_mesa_the_multi_ethnic_study_of_atherosclerosis -o output.jsonl
```

## 输出格式

- JSONL格式: `output/多民族动脉粥样硬化研究_mesa_the_multi_ethnic_study_of_atherosclerosis_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/多民族动脉粥样硬化研究_mesa_the_multi_ethnic_study_of_atherosclerosis_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/多民族动脉粥样硬化研究_mesa_the_multi_ethnic_study_of_atherosclerosis/
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

- **生成时间**: 2026-01-18 06:11:42
- **生成工具**: Spider Generator v1.0
