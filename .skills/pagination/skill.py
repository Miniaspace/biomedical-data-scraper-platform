"""
PaginationSkill - 智能翻页Skill
"""

import re
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from common.agent_skills.skill_base import BaseSkill, SkillMetadata


class PaginationSkill(BaseSkill):
    """
    智能翻页Skill
    
    功能:
    - 自动识别"下一页"链接或按钮
    - 支持多种翻页模式（链接、表单、API参数）
    - 生成翻页请求
    """
    
    @property
    def metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="pagination",
            version="1.0.0",
            description="智能翻页，自动识别下一页按钮或API参数",
            author="Biomedical Data Scraper Team",
            tags=["pagination", "navigation", "crawling"],
            priority=70
        )
    
    def can_handle(self, context: Dict[str, Any]) -> bool:
        """
        判断是否需要翻页
        
        检查:
        1. 页面是否有"下一页"链接
        2. URL是否包含分页参数
        3. 是否已经是最后一页
        """
        # 如果明确指定不需要翻页
        if context.get('pagination_disabled'):
            return False
        
        # 如果已经是最后一页
        if context.get('is_last_page'):
            return False
        
        # 检查是否有下一页链接
        html = context.get('html', '')
        if self._find_next_page_link(html, context.get('url', '')):
            return True
        
        # 检查URL是否包含分页参数
        url = context.get('url', '')
        if self._has_pagination_params(url):
            return True
        
        return False
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行翻页
        
        Args:
            context: 包含html, url等信息
        
        Returns:
            包含next_page_url等翻页信息
        """
        html = context.get('html', '')
        current_url = context.get('url', '')
        
        # 尝试多种翻页策略
        next_url = None
        
        # 策略1: 查找"下一页"链接
        next_url = self._find_next_page_link(html, current_url)
        
        # 策略2: 增加页码参数
        if not next_url:
            next_url = self._increment_page_param(current_url)
        
        # 策略3: 增加offset参数
        if not next_url:
            next_url = self._increment_offset_param(current_url, context)
        
        if next_url:
            self.logger.info(f"Found next page: {next_url}")
            return {
                'has_next_page': True,
                'next_page_url': next_url,
                'pagination_method': 'auto'
            }
        else:
            self.logger.info("No next page found")
            return {
                'has_next_page': False,
                'is_last_page': True
            }
    
    def _find_next_page_link(self, html: str, base_url: str) -> Optional[str]:
        """
        在HTML中查找"下一页"链接
        
        Args:
            html: 页面HTML
            base_url: 基础URL，用于解析相对链接
        
        Returns:
            下一页的绝对URL，如果没找到返回None
        """
        # 常见的"下一页"文本
        next_page_texts = [
            'next', 'next page', '下一页', '下页', 'siguiente',
            '›', '»', '→', 'more'
        ]
        
        # 构建正则表达式
        for text in next_page_texts:
            # 查找包含该文本的<a>标签
            pattern = rf'<a[^>]*href=["\']([^"\']+)["\'][^>]*>{text}</a>'
            match = re.search(pattern, html, re.I)
            if match:
                href = match.group(1)
                return urljoin(base_url, href)
            
            # 查找aria-label或title包含该文本的<a>标签
            pattern = rf'<a[^>]*(aria-label|title)=["\'][^"\']*{text}[^"\']*["\'][^>]*href=["\']([^"\']+)["\']'
            match = re.search(pattern, html, re.I)
            if match:
                href = match.group(2)
                return urljoin(base_url, href)
        
        return None
    
    def _has_pagination_params(self, url: str) -> bool:
        """检查URL是否包含分页参数"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # 常见的分页参数名
        pagination_params = ['page', 'p', 'offset', 'start', 'from', 'skip']
        
        return any(param in params for param in pagination_params)
    
    def _increment_page_param(self, url: str) -> Optional[str]:
        """增加URL中的页码参数"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # 尝试找到页码参数
        page_param_names = ['page', 'p', 'pageNum', 'pageNumber']
        
        for param_name in page_param_names:
            if param_name in params:
                try:
                    current_page = int(params[param_name][0])
                    params[param_name] = [str(current_page + 1)]
                    
                    # 重建URL
                    new_query = urlencode(params, doseq=True)
                    new_parsed = parsed._replace(query=new_query)
                    return urlunparse(new_parsed)
                except ValueError:
                    continue
        
        return None
    
    def _increment_offset_param(
        self,
        url: str,
        context: Dict[str, Any]
    ) -> Optional[str]:
        """增加URL中的offset参数"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # 尝试找到offset参数
        offset_param_names = ['offset', 'start', 'from', 'skip']
        
        # 默认每页数量
        page_size = context.get('page_size', 20)
        
        for param_name in offset_param_names:
            if param_name in params:
                try:
                    current_offset = int(params[param_name][0])
                    params[param_name] = [str(current_offset + page_size)]
                    
                    # 重建URL
                    new_query = urlencode(params, doseq=True)
                    new_parsed = parsed._replace(query=new_query)
                    return urlunparse(new_parsed)
                except ValueError:
                    continue
        
        return None
