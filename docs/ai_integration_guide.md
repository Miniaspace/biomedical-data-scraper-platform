# AI辅助数据采集集成指南

**版本**: 3.0
**日期**: 2026年1月16日

## 1. 概述：为什么需要AI？

传统爬虫依赖固定的CSS选择器，当网站结构复杂或频繁变化时，维护成本极高。AI，特别是大型语言模型（LLM），为我们提供了全新的解决方案。

**AI解决了三大核心痛点：**
1.  **复杂结构解析**：AI能像人一样理解页面布局，轻松处理嵌套、非结构化的数据。
2.  **自适应变化**：AI理解语义而非代码结构，网站的小幅改版不会导致采集器失效。
3.  **开发效率提升**：用自然语言描述所需数据，替代繁琐的选择器编写和调试。

## 2. 我们的方案：双模式混合AI架构

为了兼顾**成本、效果和数据隐私**，我们设计了一套灵活的**双模式混合AI架构**。

| 对比维度 | **本地AI模式 (Local)** | **商用API模式 (Commercial)** |
| :--- | :--- | :--- |
| **核心技术** | Ollama + Llama 3/Mistral | OpenAI/Anthropic/Google API |
| **优势** | **零成本**、**数据私密**、无限调用 | **效果最好**、无需硬件、稳定可靠 |
| **劣势** | 需要GPU、效果略逊于顶级模型 | 按调用付费、数据需外传 |
| **适用场景** | 大规模采集、敏感数据、常规页面 | 高价值数据、复杂推理、质量要求极高 |
| **成本估算** | 硬件成本(一次性) + 电费 | GPT-4o-mini: 约$0.6/百万输出Token |

### 混合策略 (Hybrid)

这是我们**默认并推荐**的模式。它结合了前两者的优点：
- **优先使用本地AI**：处理绝大部分任务，实现成本最低化。
- **智能Fallback**：当本地AI提取失败或结果质量低于预设阈值（如7/10分）时，**自动切换到商用API**进行重试，确保关键数据的采集成功率和质量。

## 3. 如何使用AI辅助功能

### 步骤1：安装本地AI环境 (Ollama)

如果您想使用本地AI模式，只需在您的机器上（需要GPU以获得良好性能）执行一行命令：

```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 下载并运行一个模型 (推荐Llama 3.1 8B)
ollama run llama3.1:8b
```

Ollama会自动在 `http://localhost:11434` 启动一个与OpenAI兼容的API服务。我们的框架已配置好直接使用它。

### 步骤2：配置采集器

在您的Spider中，通过`custom_settings`启用并配置AI模式：

```python
class MyAISpider(BaseSpider):
    custom_settings = {
        **BaseSpider.custom_settings,
        'AI_ENABLED': True,          # 启用AI
        'AI_MODE': 'hybrid',         # 模式: 'local', 'commercial', 'hybrid'
        'AI_LOCAL_MODEL': 'llama3.1:8b', # 本地模型
        'AI_COMMERCIAL_MODEL': 'gpt-4o-mini', # 商用模型
        'AI_QUALITY_THRESHOLD': 7.0, # 质量阈值
    }
```

### 步骤3：在Spider中调用AI

我们为您封装了`HybridLLMExtractor`，它会自动处理所有模式切换和重试逻辑。

请参考我们为您编写的全新示例：`spiders/ai_enhanced_spider.py`。

**核心代码示例：**

```python
# spiders/ai_enhanced_spider.py

from common.ai.llm_extractor import HybridLLMExtractor
from pydantic import BaseModel, Field

# 1. 定义你想要的数据结构
class Publication(BaseModel):
    title: str = Field(description="论文标题")
    authors: List[str] = Field(description="作者列表")
    doi: Optional[str] = Field(default=None, description="DOI")

class AIEnhancedSpider(BaseSpider):
    # ... (省略配置)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化AI提取器
        self.ai_extractor = HybridLLMExtractor(...)

    def parse_detail_page(self, response):
        # 2. 提取页面文本
        page_text = ' '.join(response.css('main ::text').getall())
        page_text = page_text[:10000] # 限制长度以节省成本
        
        # 3. 调用AI提取
        publication = self.ai_extractor.extract(
            text=page_text,
            schema=Publication,
            instruction="请特别注意提取所有作者的完整姓名"
        )
        
        if publication:
            yield publication.model_dump()
```

## 4. 最佳实践与优化策略

我们发现，**Crawl4AI** 和 **Scrapy-LLM** 这两个开源项目提供了很多优秀的设计思想。结合它们的优点和我们的实践，我们推荐以下最佳策略：

1.  **分层提取策略 (成本最优)**
    - **L1 - 简单页面**: 坚持使用**传统CSS选择器**。这是最快、最稳定、成本为零的方案。
    - **L2 - 动态页面**: 使用**Playwright**渲染页面后，再尝试L1或L3。
    - **L3 - 复杂页面**: 使用**AI辅助提取**。这是应对复杂结构和变化的终极武器。

2.  **优先使用`scrapy-llm`集成**
    我们发现`scrapy-llm`项目提供了一个非常优雅的Scrapy中间件集成方案。我们已将其设计思想融入`LLMExtractor`中，未来可以进一步将其封装为中间件，实现更无缝的集成。

3.  **借鉴Crawl4AI的Markdown输出**
    Crawl4AI将网页转换为干净Markdown的思路非常适合RAG应用。我们可以在数据管道（Pipeline）中增加一个步骤，调用LLM将抓取到的HTML内容转换为结构化的Markdown，作为最终交付成果之一。

## 5. 结论

通过集成双模式AI辅助功能，您的数据采集平台现在已经进化为一个**智能、健壮、面向未来**的系统。它不仅能高效完成当前的采集任务，更能轻松应对未来各种复杂多变的网站，同时将开发和维护成本降至最低。
