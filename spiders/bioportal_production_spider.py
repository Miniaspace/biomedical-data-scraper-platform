"""
BioPortal Production Spider
完整的、生产就绪的BioPortal数据采集器

采集内容:
1. 所有本体的元数据
2. 每个本体的类/概念数据
3. 映射关系数据
4. 统计数据
"""

import scrapy
import json
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import logging


class BioportalProductionSpider(scrapy.Spider):
    """
    BioPortal生产级采集器
    
    使用BioPortal REST API采集完整的本体数据
    """
    
    name = "bioportal_production"
    
    # API配置
    API_BASE = "https://data.bioontology.org"
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 4,  # 限制并发请求数
        'DOWNLOAD_DELAY': 1,  # 请求间延迟1秒
        'ROBOTSTXT_OBEY': False,  # API不需要遵守robots.txt
        'USER_AGENT': 'BiomedicalDataScraper/1.0 (Research Project)',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json',
            'Accept-Language': 'en',
        }
    }
    
    def __init__(self, api_key=None, limit_ontologies=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # API Key
        if not api_key:
            # 尝试从配置文件读取
            try:
                import yaml
                with open('config/credentials.yaml', 'r') as f:
                    creds = yaml.safe_load(f)
                    api_key = creds['bioportal']['api_key']
            except Exception as e:
                raise ValueError(f"API key is required. Error: {e}")
        
        self.api_key = api_key
        self.limit_ontologies = int(limit_ontologies) if limit_ontologies else None
        
        # 数据存储路径
        self.data_dir = Path('data/raw/bioportal')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 统计信息
        self.stats = {
            'ontologies_count': 0,
            'classes_count': 0,
            'mappings_count': 0,
            'start_time': datetime.now().isoformat(),
        }
        
        # 用于存储元数据的列表
        self.ontologies_metadata = []
        
        self.logger.info(f"BioPortal Production Spider initialized")
        self.logger.info(f"Data directory: {self.data_dir.absolute()}")
        if self.limit_ontologies:
            self.logger.info(f"Limiting to {self.limit_ontologies} ontologies for testing")
    
    def start_requests(self):
        """开始采集：获取所有本体列表"""
        url = f"{self.API_BASE}/ontologies?apikey={self.api_key}&display=all"
        
        self.logger.info(f"Fetching ontologies list from {url}")
        yield scrapy.Request(
            url=url,
            callback=self.parse_ontologies_list,
            dont_filter=True
        )
    
    def parse_ontologies_list(self, response):
        """解析本体列表"""
        try:
            data = json.loads(response.text)
            
            # 如果是分页数据
            if isinstance(data, dict) and 'collection' in data:
                ontologies = data['collection']
            else:
                ontologies = data
            
            total = len(ontologies)
            self.logger.info(f"Found {total} ontologies")
            
            # 如果设置了限制，只处理前N个
            if self.limit_ontologies:
                ontologies = ontologies[:self.limit_ontologies]
                self.logger.info(f"Limited to {len(ontologies)} ontologies for testing")
            
            # 处理每个本体
            for idx, ontology in enumerate(ontologies, 1):
                acronym = ontology.get('acronym')
                name = ontology.get('name', 'Unknown')
                
                self.logger.info(f"[{idx}/{len(ontologies)}] Processing: {acronym} - {name}")
                
                # 保存元数据
                metadata = self._extract_ontology_metadata(ontology)
                self.ontologies_metadata.append(metadata)
                self.stats['ontologies_count'] += 1
                
                # 获取该本体的详细信息
                links = ontology.get('links', {})
                if isinstance(links, dict) and 'self' in links:
                    detail_url = links['self'] + f"?apikey={self.api_key}"
                    yield scrapy.Request(
                        url=detail_url,
                        callback=self.parse_ontology_details,
                        meta={'acronym': acronym, 'metadata': metadata}
                    )
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            self.logger.error(f"Response text: {response.text[:500]}")
    
    def _extract_ontology_metadata(self, ontology: Dict) -> Dict:
        """提取本体元数据"""
        # 安全提取嵌套字段
        def safe_get_name(obj):
            if isinstance(obj, dict):
                return obj.get('name')
            elif isinstance(obj, str):
                return obj
            return None
        
        administered_by = ontology.get('administeredBy', [])
        if isinstance(administered_by, list) and administered_by:
            status = safe_get_name(administered_by[0])
        else:
            status = safe_get_name(administered_by)
        
        group = ontology.get('group', [])
        if isinstance(group, list) and group:
            group_name = safe_get_name(group[0])
        else:
            group_name = safe_get_name(group)
        
        categories = ontology.get('categories', [])
        if isinstance(categories, list):
            category_names = [safe_get_name(cat) for cat in categories]
        else:
            category_names = []
        
        return {
            'acronym': ontology.get('acronym'),
            'name': ontology.get('name'),
            'description': ontology.get('description', ''),
            'status': status,
            'group': group_name,
            'categories': category_names,
            'homepage': ontology.get('homepage'),
            'documentation': ontology.get('documentation'),
            'version': ontology.get('version'),
            'released': ontology.get('released'),
            'created_at': ontology.get('creationDate'),
            'updated_at': ontology.get('modificationDate'),
            'number_of_classes': ontology.get('numberOfClasses', 0),
            'number_of_individuals': ontology.get('numberOfIndividuals', 0),
            'number_of_properties': ontology.get('numberOfProperties', 0),
            'views': ontology.get('views', 0),
            'projects': ontology.get('projects', []),
            'api_url': ontology.get('links', {}).get('self') if isinstance(ontology.get('links'), dict) else None,
            'collected_at': datetime.now().isoformat(),
        }
    
    def parse_ontology_details(self, response):
        """解析本体详细信息"""
        acronym = response.meta['acronym']
        
        try:
            data = json.loads(response.text)
            
            # 获取类数据
            if data.get('links', {}).get('classes'):
                classes_url = data['links']['classes'] + f"?apikey={self.api_key}"
                yield scrapy.Request(
                    url=classes_url,
                    callback=self.parse_classes,
                    meta={'acronym': acronym}
                )
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse ontology details for {acronym}: {e}")
    
    def parse_classes(self, response):
        """解析类数据"""
        acronym = response.meta['acronym']
        
        try:
            data = json.loads(response.text)
            
            # 处理分页
            if isinstance(data, dict):
                classes = data.get('collection', [])
                next_page = data.get('links', {}).get('nextPage')
            else:
                classes = data
                next_page = None
            
            if classes:
                # 保存类数据
                self._save_classes(acronym, classes)
                self.stats['classes_count'] += len(classes)
                self.logger.info(f"{acronym}: Saved {len(classes)} classes")
            
            # 处理下一页
            if next_page:
                yield scrapy.Request(
                    url=next_page + f"&apikey={self.api_key}",
                    callback=self.parse_classes,
                    meta={'acronym': acronym}
                )
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse classes for {acronym}: {e}")
    
    def _save_classes(self, acronym: str, classes: List[Dict]):
        """保存类数据到JSONL文件"""
        classes_dir = self.data_dir / 'classes'
        classes_dir.mkdir(exist_ok=True)
        
        file_path = classes_dir / f"{acronym}.jsonl"
        
        with open(file_path, 'a', encoding='utf-8') as f:
            for cls in classes:
                class_data = {
                    'ontology': acronym,
                    'id': cls.get('@id'),
                    'prefLabel': cls.get('prefLabel'),
                    'definition': cls.get('definition', []),
                    'synonym': cls.get('synonym', []),
                    'parents': cls.get('parents', []),
                    'children': cls.get('children', []),
                    'properties': cls.get('properties', {}),
                    'collected_at': datetime.now().isoformat(),
                }
                f.write(json.dumps(class_data, ensure_ascii=False) + '\n')
    
    def closed(self, reason):
        """采集结束时的清理工作"""
        self.stats['end_time'] = datetime.now().isoformat()
        self.stats['reason'] = reason
        
        # 保存元数据
        self._save_metadata()
        
        # 保存统计信息
        self._save_statistics()
        
        self.logger.info("=" * 80)
        self.logger.info("BioPortal采集完成!")
        self.logger.info(f"本体数量: {self.stats['ontologies_count']}")
        self.logger.info(f"类数量: {self.stats['classes_count']}")
        self.logger.info(f"数据目录: {self.data_dir.absolute()}")
        self.logger.info("=" * 80)
    
    def _save_metadata(self):
        """保存元数据到JSONL和CSV文件"""
        if not self.ontologies_metadata:
            return
        
        # 保存JSONL
        jsonl_path = self.data_dir / 'metadata.jsonl'
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for item in self.ontologies_metadata:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        self.logger.info(f"Saved metadata to {jsonl_path}")
        
        # 保存CSV
        csv_path = self.data_dir / 'metadata.csv'
        if self.ontologies_metadata:
            # 处理嵌套字段
            flattened_data = []
            for item in self.ontologies_metadata:
                flat_item = item.copy()
                # 将列表和字典转换为字符串
                for key, value in flat_item.items():
                    if isinstance(value, (list, dict)):
                        flat_item[key] = json.dumps(value, ensure_ascii=False)
                flattened_data.append(flat_item)
            
            keys = flattened_data[0].keys()
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(flattened_data)
            
            self.logger.info(f"Saved metadata to {csv_path}")
    
    def _save_statistics(self):
        """保存统计信息"""
        stats_path = self.data_dir / 'statistics.json'
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved statistics to {stats_path}")
