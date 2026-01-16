#!/usr/bin/env python3
"""
Local Runner for Biomedical Data Scraper

This script allows running spiders locally without Docker/Airflow.
Perfect for development and testing.

Usage:
    python run_local.py --platform biolincc
    python run_local.py --platform all
    python run_local.py --list
"""

import sys
import argparse
import logging
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import spiders
from spiders.biolincc_spider import BiolinccSpider
from spiders.openicpsr_spider import OpenicpsrSpider
from spiders.bioportal_spider import BioportalSpider
from spiders.kidsfirst_spider import KidsfirstSpider
from spiders.nsrr_spider import NsrrSpider

# Spider registry
SPIDER_REGISTRY = {
    'biolincc': BiolinccSpider,
    'openicpsr': OpenicpsrSpider,
    'bioportal': BioportalSpider,
    'kidsfirst': KidsfirstSpider,
    'nsrr': NsrrSpider,
}


def setup_logging(level=logging.INFO):
    """Setup logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def load_platform_config():
    """Load platform configurations."""
    config_file = Path('config/platforms.yaml')
    if config_file.exists():
        with open(config_file, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}


def list_platforms():
    """List all available platforms."""
    platforms = load_platform_config()
    
    print("\n=== Available Platforms ===\n")
    print(f"{'Platform':<20} {'Name':<30} {'Status':<10} {'Auth':<10}")
    print("-" * 70)
    
    for platform_id, config in platforms.items():
        name = config.get('name', platform_id)
        enabled = "Enabled" if config.get('enabled', False) else "Disabled"
        auth = "Yes" if config.get('auth_required', False) else "No"
        
        # Check if spider is implemented
        if platform_id in SPIDER_REGISTRY:
            print(f"{platform_id:<20} {name:<30} {enabled:<10} {auth:<10}")
        else:
            print(f"{platform_id:<20} {name:<30} {'Not Impl':<10} {auth:<10}")
    
    print("\n")


def run_spider(spider_name, **kwargs):
    """
    Run a single spider.
    
    Args:
        spider_name: Name of the spider to run
        **kwargs: Additional arguments to pass to spider
    """
    if spider_name not in SPIDER_REGISTRY:
        print(f"Error: Spider '{spider_name}' not found or not implemented yet.")
        print(f"Available spiders: {', '.join(SPIDER_REGISTRY.keys())}")
        return False
    
    spider_class = SPIDER_REGISTRY[spider_name]
    
    # Configure Scrapy settings
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (compatible; BiomedicalResearchBot/1.0)',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': True,
        'TELNETCONSOLE_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        
        # Enable pipeline
        'ITEM_PIPELINES': {
            'common.pipeline.data_pipeline.ScrapyPipeline': 300,
        },
        
        # Output settings
        'FEEDS': {
            f'data/raw/{spider_name}/%(name)s_%(time)s.jsonl': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'store_empty': False,
                'overwrite': False,
            },
        },
    }
    
    # Create output directory
    output_dir = Path(f'data/raw/{spider_name}')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create and configure crawler
    process = CrawlerProcess(settings)
    
    print(f"\n=== Starting spider: {spider_name} ===\n")
    
    try:
        process.crawl(spider_class, **kwargs)
        process.start()
        
        print(f"\n=== Spider completed: {spider_name} ===\n")
        print(f"Output directory: {output_dir.absolute()}")
        
        return True
        
    except Exception as e:
        print(f"\n=== Spider failed: {spider_name} ===")
        print(f"Error: {e}")
        return False


def run_all_spiders():
    """Run all enabled spiders sequentially."""
    platforms = load_platform_config()
    
    enabled_platforms = [
        platform_id for platform_id, config in platforms.items()
        if config.get('enabled', False) and platform_id in SPIDER_REGISTRY
    ]
    
    if not enabled_platforms:
        print("No enabled platforms found.")
        return
    
    print(f"\n=== Running {len(enabled_platforms)} enabled spiders ===\n")
    
    results = {}
    for platform_id in enabled_platforms:
        success = run_spider(platform_id)
        results[platform_id] = success
    
    # Print summary
    print("\n=== Summary ===\n")
    for platform_id, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"{platform_id:<20} {status}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Run biomedical data scrapers locally'
    )
    
    parser.add_argument(
        '--platform',
        type=str,
        help='Platform to scrape (or "all" for all enabled platforms)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available platforms'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    
    # Handle list command
    if args.list:
        list_platforms()
        return
    
    # Handle platform command
    if args.platform:
        if args.platform.lower() == 'all':
            run_all_spiders()
        else:
            run_spider(args.platform.lower())
        return
    
    # No command specified, show help
    parser.print_help()


if __name__ == '__main__':
    main()
