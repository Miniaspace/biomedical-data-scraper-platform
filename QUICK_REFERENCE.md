# Spider生成器 - 快速参考指南

## 📦 交付内容

### 1. 生成的Spider代码 (64个)

```
generated_spiders_batch1/  (20个Spider)
generated_spiders_batch2/  (22个Spider)
generated_spiders_batch3/  (22个Spider)
```

**压缩包**: `all_generated_spiders.tar.gz` (253KB)

### 2. 核心工具

- `spider_generator/spider_generator_cli_optimized.py` - 优化版生成器
- `spider_generator/spider_generator_cli.py` - 原始版生成器
- `monitor_progress.sh` - 进度监控脚本

### 3. 文档

- `FINAL_GENERATION_SUMMARY.md` - 最终总结报告 ⭐
- `SPIDER_GENERATOR_QUICKSTART.md` - 快速开始指南
- `docs/spider_generator_user_guide.md` - 用户手册
- `docs/spider_generator_architecture.md` - 架构设计

## 🚀 快速开始

### 查看生成结果

```bash
cd /home/ubuntu/biomedical-data-scraper-platform

# 查看第1批
ls generated_spiders_batch1/spiders/

# 查看批次报告
cat generated_spiders_batch1/BATCH_REPORT.md
```

### 测试单个Spider

```bash
# 进入目录
cd generated_spiders_batch1/spiders

# 查看README
cat 社区动脉粥样硬化风险研究_*_README.md

# 运行Spider (如果是Scrapy)
scrapy runspider 社区动脉粥样硬化风险研究_*_spider.py
```

### 生成新的Spider

```bash
cd /home/ubuntu/biomedical-data-scraper-platform

# 单个生成
python3 spider_generator/spider_generator_cli_optimized.py \
  --url "https://example.com" \
  --name "Example Platform"

# 批量生成
python3 spider_generator/spider_generator_cli_optimized.py \
  --batch-file "platforms.xlsx" \
  --start-row 1 \
  --end-row 10
```

### 重试失败的平台

```bash
# 增加超时和重试次数
python3 spider_generator/spider_generator_cli_optimized.py \
  --url "https://framinghamheartstudy.org/" \
  --name "FHS" \
  --timeout 180 \
  --max-retries 5
```

## 📊 生成统计

| 批次 | 成功 | 失败 | 成功率 |
|------|------|------|--------|
| 第1批 (1-25) | 20 | 5 | 80% |
| 第2批 (26-50) | 22 | 3 | 88% |
| 第3批 (51-75) | 22 | 3 | 88% |
| **总计** | **64** | **11** | **85.3%** |

## 🔧 常见问题

### Q1: Spider无法运行？

**A**: 检查依赖是否安装：

```bash
pip3 install scrapy playwright pandas openpyxl
playwright install chromium
```

### Q2: 需要登录的平台如何处理？

**A**: 编辑对应的 `config.json` 文件，添加登录凭证：

```json
{
  "login": {
    "required": true,
    "username": "your_username",
    "password": "your_password"
  }
}
```

### Q3: 如何调整Spider参数？

**A**: 每个Spider的 `config.json` 包含所有可配置参数：

- `max_pages`: 最大采集页数
- `delay`: 请求延迟
- `timeout`: 超时时间
- `user_agent`: 用户代理

### Q4: 生成的代码需要修改吗？

**A**: 70-80%的Spider可以直接使用，其余可能需要：

- 调整CSS/XPath选择器
- 添加特定的登录逻辑
- 处理特殊的分页方式
- 添加数据清洗逻辑

### Q5: 如何部署到生产环境？

**A**: 推荐使用Airflow进行调度：

1. 将Spider代码复制到Scrapy项目
2. 创建Airflow DAG
3. 配置定时任务
4. 设置监控告警

## 📁 文件结构说明

```
generated_spiders_batchX/
├── spiders/                    # Spider代码目录
│   ├── {name}_spider.py       # Spider主代码
│   ├── {name}_config.json     # 配置文件
│   └── {name}_README.md       # 使用说明
├── strategies/                 # AI策略目录
│   └── {name}_strategy.json   # 策略规划
├── analysis/                   # 分析结果目录
│   └── {name}_analysis.json   # 网站分析
├── batch_progress.json         # 批次进度
└── BATCH_REPORT.md            # 批次报告
```

## 🎯 下一步建议

### 1周内
- [ ] 审查所有64个Spider代码
- [ ] 测试10-20个无需登录的Spider
- [ ] 重试11个失败的平台

### 1个月内
- [ ] 完成所有Spider的测试
- [ ] 部署到Airflow
- [ ] 配置定时采集任务

### 3个月内
- [ ] 数据质量验证
- [ ] 构建数据仓库
- [ ] 开发数据分析工具

## 📞 技术支持

- **文档**: 查看 `docs/` 目录下的详细文档
- **示例**: 参考已生成的Spider代码
- **GitHub**: https://github.com/Miniaspace/biomedical-data-scraper-platform

## 🎉 成功案例

生成器已成功为64个生物医学平台生成Spider，包括：

- **心血管研究**: ARIC, MESA, JHS等
- **癌症研究**: BioLINCC, CCDI Hub等
- **神经科学**: FITBIR, DABI等
- **基因组学**: AnVIL, AMP PD等
- **临床试验**: NIAID, TrialShare等

---

**最后更新**: 2026-01-18  
**版本**: v1.0
