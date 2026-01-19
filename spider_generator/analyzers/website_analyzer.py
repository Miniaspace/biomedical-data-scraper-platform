"""
网站分析器模块
自动访问并分析目标网站的结构、内容和采集策略
"""

import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import asyncio
from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebsiteAnalyzer:
    """网站结构分析器"""
    
    def __init__(self, url: str, timeout: int = 30000):
        self.url = url
        self.timeout = timeout
        self.domain = urlparse(url).netloc
        self.analysis_result = {}
        
    async def analyze(self) -> Dict[str, Any]:
        """
        执行完整的网站分析
        
        Returns:
            分析结果字典
        """
        logger.info(f"开始分析网站: {self.url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # 访问页面
                await page.goto(self.url, timeout=self.timeout, wait_until='networkidle')
                await asyncio.sleep(2)  # 等待动态内容加载
                
                # 执行各项分析
                self.analysis_result = {
                    'url': self.url,
                    'domain': self.domain,
                    'site_type': await self._detect_site_type(page),
                    'has_login': await self._detect_login_requirement(page),
                    'pagination': await self._analyze_pagination(page),
                    'data_structure': await self._analyze_data_structure(page),
                    'api_info': await self._detect_api_calls(page),
                    'files': await self._detect_file_types(page),
                    'anti_scraping': await self._detect_anti_scraping(page),
                    'screenshot_path': await self._save_screenshot(page),
                    'html_sample': await self._get_html_sample(page),
                }
                
                logger.info(f"网站分析完成: {self.analysis_result['site_type']}")
                
            except Exception as e:
                logger.error(f"分析过程中出错: {str(e)}")
                self.analysis_result['error'] = str(e)
                
            finally:
                await browser.close()
                
        return self.analysis_result
    
    async def _detect_site_type(self, page: Page) -> str:
        """
        检测网站类型
        
        Returns:
            网站类型: data_repository, journal, database, clinical_trial, biobank等
        """
        html = await page.content()
        text = await page.inner_text('body')
        text_lower = text.lower()
        
        # 关键词匹配
        if any(kw in text_lower for kw in ['biobank', 'biorepository', 'specimen']):
            return 'biobank'
        elif any(kw in text_lower for kw in ['clinical trial', 'clinicaltrials', 'trial registry']):
            return 'clinical_trial'
        elif any(kw in text_lower for kw in ['journal', 'article', 'publication', 'manuscript']):
            return 'journal'
        elif any(kw in text_lower for kw in ['database', 'repository', 'data archive']):
            return 'data_repository'
        elif any(kw in text_lower for kw in ['ontology', 'terminology', 'vocabulary']):
            return 'ontology'
        else:
            return 'unknown'
    
    async def _detect_login_requirement(self, page: Page) -> bool:
        """检测是否需要登录"""
        html = await page.content()
        
        # 检查登录相关元素
        login_indicators = [
            'input[type="password"]',
            'button:has-text("Login")',
            'button:has-text("Sign in")',
            'a:has-text("Login")',
            'a:has-text("Sign in")',
        ]
        
        for selector in login_indicators:
            try:
                element = await page.query_selector(selector)
                if element:
                    return True
            except:
                pass
        
        # 检查URL和文本
        if 'login' in self.url.lower() or 'signin' in self.url.lower():
            return True
            
        text = await page.inner_text('body')
        if 'please log in' in text.lower() or 'please sign in' in text.lower():
            return True
            
        return False
    
    async def _analyze_pagination(self, page: Page) -> Dict[str, Any]:
        """
        分析分页机制
        
        Returns:
            分页信息字典
        """
        pagination_info = {
            'type': 'none',
            'selectors': [],
            'total_pages': None,
        }
        
        html = await page.content()
        
        # 检测分页按钮
        next_selectors = [
            'a:has-text("Next")',
            'button:has-text("Next")',
            'a:has-text(">")',
            '.pagination a.next',
            'a[rel="next"]',
        ]
        
        for selector in next_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    pagination_info['type'] = 'next_button'
                    pagination_info['selectors'].append(selector)
                    break
            except:
                pass
        
        # 检测页码列表
        page_number_selectors = [
            '.pagination a',
            'ul.pagination li',
            '.page-numbers a',
        ]
        
        for selector in page_number_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if len(elements) > 2:
                    pagination_info['type'] = 'page_numbers'
                    pagination_info['selectors'].append(selector)
                    
                    # 尝试获取总页数
                    for elem in elements:
                        text = await elem.inner_text()
                        if text.isdigit():
                            pagination_info['total_pages'] = max(
                                pagination_info['total_pages'] or 0, 
                                int(text)
                            )
                    break
            except:
                pass
        
        # 检测无限滚动
        if 'infinite' in html.lower() or 'lazy' in html.lower():
            pagination_info['type'] = 'infinite_scroll'
        
        return pagination_info
    
    async def _analyze_data_structure(self, page: Page) -> Dict[str, Any]:
        """
        分析数据结构
        
        Returns:
            数据结构信息
        """
        structure = {
            'list_items': [],
            'detail_link_pattern': None,
            'fields': [],
        }
        
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找列表项（常见的容器元素）
        list_containers = [
            ('table tbody tr', 'table_row'),
            ('ul li', 'list_item'),
            ('div.item', 'div_item'),
            ('div.result', 'result_item'),
            ('article', 'article'),
        ]
        
        for selector, item_type in list_containers:
            items = soup.select(selector)
            if len(items) >= 3:  # 至少3个项目才认为是列表
                structure['list_items'].append({
                    'selector': selector,
                    'type': item_type,
                    'count': len(items),
                })
                
                # 分析第一个项目的结构
                if items:
                    first_item = items[0]
                    
                    # 查找链接
                    links = first_item.find_all('a', href=True)
                    if links:
                        structure['detail_link_pattern'] = links[0].get('href')
                    
                    # 识别字段
                    structure['fields'] = self._identify_fields(first_item)
                
                break
        
        return structure
    
    def _identify_fields(self, element) -> List[str]:
        """识别数据字段类型"""
        fields = []
        text = element.get_text().lower()
        
        # 常见字段关键词
        field_keywords = {
            'title': ['title', 'name', 'study'],
            'author': ['author', 'investigator', 'pi'],
            'date': ['date', 'year', 'published'],
            'abstract': ['abstract', 'summary', 'description'],
            'doi': ['doi', 'identifier'],
            'institution': ['institution', 'university', 'organization'],
        }
        
        for field, keywords in field_keywords.items():
            if any(kw in text for kw in keywords):
                fields.append(field)
        
        return fields
    
    async def _detect_api_calls(self, page: Page) -> Dict[str, Any]:
        """
        检测API调用
        
        Returns:
            API信息
        """
        api_info = {
            'detected': False,
            'endpoints': [],
        }
        
        # 监听网络请求
        requests = []
        
        def handle_request(request):
            if request.resource_type in ['xhr', 'fetch']:
                requests.append({
                    'url': request.url,
                    'method': request.method,
                    'resource_type': request.resource_type,
                })
        
        page.on('request', handle_request)
        
        # 等待一段时间收集请求
        await asyncio.sleep(3)
        
        # 分析API请求
        api_patterns = ['/api/', '/rest/', '/graphql', '.json', '/v1/', '/v2/']
        
        for req in requests:
            if any(pattern in req['url'] for pattern in api_patterns):
                api_info['detected'] = True
                api_info['endpoints'].append(req)
        
        return api_info
    
    async def _detect_file_types(self, page: Page) -> List[str]:
        """检测可下载的文件类型"""
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        file_types = set()
        
        # 查找所有链接
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '').lower()
            
            # 检测文件扩展名
            extensions = ['.pdf', '.docx', '.xlsx', '.csv', '.zip', '.xml', '.json']
            for ext in extensions:
                if ext in href:
                    file_types.add(ext.replace('.', ''))
        
        return list(file_types)
    
    async def _detect_anti_scraping(self, page: Page) -> Dict[str, Any]:
        """检测反爬机制"""
        anti_scraping = {
            'captcha': False,
            'rate_limiting': False,
            'javascript_required': False,
            'cloudflare': False,
        }
        
        html = await page.content()
        text_lower = html.lower()
        
        # 检测CAPTCHA
        if any(kw in text_lower for kw in ['captcha', 'recaptcha', 'hcaptcha']):
            anti_scraping['captcha'] = True
        
        # 检测Cloudflare
        if 'cloudflare' in text_lower or 'cf-ray' in text_lower:
            anti_scraping['cloudflare'] = True
        
        # 检测JavaScript要求
        noscript = await page.query_selector('noscript')
        if noscript:
            noscript_text = await noscript.inner_text()
            if 'javascript' in noscript_text.lower():
                anti_scraping['javascript_required'] = True
        
        return anti_scraping
    
    async def _save_screenshot(self, page: Page) -> str:
        """保存页面截图"""
        screenshot_path = f"/home/ubuntu/biomedical-data-scraper-platform/spider_generator/screenshots/{self.domain.replace('.', '_')}.png"
        
        try:
            await page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"截图已保存: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            return None
    
    async def _get_html_sample(self, page: Page) -> str:
        """获取HTML样本（前5000字符）"""
        html = await page.content()
        return html[:5000]
    
    def save_analysis(self, output_path: str):
        """保存分析结果到JSON文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_result, f, ensure_ascii=False, indent=2)
        logger.info(f"分析结果已保存: {output_path}")


async def analyze_website(url: str) -> Dict[str, Any]:
    """
    便捷函数：分析单个网站
    
    Args:
        url: 目标网站URL
        
    Returns:
        分析结果字典
    """
    analyzer = WebsiteAnalyzer(url)
    return await analyzer.analyze()


if __name__ == '__main__':
    # 测试
    import sys
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    else:
        test_url = 'https://biolincc.nhlbi.nih.gov/studies/'
    
    result = asyncio.run(analyze_website(test_url))
    print(json.dumps(result, indent=2, ensure_ascii=False))
