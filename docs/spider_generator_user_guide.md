# 智能Spider生成器用户指南

**版本**: 1.0
**作者**: Manus AI
**最后更新**: {{datetime.now().strftime("%Y-%m-%d")}} 

---

## 1. 简介

智能Spider生成器（Spider Generator）是一个强大的命令行工具，旨在彻底改变生物医学数据采集的工作流程。它通过自动化分析目标网站、生成采集策略和创建生产就绪的Scrapy采集器代码，极大地提高了开发效率和数据采集的深度。

### 1.1 核心目标

- **自动化**: 最大限度地减少手动分析和编码工作。
- **标准化**: 确保所有生成的采集器都遵循统一的项目架构和最佳实践。
- **智能化**: 利用AI（GPT-4）分析复杂的网站结构，并推荐最优的采集策略。
- **高质量**: 生成可读性强、易于维护且功能完备的采集器代码。

### 1.2 主要功能

- **一键式生成**: 只需提供一个URL和平台名称，即可获得完整的Spider项目。
- **多模式支持**: 支持命令行批量处理和交互式问答两种模式。
- **全面的网站分析**: 自动识别网站类型、分页机制、登录需求、API接口和反爬措施。
- **AI策略规划**: 基于分析结果，由AI规划出最佳采集路径和方法。
- **多模板系统**: 内置多种Spider模板，适应不同类型的网站（静态、动态、API驱动等）。
- **自动化文档**: 为每个生成的Spider创建独立的README和配置文件。

## 2. 安装与环境配置

该工具作为`biomedical-data-scraper-platform`项目的一部分，无需单独安装。只需确保项目环境已正确配置。

### 2.1 环境要求

- Python 3.11+
- Scrapy 2.11+
- Playwright
- OpenAI Python Library
- Pandas & openpyxl (用于批量处理)

### 2.2 依赖安装

如果您尚未安装所有依赖，请在项目根目录运行：

```bash
sudo pip3 install -r requirements.txt
sudo pip3 install playwright jinja2 pandas openpyxl
sudo playwright install chromium
```

### 2.3 OpenAI API密钥配置

工具需要访问OpenAI API来执行AI策略规划。请确保您已在环境变量中设置了API密钥：

```bash
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## 3. 使用方法

工具的主入口是 `spider_generator/spider_generator_cli.py`。

### 3.1 命令行模式 (CLI)

命令行模式最适合自动化和批量处理任务。

#### 3.1.1 生成单个Spider

这是最基础的用法。提供平台URL和名称即可。

```bash
python3 spider_generator/spider_generator_cli.py --url "https://www.example.com" --name "ExamplePlatform"
```

**参数说明**:

| 参数 | 缩写 | 描述 | 是否必须 |
| :--- | :--- | :--- | :--- |
| `--url` | | 目标平台的完整URL | 是 |
| `--name` | | 平台的名称，用于生成文件名和类名 | 是 |
| `--type` | | 平台类型 (如 `data_repository`, `journal`)，不提供则自动检测 | 否 |
| `--target-data` | | 描述您希望采集的具体数据，帮助AI生成更精确的策略 | 否 |
| `--output-dir` | | 生成文件的输出目录，默认为 `./generated_spiders` | 否 |
| `--test` | | 生成后自动运行基础测试（功能待实现） | 否 |

#### 3.1.2 批量生成Spider

工具可以读取一个Excel文件，并为其中的每一行记录批量生成Spider。

```bash
python3 spider_generator/spider_generator_cli.py --batch-file "需求清单.xlsx" --start-row 1 --end-row 10
```

**Excel文件格式要求**:

Excel文件必须包含至少两列：
- `平台名称` (或 `name`)
- `网址` (或 `url`)

**批量处理参数**:

| 参数 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `--batch-file` | 包含平台列表的Excel文件路径 | 无 |
| `--start-row` | 从Excel的第几行开始处理（1-based） | 1 |
| `--end-row` | 处理到Excel的第几行结束（包含该行） | 文件末尾 |

### 3.2 交互式模式

如果您不确定所有参数，或者希望通过引导式流程生成Spider，可以使用交互式模式。

```bash
python3 spider_generator/spider_generator_cli.py --interactive
```

启动后，工具会通过一系列问题来收集必要信息，然后开始生成过程。

```
> 请输入目标网站URL: https://biolincc.nhlbi.nih.gov
> 正在分析网站...
> 检测到网站类型: 数据仓库
> 是否需要登录? (y/n): n
> 目标数据类型: (1)研究数据 (2)文献数据 (3)临床试验: 1
> 正在生成Spider...
> ✓ Spider生成成功: biolincc_spider.py
> 是否运行测试? (y/n): y
> 正在测试...
> ✓ 测试通过！采集了3条样本数据
```

## 4. 生成的文件结构

每次成功运行后，工具会在指定的输出目录（默认为`./generated_spiders`）下创建一套完整的文件。

```
generated_spiders/
├── analysis/                     # 网站分析原始报告
│   └── biolincc_analysis.json
├── strategies/                   # AI生成的采集策略
│   └── biolincc_strategy.json
├── spiders/                      # 最终生成的采集器代码和文档
│   ├── biolincc_spider.py
│   ├── biolincc_spider_config.json
│   └── biolincc_spider_README.md
├── screenshots/                  # 网站分析时保存的截图
│   └── biolincc_nhlbi_nih_gov.png
└── BATCH_REPORT.md               # (批量模式下) 汇总报告
```

### 4.1 文件详解

- **`_spider.py`**: **核心采集器代码**。这是一个可以直接被Scrapy调用的Python文件。
- **`_config.json`**: 该Spider的配置文件，包含了平台信息、采集策略摘要和特定设置。
- **`_README.md`**: **使用和维护文档**。详细说明了该Spider的采集策略、数据结构、使用方法和注意事项。
- **`_analysis.json`**: `WebsiteAnalyzer`模块输出的原始JSON报告，包含了对网站结构的详细分析。
- **`_strategy.json`**: `AIStrategyPlanner`模块输出的JSON文件，包含了AI对如何采集该网站的完整建议。
- **`.png`**: 网站首页的完整截图，用于辅助人工分析。

## 5. 理解生成的Spider代码

生成的Spider代码遵循了项目预定义的框架和最佳实践。

### 5.1 主要组成部分

- **`__init__`**: 初始化Spider，设置统计信息。
- **`start_requests`**: 生成初始请求，通常是访问列表页的第一页。
- **`parse_list`**: 解析列表页，提取详情页链接，并处理分页。
- **`parse_detail`**: 解析详情页，提取所有目标元数据和文件链接。
- **`_extract_field`**: 一个辅助方法，用于安全地提取单个数据字段。
- **`handle_error`**: 统一的错误处理回调。
- **`closed`**: Spider关闭时调用，用于打印采集统计报告。

### 5.2 如何运行

将生成的 `spiders/` 目录下的所有文件复制到 Scrapy 项目的 `spiders/` 目录下，然后运行：

```bash
# 切换到Scrapy项目根目录
cd /path/to/your/biomedical-data-scraper-platform

# 运行采集器
scrapy crawl <spider_name>

# 例如:
scrapy crawl biolincc_spider
```

## 6. 扩展与定制

该工具被设计为可扩展的。您可以轻松添加新的模板或修改现有逻辑。

### 6.1 添加新的Spider模板

1. 在 `spider_generator/templates/` 目录下创建一个新的 `.py.j2` 文件（例如 `my_template.py.j2`）。
2. 使用Jinja2语法编写您的模板。您可以参考 `basic_spider.py.j2` 和 `api_spider.py.j2`。
3. 在 `AIStrategyPlanner` 中，让AI在适当的情况下推荐您的新模板名称（例如 `my_template`）。

### 6.2 修改AI提示词

您可以编辑 `spider_generator/analyzers/ai_strategy_planner.py` 中的 `_get_system_prompt` 和 `_build_prompt` 方法，以调整您与AI的交互方式，从而获得更符合您需求的策略。

### 6.3 调整网站分析逻辑

如果您发现 `WebsiteAnalyzer` 对某些网站的分析不准确，您可以直接修改 `spider_generator/analyzers/website_analyzer.py` 中的相应方法（例如 `_analyze_pagination`）来改进其识别能力。

## 7. 常见问题 (FAQ)

**Q: 生成的Spider可以直接在生产环境中使用吗？**

A: 生成的Spider是“生产就绪”的，但我们强烈建议在投入生产前进行人工审查和完整测试。AI生成的选择器可能不是最优的，或者某些特殊情况需要手动处理。

**Q: 如果一个网站需要登录怎么办？**

A: `WebsiteAnalyzer` 会尝试检测登录需求。AI策略规划器会据此推荐使用基于Playwright的模板（功能待实现）。在当前版本中，您可能需要手动修改生成的代码以处理登录逻辑。

**Q: 工具生成代码需要多长时间？**

A: 单个Spider的生成过程通常需要1-2分钟，主要时间消耗在网站分析（访问网站、等待动态内容加载）和AI策略规划（调用GPT-4 API）上。

**Q: 批量生成时，如果中途失败了怎么办？**

A: 批量生成模式会将每个成功或失败的结果实时记录在 `generated_spiders/batch_results.json` 文件中。您可以随时根据此文件恢复进度，或在完成后查看失败原因。

---

**技术支持**: 如果您在使用中遇到任何问题，请在项目中提出Issue。
