#!/usr/bin/env python3
"""
Add New Platform Script

This script helps quickly scaffold a new platform adapter.
It creates the spider file and updates configuration files.

Usage:
    python scripts/add_platform.py <platform_name>
"""

import sys
import yaml
from pathlib import Path
from datetime import datetime


SPIDER_TEMPLATE = '''"""
{platform_title} Spider

Spider for scraping data from {platform_title}.
URL: {base_url}

Auto-generated on {date}
"""

import scrapy
from typing import Iterator, Dict, Any
from scrapy.http import Response, Request
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.base_spider import BaseSpider


class {spider_class}(BaseSpider):
    """
    Spider for {platform_title} platform.
    
    TODO: Document what data this spider extracts
    """
    
    name = '{platform_name}'
    
    custom_settings = {{
        **BaseSpider.custom_settings,
        'DOWNLOAD_DELAY': 2,
    }}
    
    def __init__(self, *args, **kwargs):
        # Platform configuration
        platform_config = {{
            'name': '{platform_title}',
            'base_url': '{base_url}',
            'start_url': '{start_url}',
            'auth_required': {auth_required},
        }}
        
        super().__init__(platform_config=platform_config, *args, **kwargs)
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse list/index pages to extract detail page URLs.
        
        TODO: Implement list page parsing logic
        
        Args:
            response: Response from list page
            
        Yields:
            Requests to detail pages
        """
        self.logger.info(f"Parsing list page: {{response.url}}")
        
        # TODO: Extract links to detail pages
        # Example:
        # detail_links = response.css('a.detail-link::attr(href)').getall()
        # for link in detail_links:
        #     yield scrapy.Request(
        #         url=response.urljoin(link),
        #         callback=self.parse_detail_page,
        #         errback=self.handle_error
        #     )
        
        raise NotImplementedError("parse_list_page() must be implemented")
    
    def parse_detail_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse detail pages to extract target data.
        
        TODO: Implement detail page parsing logic
        
        Args:
            response: Response from detail page
            
        Returns:
            Dictionary with extracted data
        """
        self.logger.info(f"Parsing detail page: {{response.url}}")
        
        # Extract common metadata
        item = self.extract_common_metadata(response)
        
        # TODO: Extract platform-specific fields
        # Example:
        # item.update({{
        #     'title': self.clean_text(response.css('h1::text').get()),
        #     'description': self.clean_text(response.css('div.description::text').get()),
        #     # Add more fields...
        # }})
        
        raise NotImplementedError("parse_detail_page() must be implemented")
        
        return item


if __name__ == "__main__":
    # For testing purposes
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess({{
        'USER_AGENT': 'Mozilla/5.0 (compatible; BiomedicalResearchBot/1.0)',
        'LOG_LEVEL': 'INFO',
    }})
    
    process.crawl({spider_class})
    process.start()
'''


def create_spider_file(platform_name: str, config: dict):
    """Create spider file from template."""
    spider_dir = Path('spiders')
    spider_dir.mkdir(exist_ok=True)
    
    spider_file = spider_dir / f"{platform_name}_spider.py"
    
    if spider_file.exists():
        print(f"Warning: Spider file already exists: {spider_file}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return False
    
    # Generate spider class name
    spider_class = ''.join(word.capitalize() for word in platform_name.split('_')) + 'Spider'
    
    # Fill template
    content = SPIDER_TEMPLATE.format(
        platform_name=platform_name,
        platform_title=config.get('name', platform_name.title()),
        base_url=config.get('base_url', 'https://example.com'),
        start_url=config.get('start_url', config.get('base_url', 'https://example.com')),
        auth_required=config.get('auth_required', False),
        spider_class=spider_class,
        date=datetime.now().strftime('%Y-%m-%d')
    )
    
    with open(spider_file, 'w') as f:
        f.write(content)
    
    print(f"✓ Created spider file: {spider_file}")
    return True


def update_platforms_config(platform_name: str, config: dict):
    """Add platform to platforms.yaml."""
    config_file = Path('config/platforms.yaml')
    
    # Load existing config
    if config_file.exists():
        with open(config_file, 'r') as f:
            platforms = yaml.safe_load(f) or {}
    else:
        platforms = {}
    
    if platform_name in platforms:
        print(f"Warning: Platform already exists in config: {platform_name}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Skipped config update.")
            return False
    
    # Add new platform
    platforms[platform_name] = config
    
    # Save config
    with open(config_file, 'w') as f:
        yaml.dump(platforms, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Updated platforms config: {config_file}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/add_platform.py <platform_name>")
        print("\nExample:")
        print("  python scripts/add_platform.py new_platform")
        sys.exit(1)
    
    platform_name = sys.argv[1].lower().replace('-', '_')
    
    print(f"\n=== Adding new platform: {platform_name} ===\n")
    
    # Gather configuration
    print("Please provide the following information:")
    display_name = input(f"Display name [{platform_name.title()}]: ") or platform_name.title()
    base_url = input("Base URL (e.g., https://example.com): ")
    start_url = input(f"Start URL [{base_url}]: ") or base_url
    
    auth_input = input("Requires authentication? (y/n) [n]: ").lower()
    auth_required = auth_input == 'y'
    
    schedule = input("Cron schedule [0 2 * * *]: ") or "0 2 * * *"
    priority = input("Priority (1-10) [5]: ") or "5"
    description = input("Description: ")
    
    # Build configuration
    config = {
        'name': display_name,
        'base_url': base_url,
        'start_url': start_url,
        'spider_class': ''.join(word.capitalize() for word in platform_name.split('_')) + 'Spider',
        'schedule': schedule,
        'enabled': False,  # Disabled by default until implemented
        'auth_required': auth_required,
        'priority': int(priority),
        'description': description,
    }
    
    print("\n=== Configuration ===")
    print(yaml.dump({platform_name: config}, default_flow_style=False))
    
    confirm = input("\nProceed? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        sys.exit(0)
    
    # Create files
    print("\n=== Creating files ===\n")
    
    spider_created = create_spider_file(platform_name, config)
    config_updated = update_platforms_config(platform_name, config)
    
    if spider_created and config_updated:
        print("\n✓ Platform added successfully!")
        print("\nNext steps:")
        print(f"1. Implement parsing logic in spiders/{platform_name}_spider.py")
        print(f"2. Add credentials to config/credentials.yaml (if auth required)")
        print(f"3. Test the spider: scrapy runspider spiders/{platform_name}_spider.py")
        print(f"4. Enable in config/platforms.yaml: enabled: true")
        print(f"5. Restart Airflow to load the new DAG")
    else:
        print("\n⚠ Platform addition incomplete. Please check errors above.")


if __name__ == "__main__":
    main()
