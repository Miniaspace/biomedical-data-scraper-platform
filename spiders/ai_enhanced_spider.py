"""
AI增强的Spider示例
展示如何使用LLM辅助提取复杂、非结构化的数据
"""

import scrapy
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

from common.base_spider import BaseSpider
from common.ai.llm_extractor import HybridLLMExtractor


# 定义数据模型
class Author(BaseModel):
    """作者信息"""
    name: str = Field(description="作者姓名")
    affiliation: Optional[str] = Field(default=None, description="所属机构")
    email: Optional[str] = Field(default=None, description="电子邮件")


class Publication(BaseModel):
    """发表信息"""
    title: str = Field(description="论文标题")
    authors: List[Author] = Field(description="作者列表")
    abstract: Optional[str] = Field(default=None, description="摘要")
    publication_date: Optional[str] = Field(default=None, description="发表日期,ISO 8601格式")
    doi: Optional[str] = Field(default=None, description="DOI")
    journal: Optional[str] = Field(default=None, description="期刊名称")
    keywords: List[str] = Field(default_factory=list, description="关键词列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "AI in Healthcare",
                "authors": [{"name": "John Doe", "affiliation": "MIT"}],
                "publication_date": "2024-01-15"
            }
        }


class AIEnhancedSpider(BaseSpider):
    """
    AI增强的Spider
    
    使用场景:
    1. 页面结构复杂,难以用CSS选择器精确定位
    2. 数据分散在多个位置,需要智能整合
    3. 需要理解语义而非仅匹配模式
    
    特点:
    - 自动fallback: 本地LLM失败时自动切换到商用API
    - 质量保证: 自动验证提取质量
    - 灵活适配: 无需为每个网站编写复杂的选择器
    """
    
    name = "ai_enhanced_spider"
    
    # Spider配置
    custom_settings = {
        **BaseSpider.custom_settings,
        # 启用AI辅助
        'AI_ENABLED': True,
        'AI_MODE': 'hybrid',  # 'local', 'commercial', 'hybrid'
        'AI_LOCAL_MODEL': 'llama3.1:8b',
        'AI_COMMERCIAL_MODEL': 'gpt-4o-mini',
        'AI_QUALITY_THRESHOLD': 7.0,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 初始化AI提取器
        ai_mode = self.settings.get('AI_MODE', 'hybrid')
        
        if ai_mode == 'hybrid':
            self.ai_extractor = HybridLLMExtractor(
                local_model=self.settings.get('AI_LOCAL_MODEL', 'llama3.1:8b'),
                commercial_model=self.settings.get('AI_COMMERCIAL_MODEL', 'gpt-4o-mini'),
                quality_threshold=self.settings.get('AI_QUALITY_THRESHOLD', 7.0)
            )
        else:
            from common.ai.llm_extractor import LLMExtractor
            self.ai_extractor = LLMExtractor(
                mode=ai_mode,
                model=self.settings.get(f'AI_{ai_mode.upper()}_MODEL')
            )
        
        self.logger.info(f"AI提取器已初始化: mode={ai_mode}")
    
    def parse_detail_page(self, response):
        """
        使用AI提取详情页数据
        
        传统方法需要:
        - 编写复杂的CSS选择器
        - 处理各种边界情况
        - 针对每个网站定制代码
        
        AI方法:
        - 提取页面文本
        - 让LLM理解并提取
        - 自动处理各种格式
        """
        # 提取页面主要文本内容
        # 方法1: 使用Scrapy的内置方法
        page_text = ' '.join(response.css('body ::text').getall())
        
        # 方法2: 只提取主要内容区域(推荐)
        main_content = response.css('main, article, .content, #content').get()
        if main_content:
            page_text = scrapy.Selector(text=main_content).css('::text').getall()
            page_text = ' '.join(page_text)
        
        # 清理文本
        page_text = ' '.join(page_text.split())  # 规范化空白字符
        page_text = page_text[:10000]  # 限制长度以节省token
        
        self.logger.info(f"开始AI提取: {response.url}, 文本长度: {len(page_text)}")
        
        # 使用AI提取结构化数据
        publication = self.ai_extractor.extract(
            text=page_text,
            schema=Publication,
            instruction="请特别注意提取所有作者的完整信息,包括姓名、机构和邮箱"
        )
        
        if publication is None:
            self.logger.error(f"AI提取失败: {response.url}")
            return
        
        # 转换为item格式
        item = self.extract_common_metadata(response)
        item.update(publication.model_dump())
        
        # 记录使用的模式
        item['extraction_method'] = 'ai'
        item['ai_model'] = self.ai_extractor.model
        
        self.logger.info(f"AI提取成功: {publication.title}")
        
        yield item
    
    def parse_with_fallback(self, response):
        """
        混合策略: 先尝试传统方法,失败则使用AI
        
        这是最经济的方案:
        - 简单页面用传统方法(快速、免费)
        - 复杂页面用AI(准确、灵活)
        """
        # 先尝试传统方法
        title = response.css('h1.title::text').get()
        
        if title:
            # 传统方法成功
            item = {
                'title': title,
                'authors': response.css('.author::text').getall(),
                'extraction_method': 'traditional'
            }
            yield item
        else:
            # 传统方法失败,使用AI
            self.logger.info("传统方法失败,切换到AI提取")
            yield from self.parse_detail_page(response)
    
    def parse_comments_with_ai(self, response):
        """
        使用AI提取评论
        
        评论通常结构复杂:
        - 嵌套回复
        - 多种格式
        - 动态加载
        
        AI可以理解这些复杂结构
        """
        # 定义评论模型
        class Comment(BaseModel):
            author: str = Field(description="评论者姓名")
            content: str = Field(description="评论内容")
            date: Optional[str] = Field(default=None, description="评论日期")
            replies: List['Comment'] = Field(default_factory=list, description="回复列表")
        
        # 提取评论区文本
        comments_section = response.css('.comments, #comments, .discussion').get()
        if not comments_section:
            self.logger.warning("未找到评论区")
            return
        
        comments_text = scrapy.Selector(text=comments_section).css('::text').getall()
        comments_text = ' '.join(comments_text)
        
        # 使用AI提取
        comments = self.ai_extractor.extract_list(
            text=comments_text,
            item_schema=Comment,
            instruction="请提取所有评论,包括嵌套的回复。保持评论的层级结构。"
        )
        
        self.logger.info(f"提取到 {len(comments)} 条评论")
        
        # 添加到item
        item = self.extract_common_metadata(response)
        item['comments'] = [c.model_dump() for c in comments]
        item['comments_count'] = len(comments)
        
        yield item


# 使用示例
class BioRxivAISpider(AIEnhancedSpider):
    """
    bioRxiv预印本平台的AI增强Spider
    
    bioRxiv的页面结构经常变化,使用AI可以:
    - 自动适应结构变化
    - 提取复杂的作者信息
    - 理解摘要和关键词
    """
    
    name = "biorxiv_ai"
    allowed_domains = ["biorxiv.org"]
    start_urls = ["https://www.biorxiv.org/content/early/recent"]
    
    def parse(self, response):
        """解析列表页"""
        # 提取文章链接
        article_links = response.css('.highwire-article-citation a.highwire-cite-linked-title::attr(href)').getall()
        
        for link in article_links:
            yield response.follow(link, callback=self.parse_detail_page)
    
    def parse_detail_page(self, response):
        """使用AI提取文章详情"""
        # 调用父类的AI提取方法
        yield from super().parse_detail_page(response)
