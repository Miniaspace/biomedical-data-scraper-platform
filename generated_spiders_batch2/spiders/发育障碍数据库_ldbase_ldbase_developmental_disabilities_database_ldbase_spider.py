"""
发育障碍数据库 LDbase LDbase (Developmental Disabilities Database LDbase) 数据采集器

生成时间: 2026-01-18 06:29:55
平台URL: https://ldbase.org
采集策略: playwright
"""

import scrapy
from scrapy import Request
import uuid
import json
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class 发育障碍数据库LdbaseLdbaseDevelopmentalDisabilitiesDatabaseLdbaseSpider(scrapy.Spider):
    """发育障碍数据库 LDbase LDbase (Developmental Disabilities Database LDbase) 数据采集器"""
    
    name = "发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase"
    allowed_domains = ['ldbase.org']
    start_urls = ['https://ldbase.org']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'ITEM_PIPELINES': {
            'pipelines.enhanced_files_pipeline.EnhancedFilesPipeline': 1,
        },
        'FILES_STORE': './downloads/发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase',
        'FEEDS': {
            f'output/发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonl': {
                'format': 'jsonlines',
                'encoding': 'utf-8',
                'overwrite': False,
            },
            f'output/发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': False,
            },
        },
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = {
            'total_items': 0,
            'total_files': 0,
            'errors': 0,
        }
    
    def start_requests(self):
        """生成初始请求"""
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse_list,
                errback=self.handle_error,
                meta={'page': 1}
            )
    
    def parse_list(self, response):
        """
        解析列表页
        
        提取策略:
        由于采用无限滚动(infinite_scroll)分页，使用Playwright模拟用户滚动页面到底部，等待新数据加载，循环此过程直到没有新数据加载为止。
        """
        logger.info(f"正在解析列表页: {response.url} (第{response.meta.get('page', 1)}页)")
        
        # 提取列表项
        items = response.css('ul li')
        logger.info(f"找到 {len(items)} 个项目")
        
        for item in items:
            # 提取详情页链接
            detail_url = item.css('a::attr(href)').get()
            
            if detail_url:
                detail_url = response.urljoin(detail_url)
                yield Request(
                    url=detail_url,
                    callback=self.parse_detail,
                    errback=self.handle_error,
                    meta={'source_list_url': response.url}
                )
        
        # 处理分页
        # TODO: 根据实际分页机制调整
        # 示例：下一页按钮
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield Request(
                url=response.urljoin(next_page),
                callback=self.parse_list,
                errback=self.handle_error
            )
    
    def parse_detail(self, response):
        """
        解析详情页
        
        提取策略:
        登录后通过Playwright获取文件下载链接，使用带有登录状态的会话进行文件下载。对PDF及补充材料链接进行请求并保存。支持断点续传和重试机制。
        """
        logger.info(f"正在解析详情页: {response.url}")
        
        # 生成唯一track_id
        track_id = str(uuid.uuid4())
        
        # 提取元数据
        item = {
            'track_id': track_id,
            'url': response.url,
            'source_list_url': response.meta.get('source_list_url'),
            'crawl_time': datetime.now().isoformat(),
            'platform': '发育障碍数据库 LDbase LDbase (Developmental Disabilities Database LDbase)',
        }
        
        # 提取各字段
        
        item['title'] = self._extract_field(
            response, 
            'css=ul li .title, xpath=./descendant::*[contains(@class,'title')]',
            'title'
        )
        
        item['author'] = self._extract_field(
            response, 
            'css=ul li .author, xpath=./descendant::*[contains(@class,'author')]',
            'author'
        )
        
        item['date'] = self._extract_field(
            response, 
            'css=ul li .date, xpath=./descendant::*[contains(@class,'date')]',
            'date'
        )
        
        item['description'] = self._extract_field(
            response, 
            'css=ul li .description, xpath=./descendant::*[contains(@class,'description')]',
            'description'
        )
        
        item['pdf_link'] = self._extract_field(
            response, 
            'css=ul li a[href$='.pdf']',
            'pdf_link'
        )
        
        item['supplementary_material_link'] = self._extract_field(
            response, 
            'css=ul li a.supplementary-material',
            'supplementary_material_link'
        )
        
        
        # 提取文件链接
        file_urls = []
        
        # 主文件（PDF等）
        
        main_file_links = response.css('a[href$=".pdf"]::attr(href)').getall()
        for link in main_file_links:
            full_url = response.urljoin(link)
            file_urls.append({
                'url': full_url,
                'type': 'main_file',
                'track_id': track_id,
            })
        
        
        # 补充材料
        
        supp_file_links = response.css('a[href*="supplement"]::attr(href), a[href*="additional"]::attr(href)').getall()
        for idx, link in enumerate(supp_file_links, 1):
            full_url = response.urljoin(link)
            file_urls.append({
                'url': full_url,
                'type': 'SI_file',
                'track_id': track_id,
                'index': idx,
            })
        
        
        if file_urls:
            item['file_urls'] = file_urls
            logger.info(f"找到 {len(file_urls)} 个文件待下载")
        
        self.stats['total_items'] += 1
        
        yield item
    
    def _extract_field(self, response, selector: str, field_name: str) -> Optional[str]:
        """
        提取单个字段
        
        Args:
            response: Scrapy响应对象
            selector: CSS选择器
            field_name: 字段名称
            
        Returns:
            提取的文本内容
        """
        try:
            if selector.startswith('//'):
                # XPath选择器
                value = response.xpath(selector).get()
            else:
                # CSS选择器
                value = response.css(selector).get()
            
            if value:
                value = value.strip()
                logger.debug(f"成功提取字段 {field_name}: {value[:50]}...")
                return value
            else:
                logger.warning(f"字段 {field_name} 未找到内容")
                return None
                
        except Exception as e:
            logger.error(f"提取字段 {field_name} 时出错: {str(e)}")
            return None
    
    def handle_error(self, failure):
        """处理请求错误"""
        logger.error(f"请求失败: {failure.request.url}")
        logger.error(f"错误信息: {failure.value}")
        self.stats['errors'] += 1
    
    def closed(self, reason):
        """Spider关闭时的回调"""
        logger.info("=" * 50)
        logger.info(f"Spider 发育障碍数据库_ldbase_ldbase_developmental_disabilities_database_ldbase 已关闭")
        logger.info(f"关闭原因: {reason}")
        logger.info(f"采集统计:")
        logger.info(f"  - 总项目数: {self.stats['total_items']}")
        logger.info(f"  - 总文件数: {self.stats['total_files']}")
        logger.info(f"  - 错误数: {self.stats['errors']}")
        logger.info("=" * 50)