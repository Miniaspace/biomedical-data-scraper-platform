"""
流利性语言数据库 FB (FluencyBank) 数据采集器

生成时间: 2026-01-18 06:36:51
平台URL: https://fluency.talkbank.org
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


class 流利性语言数据库FbFluencybankSpider(scrapy.Spider):
    """流利性语言数据库 FB (FluencyBank) 数据采集器"""
    
    name = "流利性语言数据库_fb_fluencybank"
    allowed_domains = ['fluency.talkbank.org']
    start_urls = ['https://fluency.talkbank.org']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'ITEM_PIPELINES': {
            'pipelines.enhanced_files_pipeline.EnhancedFilesPipeline': 1,
        },
        'FILES_STORE': './downloads/流利性语言数据库_fb_fluencybank',
        'FEEDS': {
            f'output/流利性语言数据库_fb_fluencybank_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonl': {
                'format': 'jsonlines',
                'encoding': 'utf-8',
                'overwrite': False,
            },
            f'output/流利性语言数据库_fb_fluencybank_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv': {
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
        网站无分页，所有内容集中展示或通过筛选条件加载，需登录后确认是否存在动态加载或筛选分页，若有则通过Playwright模拟点击加载更多或筛选操作
        """
        logger.info(f"正在解析列表页: {response.url} (第{response.meta.get('page', 1)}页)")
        
        # 提取列表项
        items = response.css('待登录后确认具体列表页结构，初步可定位包含研究数据条目的容器，如CSS选择器 div.research-list 或 ul.data-list')
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
        通过Playwright登录后，抓取文件链接（pdf/docx），使用Playwright的页面请求拦截或直接通过Python requests携带登录cookie进行文件下载，确保文件完整性和正确命名
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
            'platform': '流利性语言数据库 FB (FluencyBank)',
        }
        
        # 提取各字段
        
        item['title'] = self._extract_field(
            response, 
            'CSS选择器 h1.article-title 或 XPath //h1[contains(@class,'article-title')]',
            'title'
        )
        
        item['author'] = self._extract_field(
            response, 
            'CSS选择器 div.authors 或 XPath //div[contains(@class,'authors')]',
            'author'
        )
        
        item['publication_date'] = self._extract_field(
            response, 
            'CSS选择器 span.pub-date 或 XPath //span[contains(@class,'pub-date')]',
            'publication_date'
        )
        
        item['abstract'] = self._extract_field(
            response, 
            'CSS选择器 div.abstract 或 XPath //div[contains(@class,'abstract')]',
            'abstract'
        )
        
        item['pdf_link'] = self._extract_field(
            response, 
            'CSS选择器 a[href$='.pdf'] 或 XPath //a[contains(@href,'.pdf')]',
            'pdf_link'
        )
        
        item['docx_link'] = self._extract_field(
            response, 
            'CSS选择器 a[href$='.docx'] 或 XPath //a[contains(@href,'.docx')]',
            'docx_link'
        )
        
        item['supplementary_materials'] = self._extract_field(
            response, 
            'CSS选择器 div.supplementary a 或 XPath //div[contains(@class,'supplementary')]//a',
            'supplementary_materials'
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
        logger.info(f"Spider 流利性语言数据库_fb_fluencybank 已关闭")
        logger.info(f"关闭原因: {reason}")
        logger.info(f"采集统计:")
        logger.info(f"  - 总项目数: {self.stats['total_items']}")
        logger.info(f"  - 总文件数: {self.stats['total_files']}")
        logger.info(f"  - 错误数: {self.stats['errors']}")
        logger.info("=" * 50)