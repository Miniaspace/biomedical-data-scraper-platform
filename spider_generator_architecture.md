# 智能Spider生成器架构设计

## 1. 系统概述

智能Spider生成器是一个自动化工具，能够分析目标网站的结构，并生成符合项目框架标准的、可直接使用的Scrapy采集器代码。

### 1.1 核心功能

1. **网站结构自动分析**：访问目标网站，识别数据结构、导航模式、文件类型
2. **智能代码生成**：基于分析结果生成定制化的Spider代码
3. **AI辅助优化**：利用GPT-4理解网站特征，生成最优采集策略
4. **模板系统**：维护多种Spider模板，适配不同类型的网站
5. **验证测试**：生成后自动进行基础验证

### 1.2 设计原则

- **自动化优先**：最小化人工干预
- **质量保证**：生成的代码必须符合项目标准
- **可扩展性**：易于添加新的网站类型模板
- **智能适配**：根据网站特征自动选择最佳策略

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Spider Generator CLI                      │
│                    (用户交互界面)                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Website Analyzer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Page Fetcher │  │ Structure    │  │ Content      │      │
│  │ (Playwright) │→ │ Analyzer     │→ │ Classifier   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  AI Strategy Planner                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ GPT-4 API    │  │ Template     │  │ Strategy     │      │
│  │ Integration  │→ │ Selector     │→ │ Generator    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Code Generator                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Template     │  │ Code         │  │ Config       │      │
│  │ Engine       │→ │ Assembler    │→ │ Generator    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Validator & Tester                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Syntax       │  │ Dry Run      │  │ Report       │      │
│  │ Checker      │→ │ Tester       │→ │ Generator    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                  生成的Spider文件
                  + 配置文件
                  + 测试报告
```

## 3. 核心组件详细设计

### 3.1 Website Analyzer（网站分析器）

**功能**：自动访问并分析目标网站的结构

**子组件**：

1. **Page Fetcher**
   - 使用Playwright访问网站
   - 处理JavaScript渲染
   - 截图保存用于AI分析
   - 提取HTML结构

2. **Structure Analyzer**
   - 识别列表页/详情页结构
   - 检测分页机制（翻页、滚动加载等）
   - 识别搜索/筛选功能
   - 检测登录要求

3. **Content Classifier**
   - 识别数据字段类型（标题、作者、日期等）
   - 检测文件下载链接（PDF、附件等）
   - 识别API调用（XHR请求）
   - 分类网站类型（数据仓库、期刊、数据库等）

**输出**：网站分析报告（JSON格式）

```json
{
  "site_type": "data_repository",
  "has_login": false,
  "pagination_type": "next_button",
  "data_structure": {
    "list_page": "https://example.com/studies",
    "detail_page_pattern": "https://example.com/study/{id}",
    "fields": ["title", "authors", "date", "abstract"],
    "files": ["pdf", "supplementary"]
  },
  "api_detected": true,
  "api_endpoints": [
    {"url": "/api/studies", "method": "GET"}
  ]
}
```

### 3.2 AI Strategy Planner（AI策略规划器）

**功能**：利用GPT-4分析网站特征，生成最优采集策略

**工作流程**：

1. 接收Website Analyzer的分析报告
2. 将网站截图、HTML结构、分析报告发送给GPT-4
3. GPT-4返回推荐的采集策略：
   - 使用Scrapy还是Playwright
   - 是否需要API采集
   - 数据提取的CSS/XPath选择器
   - 文件下载策略
   - 深度采集路径

4. 选择最合适的Spider模板
5. 生成详细的采集策略文档

**提示词模板**：

```
你是一个专业的网页采集专家。请分析以下网站并提供采集策略：

网站信息：
- URL: {url}
- 网站类型: {site_type}
- 目标数据: {target_data}

网站结构分析：
{analysis_report}

请提供：
1. 推荐的采集方法（Scrapy/Playwright/API）
2. 数据提取选择器（CSS/XPath）
3. 分页处理策略
4. 文件下载策略
5. 需要注意的反爬机制
6. 估计的采集难度（1-5星）

以JSON格式返回。
```

### 3.3 Code Generator（代码生成器）

**功能**：基于策略和模板生成完整的Spider代码

**模板类型**：

1. **basic_spider.py.j2** - 基础静态网站
2. **api_spider.py.j2** - API采集
3. **playwright_spider.py.j2** - 需要浏览器渲染
4. **login_spider.py.j2** - 需要登录
5. **hybrid_spider.py.j2** - 混合策略（API + 网页）

**生成内容**：

1. Spider主文件（`{platform_name}_spider.py`）
2. Items定义（如需要）
3. 配置文件（`{platform_name}_config.yaml`）
4. README文档（使用说明）

**代码质量保证**：

- 自动添加注释
- 遵循PEP 8规范
- 包含错误处理
- 集成项目框架（EnhancedFilesPipeline等）

### 3.4 Validator & Tester（验证测试器）

**功能**：验证生成的代码并进行测试

**验证步骤**：

1. **语法检查**：使用pylint/flake8
2. **导入测试**：确保所有依赖可用
3. **Dry Run**：运行Spider采集1-3条数据
4. **输出验证**：检查JSONL/CSV格式是否正确
5. **文件检查**：验证文件下载是否正常

**测试报告**：

```
Spider测试报告
==============
Spider名称: biolincc_spider
生成时间: 2026-01-17 10:30:00

✓ 语法检查通过
✓ 依赖导入正常
✓ 成功采集 3 条测试数据
✓ JSONL输出格式正确
✓ 文件下载功能正常

警告:
- 检测到可能的反爬限制，建议添加延迟

建议:
- 考虑添加更多错误处理
- 可以优化选择器性能
```

## 4. 使用流程

### 4.1 命令行界面

```bash
# 基础用法
python spider_generator.py --url "https://example.com" --name "example_spider"

# 高级用法
python spider_generator.py \
  --url "https://example.com" \
  --name "example_spider" \
  --type "data_repository" \
  --target-data "studies,pdfs,metadata" \
  --test \
  --output-dir "./spiders"

# 批量生成（从Excel文件）
python spider_generator.py --batch-file "需求清单.xlsx" --start-row 1 --end-row 10
```

### 4.2 交互式模式

```bash
python spider_generator.py --interactive

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

## 5. 技术栈

- **Python 3.11+**
- **Scrapy 2.11+** - 核心采集框架
- **Playwright** - 浏览器自动化
- **OpenAI API (GPT-4)** - AI分析
- **Jinja2** - 模板引擎
- **BeautifulSoup4** - HTML解析
- **PyYAML** - 配置文件
- **Click** - CLI框架

## 6. 扩展性设计

### 6.1 添加新模板

在 `templates/` 目录下创建新的Jinja2模板：

```python
# templates/new_template.py.j2
import scrapy

class {{ spider_class_name }}(scrapy.Spider):
    name = "{{ spider_name }}"
    
    # 模板特定的代码...
```

### 6.2 自定义分析器

可以添加新的分析器插件：

```python
# analyzers/custom_analyzer.py
class CustomAnalyzer:
    def analyze(self, html, url):
        # 自定义分析逻辑
        return analysis_result
```

### 6.3 集成新的AI模型

支持切换不同的AI模型：

```python
# 配置文件
AI_CONFIG = {
    "provider": "openai",  # 或 "anthropic", "local"
    "model": "gpt-4",
    "temperature": 0.3
}
```

## 7. 安全与隐私

- API密钥通过环境变量管理
- 不记录敏感信息（登录凭证等）
- 生成的代码不包含硬编码的密钥
- 遵守robots.txt和网站使用条款

## 8. 性能优化

- 缓存网站分析结果（避免重复访问）
- 并行生成多个Spider
- 增量更新（只重新生成修改的部分）
- 模板预编译

## 9. 未来改进方向

1. **Web UI**：提供图形化界面
2. **Spider市场**：共享和下载社区贡献的Spider
3. **自动维护**：检测网站结构变化，自动更新Spider
4. **性能监控**：集成采集性能分析
5. **多语言支持**：生成其他语言的采集器（Node.js等）
