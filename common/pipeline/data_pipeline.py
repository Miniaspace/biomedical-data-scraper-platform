"""
Data Processing Pipeline

Handles data validation, transformation, deduplication, and storage.
"""

import json
import logging
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd


class DataPipeline:
    """
    Pipeline for processing scraped data.
    
    Stages:
    1. Validation - Check data quality and completeness
    2. Transformation - Normalize and enrich data
    3. Deduplication - Remove duplicate records
    4. Storage - Save to appropriate storage backend
    """
    
    def __init__(self, output_dir: str = "data/raw"):
        """
        Initialize the data pipeline.
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger('data_pipeline')
        self.processed_ids = set()  # For deduplication
        
        # Statistics
        self.stats = {
            'total_items': 0,
            'valid_items': 0,
            'invalid_items': 0,
            'duplicate_items': 0,
            'saved_items': 0,
        }
    
    def process_item(self, item: Dict[str, Any], spider) -> Optional[Dict[str, Any]]:
        """
        Process a single scraped item through the pipeline.
        
        Args:
            item: Scraped item dictionary
            spider: Spider instance
            
        Returns:
            Processed item or None if invalid/duplicate
        """
        self.stats['total_items'] += 1
        
        # Stage 1: Validation
        if not self.validate_item(item):
            self.stats['invalid_items'] += 1
            self.logger.warning(f"Invalid item from {spider.name}: {item.get('source_url', 'unknown')}")
            return None
        
        self.stats['valid_items'] += 1
        
        # Stage 2: Transformation
        item = self.transform_item(item)
        
        # Stage 3: Deduplication
        if self.is_duplicate(item):
            self.stats['duplicate_items'] += 1
            self.logger.debug(f"Duplicate item: {item.get('track_id')}")
            return None
        
        # Stage 4: Storage
        self.save_item(item, spider.name)
        self.stats['saved_items'] += 1
        
        return item
    
    def validate_item(self, item: Dict[str, Any]) -> bool:
        """
        Validate item data quality.
        
        Args:
            item: Item dictionary
            
        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        required_fields = ['platform', 'source_url', 'track_id']
        
        for field in required_fields:
            if field not in item or not item[field]:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Check URL format
        if not item['source_url'].startswith('http'):
            self.logger.error(f"Invalid URL format: {item['source_url']}")
            return False
        
        # Additional platform-specific validation can be added here
        
        return True
    
    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform and enrich item data.
        
        Args:
            item: Raw item dictionary
            
        Returns:
            Transformed item dictionary
        """
        # Add processing timestamp
        item['processed_at'] = datetime.now().isoformat()
        
        # Normalize text fields
        text_fields = ['title', 'description', 'abstract']
        for field in text_fields:
            if field in item and item[field]:
                item[field] = self._normalize_text(item[field])
        
        # Add data quality score
        item['quality_score'] = self._calculate_quality_score(item)
        
        return item
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text content.
        
        Args:
            text: Raw text
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
        
        return text.strip()
    
    def _calculate_quality_score(self, item: Dict[str, Any]) -> float:
        """
        Calculate data quality score (0-1).
        
        Args:
            item: Item dictionary
            
        Returns:
            Quality score
        """
        score = 0.0
        max_score = 0.0
        
        # Check completeness of important fields
        important_fields = {
            'title': 0.3,
            'description': 0.2,
            'authors': 0.1,
            'publication_date': 0.1,
            'keywords': 0.1,
            'abstract': 0.2,
        }
        
        for field, weight in important_fields.items():
            max_score += weight
            if field in item and item[field]:
                # Check if field has substantial content
                if isinstance(item[field], str) and len(item[field]) > 10:
                    score += weight
                elif isinstance(item[field], (list, dict)) and item[field]:
                    score += weight
        
        return round(score / max_score if max_score > 0 else 0.0, 2)
    
    def is_duplicate(self, item: Dict[str, Any]) -> bool:
        """
        Check if item is a duplicate.
        
        Args:
            item: Item dictionary
            
        Returns:
            True if duplicate, False otherwise
        """
        track_id = item.get('track_id')
        
        if track_id in self.processed_ids:
            return True
        
        self.processed_ids.add(track_id)
        return False
    
    def save_item(self, item: Dict[str, Any], platform: str):
        """
        Save item to storage.
        
        Args:
            item: Item dictionary
            platform: Platform name
        """
        # Create platform-specific directory
        platform_dir = self.output_dir / platform
        platform_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as JSONL (one JSON object per line)
        jsonl_file = platform_dir / f"{platform}_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        try:
            with open(jsonl_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
            self.logger.debug(f"Saved item to {jsonl_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save item: {e}")
            raise
    
    def export_to_csv(self, platform: str, date: Optional[str] = None):
        """
        Export platform data to CSV format.
        
        Args:
            platform: Platform name
            date: Date string (YYYYMMDD), defaults to today
        """
        if not date:
            date = datetime.now().strftime('%Y%m%d')
        
        platform_dir = self.output_dir / platform
        jsonl_file = platform_dir / f"{platform}_{date}.jsonl"
        
        if not jsonl_file.exists():
            self.logger.warning(f"No data file found: {jsonl_file}")
            return
        
        try:
            # Read JSONL file
            data = []
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    data.append(json.loads(line))
            
            # Convert to DataFrame and save as CSV
            df = pd.DataFrame(data)
            csv_file = platform_dir / f"{platform}_{date}.csv"
            df.to_csv(csv_file, index=False, encoding='utf-8')
            
            self.logger.info(f"Exported {len(data)} items to {csv_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to export to CSV: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get pipeline statistics.
        
        Returns:
            Statistics dictionary
        """
        return self.stats.copy()
    
    def reset_statistics(self):
        """Reset pipeline statistics."""
        self.stats = {
            'total_items': 0,
            'valid_items': 0,
            'invalid_items': 0,
            'duplicate_items': 0,
            'saved_items': 0,
        }
        self.processed_ids.clear()


class ScrapyPipeline:
    """
    Scrapy pipeline adapter for DataPipeline.
    
    This class integrates DataPipeline with Scrapy's pipeline system.
    """
    
    def __init__(self):
        self.pipeline = None
    
    def open_spider(self, spider):
        """Called when spider is opened."""
        self.pipeline = DataPipeline()
        spider.logger.info("Data pipeline opened")
    
    def close_spider(self, spider):
        """Called when spider is closed."""
        stats = self.pipeline.get_statistics()
        spider.logger.info(f"Pipeline statistics: {stats}")
        
        # Export to CSV
        try:
            self.pipeline.export_to_csv(spider.name)
        except Exception as e:
            spider.logger.error(f"Failed to export CSV: {e}")
    
    def process_item(self, item, spider):
        """Process item through pipeline."""
        result = self.pipeline.process_item(dict(item), spider)
        
        if result is None:
            # Item was filtered out
            from scrapy.exceptions import DropItem
            raise DropItem("Item filtered by pipeline")
        
        return result
