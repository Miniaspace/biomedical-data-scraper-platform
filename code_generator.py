"""
代码生成器模块
基于策略和模板生成完整的Spider代码
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeGenerator:
    """Spider代码生成器"""
    
    def __init__(self, templates_dir: str = None):
        """
        初始化代码生成器
        
        Args:
            templates_dir: 模板目录路径
        """
        if templates_dir is None:
            templates_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'templates'
            )
        
        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
    def generate_spider(self, 
                       platform_info: Dict[str, Any],
                       strategy: Dict[str, Any],
                       output_dir: str) -> Dict[str, str]:
        """
        生成Spider代码
        
        Args:
            platform_info: 平台信息
            strategy: 采集策略
            output_dir: 输出目录
            
        Returns:
            生成的文件路径字典
        """
        logger.info(f"正在为 {platform_info['name']} 生成Spider代码...")
        
        # 准备模板变量
        template_vars = self._prepare_template_vars(platform_info, strategy)
        
        # 选择模板
        template_name = strategy.get('spider_template', 'basic_spider')
        template_file = f"{template_name}.py.j2"
        
        try:
            template = self.env.get_template(template_file)
        except Exception as e:
            logger.warning(f"模板 {template_file} 不存在，使用基础模板")
            template = self.env.get_template('basic_spider.py.j2')
        
        # 渲染代码
        spider_code = template.render(**template_vars)
        
        # 生成文件名
        spider_name = self._generate_spider_name(platform_info['name'])
        spider_filename = f"{spider_name}_spider.py"
        spider_path = os.path.join(output_dir, spider_filename)
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 写入文件
        with open(spider_path, 'w', encoding='utf-8') as f:
            f.write(spider_code)
        
        logger.info(f"Spider代码已生成: {spider_path}")
        
        # 生成配置文件
        config_path = self._generate_config(platform_info, strategy, output_dir, spider_name)
        
        # 生成README
        readme_path = self._generate_readme(platform_info, strategy, output_dir, spider_name)
        
        return {
            'spider': spider_path,
            'config': config_path,
            'readme': readme_path,
        }
    
    def _prepare_template_vars(self, 
                              platform_info: Dict[str, Any],
                              strategy: Dict[str, Any]) -> Dict[str, Any]:
        """准备模板变量"""
        
        spider_name = self._generate_spider_name(platform_info['name'])
        spider_class_name = self._generate_class_name(platform_info['name'])
        
        # 基础变量
        vars = {
            'spider_name': spider_name,
            'spider_class_name': spider_class_name,
            'platform_name': platform_info['name'],
            'platform_url': platform_info['url'],
            'spider_description': f"{platform_info['name']} 数据采集器",
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'strategy_method': strategy.get('recommended_method', 'scrapy'),
            'download_delay': 2,
            'concurrent_requests': 8,
        }
        
        # 解析URL
        from urllib.parse import urlparse
        parsed_url = urlparse(platform_info['url'])
        vars['allowed_domains'] = [parsed_url.netloc]
        vars['start_urls'] = [platform_info['url']]
        
        # 数据提取相关
        data_extraction = strategy.get('data_extraction', {})
        
        vars['list_item_selector'] = data_extraction.get('list_page_selector', 'table tbody tr')
        vars['detail_link_selector'] = data_extraction.get('detail_link_selector', 'a::attr(href)')
        
        # 字段映射
        fields = data_extraction.get('fields', {})
        vars['fields'] = fields
        
        # 提取策略描述
        vars['list_extraction_strategy'] = strategy.get('pagination_strategy', '自动提取列表项')
        vars['detail_extraction_strategy'] = strategy.get('file_download_strategy', '提取详情页所有字段')
        
        # 文件选择器
        vars['main_file_selector'] = self._guess_file_selector('pdf')
        vars['supplementary_file_selector'] = self._guess_file_selector('supplementary')
        
        # 分页代码
        vars['pagination_code'] = self._generate_pagination_code(strategy)
        
        # API相关（如果是API采集）
        if strategy.get('recommended_method') == 'api':
            vars['api_base_url'] = platform_info.get('api_base_url', platform_info['url'])
            vars['api_endpoints'] = strategy.get('api_endpoints', {'list': '/api/list'})
            vars['api_response_format'] = strategy.get('api_response_format', 'JSON')
            vars['needs_detail_api'] = strategy.get('needs_detail_api', False)
            vars['id_field'] = strategy.get('id_field', 'id')
            vars['items_per_page'] = strategy.get('items_per_page', 20)
            vars['field_mapping'] = self._generate_field_mapping(fields)
            vars['file_fields'] = strategy.get('file_fields', {
                'main_file': 'pdf_url',
                'SI_file': 'supplementary_files'
            })
        
        return vars
    
    def _generate_spider_name(self, platform_name: str) -> str:
        """生成Spider名称（snake_case）"""
        # 移除特殊字符，转换为小写，用下划线连接
        name = re.sub(r'[^\w\s-]', '', platform_name.lower())
        name = re.sub(r'[-\s]+', '_', name)
        return name
    
    def _generate_class_name(self, platform_name: str) -> str:
        """生成类名（PascalCase）"""
        # 移除特殊字符，每个单词首字母大写
        name = re.sub(r'[^\w\s]', '', platform_name)
        words = name.split()
        class_name = ''.join(word.capitalize() for word in words)
        return f"{class_name}Spider"
    
    def _guess_file_selector(self, file_type: str) -> str:
        """猜测文件选择器"""
        selectors = {
            'pdf': 'a[href$=".pdf"]::attr(href)',
            'supplementary': 'a[href*="supplement"]::attr(href), a[href*="additional"]::attr(href)',
            'attachment': 'a[href*="attachment"]::attr(href)',
        }
        return selectors.get(file_type, 'a::attr(href)')
    
    def _generate_pagination_code(self, strategy: Dict[str, Any]) -> str:
        """生成分页处理代码"""
        pagination_strategy = strategy.get('pagination_strategy', '')
        
        # 基于策略生成代码
        if 'next' in pagination_strategy.lower():
            code = """# 处理下一页
        next_page = response.css('a:has-text("Next")::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield Request(
                url=next_page,
                callback=self.parse_list,
                errback=self.handle_error,
                meta={'page': response.meta.get('page', 1) + 1}
            )"""
        elif 'page' in pagination_strategy.lower() and 'number' in pagination_strategy.lower():
            code = """# 处理页码分页
        page_links = response.css('.pagination a::attr(href)').getall()
        for link in page_links:
            if link and link not in self.visited_pages:
                self.visited_pages.add(link)
                yield Request(
                    url=response.urljoin(link),
                    callback=self.parse_list,
                    errback=self.handle_error
                )"""
        else:
            code = """# TODO: 根据实际分页机制调整
        # 示例：下一页按钮
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield Request(
                url=response.urljoin(next_page),
                callback=self.parse_list,
                errback=self.handle_error
            )"""
        
        return code
    
    def _generate_field_mapping(self, fields: Dict[str, str]) -> Dict[str, str]:
        """生成API字段映射"""
        # 如果已经是映射格式，直接返回
        if fields:
            return fields
        
        # 默认映射
        return {
            'title': 'title',
            'abstract': 'abstract',
            'authors': 'authors',
            'date': 'publication_date',
            'doi': 'doi',
        }
    
    def _generate_config(self, 
                        platform_info: Dict[str, Any],
                        strategy: Dict[str, Any],
                        output_dir: str,
                        spider_name: str) -> str:
        """生成配置文件"""
        
        config = {
            'spider_name': spider_name,
            'platform': {
                'name': platform_info['name'],
                'url': platform_info['url'],
                'type': platform_info.get('type', 'unknown'),
            },
            'strategy': {
                'method': strategy.get('recommended_method'),
                'difficulty': strategy.get('difficulty'),
                'estimated_dev_time': strategy.get('estimated_dev_time'),
            },
            'settings': {
                'download_delay': 2,
                'concurrent_requests': 8,
                'retry_times': 3,
            },
            'notes': strategy.get('special_considerations', []),
        }
        
        config_path = os.path.join(output_dir, f"{spider_name}_config.json")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"配置文件已生成: {config_path}")
        return config_path
    
    def _generate_readme(self,
                        platform_info: Dict[str, Any],
                        strategy: Dict[str, Any],
                        output_dir: str,
                        spider_name: str) -> str:
        """生成README文档"""
        
        readme_content = f"""# {platform_info['name']} Spider

## 基本信息

- **平台名称**: {platform_info['name']}
- **平台URL**: {platform_info['url']}
- **Spider名称**: {spider_name}
- **采集方法**: {strategy.get('recommended_method', 'scrapy')}
- **难度评级**: {'⭐' * strategy.get('difficulty', 3)}
- **预估开发时间**: {strategy.get('estimated_dev_time', 'N/A')}

## 采集策略

{strategy.get('pagination_strategy', 'N/A')}

## 数据字段

{self._format_fields_table(strategy.get('data_extraction', {}).get('fields', {}))}

## 文件下载

{strategy.get('file_download_strategy', 'N/A')}

## 反爬应对

{self._format_list(strategy.get('anti_scraping_handling', []))}

## 注意事项

{self._format_list(strategy.get('special_considerations', []))}

## 使用方法

```bash
# 运行Spider
scrapy crawl {spider_name}

# 限制采集数量（测试用）
scrapy crawl {spider_name} -s CLOSESPIDER_ITEMCOUNT=10

# 指定输出文件
scrapy crawl {spider_name} -o output.jsonl
```

## 输出格式

- JSONL格式: `output/{spider_name}_YYYYMMDD_HHMMSS.jsonl`
- CSV格式: `output/{spider_name}_YYYYMMDD_HHMMSS.csv`

## 文件存储结构

```
downloads/{spider_name}/
├── main_file/
│   └── {{track_id}}.pdf
├── SI_file/
│   └── {{track_id}}/
│       ├── sup_1.pdf
│       └── sup_2.xlsx
├── PR_file/
│   └── {{track_id}}/
│       └── pr_1.pdf
└── images/
    └── {{track_id}}/
        └── {{sha256}}.png
```

## 生成信息

- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **生成工具**: Spider Generator v1.0
"""
        
        readme_path = os.path.join(output_dir, f"{spider_name}_README.md")
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        logger.info(f"README已生成: {readme_path}")
        return readme_path
    
    def _format_fields_table(self, fields: Dict[str, str]) -> str:
        """格式化字段表格"""
        if not fields:
            return "暂无字段信息"
        
        table = "| 字段名 | 选择器 |\n|--------|--------|\n"
        for field, selector in fields.items():
            table += f"| {field} | `{selector}` |\n"
        
        return table
    
    def _format_list(self, items: list) -> str:
        """格式化列表"""
        if not items:
            return "无"
        
        return '\n'.join(f"- {item}" for item in items)


def generate_spider_code(platform_info: Dict[str, Any],
                        strategy: Dict[str, Any],
                        output_dir: str) -> Dict[str, str]:
    """
    便捷函数：生成Spider代码
    
    Args:
        platform_info: 平台信息
        strategy: 采集策略
        output_dir: 输出目录
        
    Returns:
        生成的文件路径字典
    """
    generator = CodeGenerator()
    return generator.generate_spider(platform_info, strategy, output_dir)


if __name__ == '__main__':
    # 测试
    test_platform = {
        'name': 'BioLINCC',
        'url': 'https://biolincc.nhlbi.nih.gov/studies/',
        'type': 'data_repository'
    }
    
    test_strategy = {
        'recommended_method': 'scrapy',
        'spider_template': 'basic_spider',
        'difficulty': 3,
        'estimated_dev_time': '4-6小时',
        'data_extraction': {
            'list_page_selector': 'table tbody tr',
            'detail_link_selector': 'a::attr(href)',
            'fields': {
                'title': 'h1::text',
                'abstract': 'div.abstract::text',
            }
        },
        'pagination_strategy': '使用Next按钮翻页',
        'file_download_strategy': '下载PDF和附件',
        'anti_scraping_handling': ['添加延迟', '使用User-Agent'],
        'special_considerations': ['注意登录要求']
    }
    
    output_dir = '/tmp/test_spider'
    files = generate_spider_code(test_platform, test_strategy, output_dir)
    
    print("生成的文件:")
    for file_type, path in files.items():
        print(f"  {file_type}: {path}")
