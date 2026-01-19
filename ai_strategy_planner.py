"""
AI策略规划器
使用GPT-4分析网站特征并生成最优采集策略
"""

import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIStrategyPlanner:
    """AI驱动的采集策略规划器"""
    
    def __init__(self, model: str = "gpt-4.1-mini"):
        """
        初始化AI策略规划器
        
        Args:
            model: 使用的AI模型
        """
        self.client = OpenAI()  # API key已在环境变量中配置
        self.model = model
        
    def plan_strategy(self, analysis_result: Dict[str, Any], 
                     target_data: Optional[str] = None) -> Dict[str, Any]:
        """
        基于网站分析结果生成采集策略
        
        Args:
            analysis_result: 网站分析结果
            target_data: 目标数据类型（可选）
            
        Returns:
            采集策略字典
        """
        logger.info(f"正在为 {analysis_result.get('url')} 生成采集策略...")
        
        # 构建提示词
        prompt = self._build_prompt(analysis_result, target_data)
        
        try:
            # 调用GPT-4
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # 解析响应
            strategy = json.loads(response.choices[0].message.content)
            logger.info(f"策略生成成功，推荐方法: {strategy.get('recommended_method')}")
            
            return strategy
            
        except Exception as e:
            logger.error(f"AI策略生成失败: {str(e)}")
            # 返回默认策略
            return self._get_fallback_strategy(analysis_result)
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一个专业的网页数据采集专家，精通Scrapy、Playwright等工具。
你的任务是分析网站结构，并提供最优的数据采集策略。

请基于提供的网站分析信息，生成详细的采集策略，包括：
1. 推荐的采集方法（scrapy/playwright/api/hybrid）
2. 具体的数据提取选择器（CSS或XPath）
3. 分页处理策略
4. 文件下载策略
5. 需要注意的反爬机制和应对方法
6. 采集难度评估（1-5星）
7. 预估的开发时间

请以JSON格式返回，确保结构清晰、建议具体可行。"""
    
    def _build_prompt(self, analysis_result: Dict[str, Any], 
                     target_data: Optional[str]) -> str:
        """构建用户提示词"""
        
        prompt = f"""请分析以下生物医学平台网站并提供采集策略：

## 基本信息
- URL: {analysis_result.get('url')}
- 域名: {analysis_result.get('domain')}
- 网站类型: {analysis_result.get('site_type')}

## 网站特征
- 需要登录: {analysis_result.get('has_login')}
- 分页类型: {analysis_result.get('pagination', {}).get('type')}
- 检测到API: {analysis_result.get('api_info', {}).get('detected')}
- 可下载文件类型: {', '.join(analysis_result.get('files', []))}

## 数据结构
{json.dumps(analysis_result.get('data_structure', {}), indent=2, ensure_ascii=False)}

## API信息
{json.dumps(analysis_result.get('api_info', {}), indent=2, ensure_ascii=False)}

## 反爬机制
{json.dumps(analysis_result.get('anti_scraping', {}), indent=2, ensure_ascii=False)}

## HTML样本
```html
{analysis_result.get('html_sample', '')[:1000]}
```

## 目标数据
{target_data or '采集所有可用的研究数据、元数据、PDF文件、补充材料等'}

请提供详细的采集策略，以JSON格式返回，包含以下字段：
{{
  "recommended_method": "scrapy/playwright/api/hybrid",
  "spider_template": "basic/api/playwright/login/hybrid",
  "difficulty": 1-5,
  "estimated_dev_time": "小时数",
  "data_extraction": {{
    "list_page_selector": "CSS或XPath选择器",
    "detail_page_selector": "CSS或XPath选择器",
    "fields": {{
      "title": "选择器",
      "author": "选择器",
      ...
    }}
  }},
  "pagination_strategy": "具体策略描述",
  "file_download_strategy": "具体策略描述",
  "anti_scraping_handling": ["应对方法1", "应对方法2"],
  "special_considerations": ["注意事项1", "注意事项2"],
  "code_snippets": {{
    "parse_list": "示例代码",
    "parse_detail": "示例代码"
  }}
}}
"""
        return prompt
    
    def _get_fallback_strategy(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """当AI调用失败时返回的默认策略"""
        
        site_type = analysis_result.get('site_type', 'unknown')
        has_api = analysis_result.get('api_info', {}).get('detected', False)
        has_login = analysis_result.get('has_login', False)
        
        # 基于规则的简单策略
        if has_api:
            method = 'api'
            template = 'api_spider'
        elif has_login:
            method = 'playwright'
            template = 'login_spider'
        else:
            method = 'scrapy'
            template = 'basic_spider'
        
        return {
            'recommended_method': method,
            'spider_template': template,
            'difficulty': 3,
            'estimated_dev_time': '4-8小时',
            'data_extraction': {
                'list_page_selector': 'table tbody tr, ul li, div.item',
                'detail_page_selector': 'a[href*="detail"], a[href*="study"]',
                'fields': {}
            },
            'pagination_strategy': '使用Scrapy的自动翻页或手动处理Next按钮',
            'file_download_strategy': '使用EnhancedFilesPipeline下载所有PDF和附件',
            'anti_scraping_handling': [
                '添加随机延迟（1-3秒）',
                '使用User-Agent轮换',
                '必要时使用代理'
            ],
            'special_considerations': [
                '需要手动验证选择器',
                '建议先进行小规模测试',
                '注意遵守网站robots.txt'
            ],
            'code_snippets': {},
            'note': '这是一个基于规则的默认策略，建议手动调整'
        }
    
    def compare_strategies(self, strategies: list) -> Dict[str, Any]:
        """
        比较多个策略，选择最优方案
        
        Args:
            strategies: 策略列表
            
        Returns:
            最优策略
        """
        if not strategies:
            return None
        
        # 简单评分：难度越低、开发时间越短越好
        def score_strategy(strategy):
            difficulty = strategy.get('difficulty', 5)
            dev_time = strategy.get('estimated_dev_time', '8')
            
            # 提取小时数
            import re
            hours = re.findall(r'\d+', str(dev_time))
            hours = int(hours[0]) if hours else 8
            
            # 评分：难度权重0.4，时间权重0.6
            return (6 - difficulty) * 0.4 + (10 - hours) * 0.6
        
        best_strategy = max(strategies, key=score_strategy)
        return best_strategy


def generate_strategy(analysis_result: Dict[str, Any], 
                     target_data: Optional[str] = None,
                     model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    """
    便捷函数：生成采集策略
    
    Args:
        analysis_result: 网站分析结果
        target_data: 目标数据类型
        model: AI模型
        
    Returns:
        采集策略
    """
    planner = AIStrategyPlanner(model=model)
    return planner.plan_strategy(analysis_result, target_data)


if __name__ == '__main__':
    # 测试
    test_analysis = {
        'url': 'https://biolincc.nhlbi.nih.gov/studies/',
        'domain': 'biolincc.nhlbi.nih.gov',
        'site_type': 'data_repository',
        'has_login': False,
        'pagination': {'type': 'page_numbers'},
        'api_info': {'detected': False},
        'files': ['pdf', 'zip'],
        'data_structure': {
            'list_items': [{'selector': 'table tbody tr', 'count': 20}],
            'fields': ['title', 'date']
        },
        'anti_scraping': {'captcha': False}
    }
    
    strategy = generate_strategy(test_analysis)
    print(json.dumps(strategy, indent=2, ensure_ascii=False))
