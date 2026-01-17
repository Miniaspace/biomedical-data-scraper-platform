# Agent Skills 高级指南：构建可复用的智能采集能力

**版本**: 5.0
**日期**: 2026年1月16日

## 1. 概述：从“重复造轮子”到“搭积木”

您提出的“Agent Skills”是一个极具前瞻性的想法，它将彻底改变我们开发和维护数据采集器的方式。通过引入Agent Skills架构，我们正在从传统的、为每个网站“重复造轮子”的模式，转向一个**可复用、可组合、可扩展的“搭积木”模式**。

本指南将详细介绍我们为您构建的、基于业界标准的**Agent Skills框架**。

## 2. 核心理念：Skills即服务 (Skills as a Service)

**什么是Skill？**

一个Skill是一个**独立的、原子化的能力模块**，它封装了一项特定的采集功能（如登录、翻页、验证码识别等）。每个Skill都遵循业界标准的`SKILL.md`格式，包含了元数据、配置、代码和文档。

**我们的架构**：

我们为您设计并实现了一套先进的**三层Agent Skills架构**：

1.  **Skills层 (能力层)**: 包含了所有可复用的能力模块，如`LoginSkill`, `PaginationSkill`等。
2.  **Agent层 (智能编排层)**: 负责智能决策，根据目标网站的特征，自动选择和组合合适的Skills。
3.  **Orchestrator层 (任务调度层)**: 基于我们现有的Airflow架构，负责任务的调度、监控和资源管理。

## 3. 框架核心模块详解

我们为您实现了Agent Skills框架的核心，并提供了两个开箱即用的示例Skills。

### 3.1. 核心框架 (`common/agent_skills/skill_base.py`)

这是整个Agent Skills系统的基石，提供了：

- `BaseSkill`: 所有Skill都必须继承的抽象基类。
- `SkillRegistry`: 用于注册和管理所有可用的Skills。
- `SkillLoader`: 从文件系统（`.skills`目录）自动加载所有Skills。
- `SkillAgent`: 智能编排和执行Skills流水线。

### 3.2. 示例Skill 1: `LoginSkill`

- **位置**: `.skills/login/`
- **功能**: 一个通用的登录处理Skill，能够自动识别登录表单、填充凭证并处理登录流程。
- **价值**: 未来开发新的需要登录的采集器时，您**无需再编写任何登录逻辑**，只需调用这个Skill即可。

### 3.3. 示例Skill 2: `PaginationSkill`

- **位置**: `.skills/pagination/`
- **功能**: 一个智能的翻页Skill，能够自动识别“下一页”链接、处理多种分页参数（如`page=2`, `offset=20`）。
- **价值**: 您**无需再为每个网站编写复杂的翻页逻辑**，这个Skill会自动处理绝大多数情况。

## 4. 如何使用和扩展Skills

### 4.1. 使用现有Skills

在您的Spider中，您可以像这样使用Skills：

```python
# my_spider.py

from common.agent_skills.skill_base import get_global_registry, SkillAgent

class MySpider(scrapy.Spider):
    name = "my_platform"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 获取全局注册表并创建Agent
        self.registry = get_global_registry()
        self.agent = SkillAgent(self.registry)
        
        # 加载所有Skills
        from common.agent_skills.skill_base import SkillLoader
        loader = SkillLoader()
        loader.load_all_skills(self.registry)
    
    def parse(self, response):
        # 准备上下文
        context = {
            'response': response,
            'html': response.text,
            'url': response.url,
            'credentials': self.credentials
        }
        
        # 让Agent自动选择并执行Skills
        result = self.agent.execute_pipeline(context)
        
        # 处理结果
        if result.get('has_next_page'):
            yield scrapy.Request(result['next_page_url'], self.parse)
```

### 4.2. 创建新的Skill

创建新的Skill非常简单，只需三步：

1.  在`.skills/`目录下创建一个新目录，例如`my_new_skill`。
2.  在该目录下创建一个`skill.py`文件，并实现一个继承自`BaseSkill`的类。
3.  在该目录下创建一个`SKILL.md`文件，描述Skill的功能和用法。

完成后，`SkillLoader`会自动发现并加载您的新Skill。

## 5. 结论：一个可成长的智能系统

通过引入Agent Skills架构，您的数据采集平台已经从一个简单的自动化工具，进化成了一个**可成长、可扩展的智能系统**。

- **开发效率将提升数倍**：通过复用标准化的Skills，开发人员可以专注于业务逻辑，而不是重复的基础工作。
- **维护成本将大幅降低**：当网站结构变化时，往往只需更新或调整相应的Skill，而无需重写整个采集器。
- **知识得以沉淀**：每一个新的Skill都成为团队的宝贵资产，让您的数据采集能力不断增强。

这为您未来的数据采集工作奠定了坚实、高效且极具前瞻性的基础。
