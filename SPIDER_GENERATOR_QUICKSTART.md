# 🚀 智能Spider生成器 - 快速开始

**为75个生物医学平台快速生成采集器代码的终极工具**

---

## 📋 概述

智能Spider生成器是一个革命性的工具，能够**自动分析网站结构、生成采集策略并创建生产就绪的Scrapy采集器代码**。它将原本需要数小时甚至数天的手工开发工作缩短到几分钟。

### ✨ 核心优势

- **🤖 AI驱动**: 利用GPT-4分析复杂网站结构并推荐最优策略
- **⚡ 极速生成**: 2-3分钟生成一个完整的Spider项目
- **📦 开箱即用**: 生成的代码集成了所有项目框架功能
- **🎯 深度定制**: 根据每个平台的特点生成专属采集逻辑
- **📊 批量处理**: 支持从Excel文件批量生成75个Spider

### 🎁 生成内容

每次运行生成：
- ✅ 完整的Spider Python代码
- ✅ 详细的README文档
- ✅ JSON配置文件
- ✅ 网站分析报告
- ✅ AI策略规划文档
- ✅ 网站截图

---

## 🛠️ 安装

### 前置条件

确保您已经安装了项目的基础环境。如果还没有，请运行：

```bash
cd /home/ubuntu/biomedical-data-scraper-platform

# 安装Python依赖
sudo pip3 install scrapy playwright jinja2 pandas openpyxl openai

# 安装Playwright浏览器
playwright install chromium
```

### 验证安装

```bash
# 测试CLI工具
python3 spider_generator/spider_generator_cli.py --help
```

如果看到帮助信息，说明安装成功！

---

## 🚀 使用方法

### 方式1: 生成单个Spider（推荐用于测试）

```bash
python3 spider_generator/spider_generator_cli.py \
  --url "https://biolincc.nhlbi.nih.gov/studies/" \
  --name "BioLINCC" \
  --output-dir "./generated_spiders"
```

**运行过程**：
1. ⏳ 分析网站结构（访问网站、识别元素）
2. 🤖 AI生成采集策略（调用GPT-4）
3. 📝 生成Spider代码
4. ✅ 完成！

**预计耗时**: 2-3分钟

### 方式2: 批量生成所有75个Spider

```bash
python3 spider_generator/spider_generator_cli.py \
  --batch-file "/home/ubuntu/upload/需求清单1222（第二批次）.xlsx" \
  --start-row 1 \
  --end-row 75
```

**这将**：
- 读取Excel文件中的所有75个平台
- 逐个分析并生成Spider
- 生成批量处理报告
- 保存所有生成的文件到 `./generated_spiders/`

**预计耗时**: 2.5-4小时（取决于网络和API响应速度）

### 方式3: 分批生成（推荐用于大规模任务）

为了避免一次性运行时间过长，可以分批处理：

```bash
# 第1批：前25个平台
python3 spider_generator/spider_generator_cli.py \
  --batch-file "/home/ubuntu/upload/需求清单1222（第二批次）.xlsx" \
  --start-row 1 \
  --end-row 25

# 第2批：26-50
python3 spider_generator/spider_generator_cli.py \
  --batch-file "/home/ubuntu/upload/需求清单1222（第二批次）.xlsx" \
  --start-row 26 \
  --end-row 50

# 第3批：51-75
python3 spider_generator/spider_generator_cli.py \
  --batch-file "/home/ubuntu/upload/需求清单1222（第二批次）.xlsx" \
  --start-row 51 \
  --end-row 75
```

---

## 📂 生成的文件结构

```
generated_spiders/
├── analysis/                          # 网站分析原始数据
│   ├── biolincc_analysis.json
│   ├── framingham_analysis.json
│   └── ...
├── strategies/                        # AI生成的策略
│   ├── biolincc_strategy.json
│   ├── framingham_strategy.json
│   └── ...
├── spiders/                           # 🎯 最终的Spider代码
│   ├── biolincc_spider.py            ← 可直接运行
│   ├── biolincc_config.json
│   ├── biolincc_README.md
│   ├── framingham_spider.py
│   ├── framingham_config.json
│   ├── framingham_README.md
│   └── ...
├── screenshots/                       # 网站截图
│   ├── biolincc_nhlbi_nih_gov.png
│   └── ...
└── BATCH_REPORT.md                    # 批量处理汇总报告
```

---

## 🎯 如何使用生成的Spider

### 步骤1: 复制Spider到项目

```bash
# 将生成的Spider复制到Scrapy项目的spiders目录
cp generated_spiders/spiders/biolincc_spider.py \
   /home/ubuntu/biomedical-data-scraper-platform/spiders/
```

### 步骤2: 运行Spider

```bash
cd /home/ubuntu/biomedical-data-scraper-platform

# 运行采集器
scrapy crawl biolincc

# 或者限制采集数量（测试用）
scrapy crawl biolincc -s CLOSESPIDER_ITEMCOUNT=10
```

### 步骤3: 查看输出

```bash
# 查看JSONL输出
cat output/biolincc_*.jsonl | jq .

# 查看CSV输出
head output/biolincc_*.csv
```

---

## 🔧 高级用法

### 指定目标数据类型

```bash
python3 spider_generator/spider_generator_cli.py \
  --url "https://example.com" \
  --name "Example" \
  --target-data "研究数据、PDF文件、补充材料、同行评审"
```

这会让AI更精确地理解您的需求，生成更有针对性的代码。

### 指定平台类型

```bash
python3 spider_generator/spider_generator_cli.py \
  --url "https://example.com" \
  --name "Example" \
  --type "data_repository"
```

支持的类型：
- `data_repository` - 数据仓库
- `journal` - 学术期刊
- `clinical_trial` - 临床试验
- `biobank` - 生物样本库
- `database` - 数据库

---

## 📊 理解生成的策略

每个Spider都会生成一个策略文件（`*_strategy.json`），包含：

```json
{
  "recommended_method": "scrapy",           // 推荐的采集方法
  "spider_template": "basic_spider",        // 使用的模板
  "difficulty": 3,                          // 难度（1-5星）
  "estimated_dev_time": "4-6小时",          // 预估开发时间
  "data_extraction": {                      // 数据提取策略
    "list_page_selector": "table tbody tr",
    "detail_link_selector": "a::attr(href)",
    "fields": {
      "title": "h1::text",
      "abstract": "div.abstract::text"
    }
  },
  "pagination_strategy": "...",             // 分页策略
  "file_download_strategy": "...",          // 文件下载策略
  "anti_scraping_handling": [...],          // 反爬应对
  "special_considerations": [...]           // 特殊注意事项
}
```

---

## 🐛 常见问题

### Q: 生成的Spider可以直接用吗？

**A**: 可以，但建议先进行小规模测试。AI生成的选择器可能需要根据实际情况微调。

### Q: 如果网站需要登录怎么办？

**A**: 工具会检测登录需求。对于需要登录的网站，您需要手动添加登录逻辑，或使用Playwright模板。

### Q: 生成失败了怎么办？

**A**: 查看错误信息。常见原因：
- 网络问题（无法访问目标网站）
- OpenAI API配额不足
- 网站结构过于复杂

可以尝试重新运行，或手动调整生成的代码。

### Q: 如何提高生成质量？

**A**: 
1. 使用 `--target-data` 参数明确说明您要采集什么
2. 使用 `--type` 参数指定平台类型
3. 生成后人工审查并优化选择器

---

## 📈 批量处理最佳实践

### 1. 分批运行

不要一次性运行75个，建议分3-4批：
- 更容易追踪进度
- 出错时不会丢失所有进度
- 可以及时发现问题并调整

### 2. 监控日志

```bash
# 将日志保存到文件
python3 spider_generator/spider_generator_cli.py \
  --batch-file "需求清单.xlsx" \
  --start-row 1 \
  --end-row 25 \
  2>&1 | tee generation_log_batch1.txt
```

### 3. 查看批量报告

批量运行完成后，查看 `BATCH_REPORT.md`：

```bash
cat generated_spiders/BATCH_REPORT.md
```

这会显示每个平台的生成状态、难度、推荐方法等。

---

## 🎓 进阶：自定义模板

如果您想添加自己的Spider模板：

### 1. 创建模板文件

```bash
# 在templates目录创建新模板
nano spider_generator/templates/my_custom_spider.py.j2
```

### 2. 使用Jinja2语法

参考 `basic_spider.py.j2` 和 `api_spider.py.j2` 的写法。

### 3. 在策略规划中引用

修改 `ai_strategy_planner.py`，让AI在适当情况下推荐您的模板。

---

## 📞 技术支持

- **文档**: 查看 `docs/spider_generator_user_guide.md` 获取完整文档
- **架构**: 查看 `docs/spider_generator_architecture.md` 了解系统设计
- **问题**: 在GitHub项目中提Issue

---

## 🎉 开始使用

现在您已经掌握了所有必要的知识！选择一个方式开始生成您的Spider吧：

```bash
# 🚀 快速测试（单个平台）
python3 spider_generator/spider_generator_cli.py \
  --url "https://biolincc.nhlbi.nih.gov/studies/" \
  --name "BioLINCC"

# 🔥 批量生成（所有75个平台）
python3 spider_generator/spider_generator_cli.py \
  --batch-file "/home/ubuntu/upload/需求清单1222（第二批次）.xlsx" \
  --start-row 1 \
  --end-row 75
```

**祝您采集顺利！** 🎊
