"""
BioLINCC深度采集器

这是一个真正的"深度采集"示例，展示如何：
1. 多层级爬取（列表 → 详情 → 出版物 → 文件）
2. 下载并管理所有文档文件
3. 提取完整的结构化数据
4. 处理复杂的嵌套关系

作者: Manus AI
日期: 2026-01-17
"""

import scrapy
import json
import re
from urllib.parse import urljoin
from datetime import datetime
from common.base_spider import BaseSpider


class BiolinccDeepSpider(BaseSpider):
    """BioLINCC深度采集器"""
    
    name = 'biolincc_deep'
    platform_name = 'biolincc'
    
    # 自定义设置
    custom_settings = {
        'CONCURRENT_REQUESTS': 4,  # 降低并发，避免封禁
        'DOWNLOAD_DELAY': 2,  # 增加延迟
        'ITEM_PIPELINES': {
            # Pipelines暂时禁用，直接输出到文件
            # 'common.pipeline.data_pipeline.DataPipeline': 300,
        },
        'FILES_STORE': './data/files/biolincc',
    }
    
    def __init__(self, max_studies=None, *args, **kwargs):
        """
        初始化
        
        Args:
            max_studies: 限制采集的研究数量（用于测试）
        """
        super().__init__(*args, **kwargs)
        self.max_studies = int(max_studies) if max_studies else None
        self.studies_count = 0
        
    def start_requests(self):
        """开始爬取：从研究列表页开始"""
        # 第1层：研究列表页
        list_url = 'https://biolincc.nhlbi.nih.gov/studies/'
        
        self.logger.info(f"开始采集BioLINCC平台")
        if self.max_studies:
            self.logger.info(f"测试模式：限制采集{self.max_studies}个研究")
        
        yield scrapy.Request(
            url=list_url,
            callback=self.parse_study_list,
            meta={'playwright': False}  # 不需要浏览器渲染
        )
    
    def parse_study_list(self, response):
        """解析研究列表页"""
        self.logger.info(f"正在解析研究列表页: {response.url}")
        
        # 提取所有研究的链接
        # 研究链接格式: /studies/aric/, /studies/fhs/, etc.
        study_links = response.css('table tbody tr td:first-child a::attr(href)').getall()
        
        self.logger.info(f"找到 {len(study_links)} 个研究")
        
        for link in study_links:
            # 检查是否达到限制
            if self.max_studies and self.studies_count >= self.max_studies:
                self.logger.info(f"已达到限制数量 {self.max_studies}，停止采集")
                return
            
            self.studies_count += 1
            study_url = response.urljoin(link)
            
            # 第2层：进入研究详情页
            yield scrapy.Request(
                url=study_url,
                callback=self.parse_study_detail,
                meta={'playwright': False}
            )
    
    def parse_study_detail(self, response):
        """解析研究详情页 - 核心方法"""
        self.logger.info(f"正在深度解析研究: {response.url}")
        
        # 从URL提取study_id
        study_id = response.url.rstrip('/').split('/')[-1]
        
        # 构建完整的数据项
        item = {
            'track_id': f'biolincc_{study_id}',
            'platform': 'biolincc',
            'study_id': study_id,
            'url': response.url,
            'scraped_at': datetime.now().isoformat(),
            
            # 基础元数据
            'basic_info': self._extract_basic_info(response),
            
            # 同意书信息
            'consent': self._extract_consent_info(response),
            
            # 详细描述
            'available_data': self._extract_section_text(response, 'Available Data'),
            'objectives': self._extract_section_text(response, 'Objectives'),
            'background': self._extract_section_text(response, 'Background'),
            'participants': self._extract_section_text(response, 'Participants'),
            'design': self._extract_section_text(response, 'Design'),
            
            # 文档文件
            'documents': self._extract_documents(response),
            
            # 文件下载列表（用于Pipeline）
            'file_urls': [],
            'files': [],
        }
        
        # 准备文件下载
        for doc in item['documents']:
            if doc.get('url'):
                item['file_urls'].append(doc['url'])
        
        # 输出当前研究的数据
        yield item
        
        # 第3层：爬取出版物列表
        publications_url = response.url.rstrip('/') + '/publications'
        yield scrapy.Request(
            url=publications_url,
            callback=self.parse_publications,
            meta={
                'study_id': study_id,
                'track_id': item['track_id']
            }
        )
    
    def _extract_basic_info(self, response):
        """提取基础信息"""
        info = {}
        
        # 研究名称
        info['name'] = response.css('h1::text').get('').strip()
        
        # 提取所有元数据字段
        meta_fields = response.css('dl')
        if meta_fields:
            for dt, dd in zip(
                meta_fields.css('dt::text').getall(),
                meta_fields.css('dd')
            ):
                field_name = dt.strip().lower().replace(' ', '_')
                field_value = dd.css('::text').get('').strip()
                
                # 处理链接
                if dd.css('a'):
                    links = dd.css('a::attr(href)').getall()
                    if links:
                        field_value = links if len(links) > 1 else links[0]
                
                info[field_name] = field_value
        
        return info
    
    def _extract_consent_info(self, response):
        """提取同意书信息"""
        consent = {}
        
        consent_section = response.css('section:contains("Consent")')
        if consent_section:
            # 提取所有同意书相关字段
            for dt, dd in zip(
                consent_section.css('dt::text').getall(),
                consent_section.css('dd::text').getall()
            ):
                field_name = dt.strip().lower().replace(' ', '_')
                consent[field_name] = dd.strip()
            
            # 提取具体限制
            restrictions = consent_section.css('p::text').get()
            if restrictions:
                consent['specific_restrictions'] = restrictions.strip()
        
        return consent
    
    def _extract_section_text(self, response, section_title):
        """提取指定章节的完整文本"""
        # 查找包含标题的section或div
        section = response.xpath(
            f'//h2[contains(text(), "{section_title}")]/following-sibling::*[1]'
        )
        
        if section:
            # 提取所有文本，保留段落结构
            paragraphs = section.css('::text').getall()
            text = '\n'.join([p.strip() for p in paragraphs if p.strip()])
            return text
        
        return None
    
    def _extract_documents(self, response):
        """提取所有可下载的文档"""
        documents = []
        
        # 查找"Study Documents"部分
        doc_section = response.css('section:contains("Study Documents"), div:contains("Study Documents")')
        
        if doc_section:
            doc_links = doc_section.css('a')
            
            for idx, link in enumerate(doc_links, 1):
                title = link.css('::text').get('').strip()
                url = response.urljoin(link.css('::attr(href)').get())
                
                # 从标题中提取文件信息
                # 例如: "Data Dictionary (PDF - 52.5 MB)"
                format_match = re.search(r'\((\w+)\s*-\s*([\d.]+)\s*(\w+)\)', title)
                
                doc = {
                    'type': self._classify_document_type(title),
                    'title': re.sub(r'\s*\([^)]+\)', '', title).strip(),  # 移除括号内容
                    'url': url,
                    'file_type': 'supplementary',  # 归类为补充材料
                    'filename': f'sup_{idx}.pdf',  # 标准化文件名
                }
                
                if format_match:
                    doc['format'] = format_match.group(1)
                    doc['size_value'] = float(format_match.group(2))
                    doc['size_unit'] = format_match.group(3)
                
                documents.append(doc)
        
        return documents
    
    def _classify_document_type(self, title):
        """根据标题分类文档类型"""
        title_lower = title.lower()
        
        if 'data dictionary' in title_lower:
            if 'ancillary' in title_lower:
                return 'data_dictionary_ancillary'
            return 'data_dictionary'
        elif 'documentation' in title_lower:
            return 'data_documentation'
        elif 'manual' in title_lower:
            return 'manual'
        elif 'protocol' in title_lower:
            return 'protocol'
        else:
            return 'other'
    
    def parse_publications(self, response):
        """解析出版物列表页"""
        study_id = response.meta['study_id']
        track_id = response.meta['track_id']
        
        self.logger.info(f"正在解析研究 {study_id} 的出版物列表")
        
        # 提取出版物信息
        publications = []
        
        # 假设出版物以表格或列表形式展示
        pub_rows = response.css('table tbody tr, ul.publications li')
        
        for row in pub_rows:
            pub = {}
            
            # 提取标题
            pub['title'] = row.css('a::text, strong::text').get('').strip()
            
            # 提取作者
            authors_text = row.css('.authors::text, em::text').get()
            if authors_text:
                pub['authors'] = [a.strip() for a in authors_text.split(',')]
            
            # 提取期刊和年份
            journal_text = row.css('.journal::text').get()
            if journal_text:
                pub['journal'] = journal_text.strip()
            
            year_text = row.css('.year::text').get()
            if year_text:
                pub['year'] = int(re.search(r'\d{4}', year_text).group())
            
            # 提取PMID
            pmid_link = row.css('a[href*="pubmed"]::attr(href)').get()
            if pmid_link:
                pmid_match = re.search(r'(\d+)', pmid_link)
                if pmid_match:
                    pub['pmid'] = pmid_match.group(1)
            
            # 提取DOI
            doi_link = row.css('a[href*="doi.org"]::attr(href)').get()
            if doi_link:
                pub['doi'] = doi_link.replace('https://doi.org/', '')
            
            if pub.get('title'):
                publications.append(pub)
        
        # 输出出版物数据
        if publications:
            yield {
                'track_id': f'{track_id}_publications',
                'platform': 'biolincc',
                'study_id': study_id,
                'data_type': 'publications',
                'publications': publications,
                'count': len(publications),
                'scraped_at': datetime.now().isoformat(),
            }
            
            self.logger.info(f"研究 {study_id} 找到 {len(publications)} 篇出版物")
        else:
            self.logger.warning(f"研究 {study_id} 没有找到出版物")
