"""
Base Spider Template for All Platform Adapters

This module provides a base class that handles all common scraping logic,
including authentication, rate limiting, error handling, and logging.
Platform-specific spiders only need to implement parse methods.
"""

import scrapy
import logging
from typing import Dict, Any, Optional, Iterator
from scrapy.http import Response, Request
from scrapy.exceptions import CloseSpider
import time
import hashlib
import json
from datetime import datetime


class BaseSpider(scrapy.Spider):
    """
    Base spider class with common functionality for all platform adapters.
    
    Attributes:
        platform_name: Name of the platform (e.g., 'biolincc')
        base_url: Base URL of the target platform
        auth_required: Whether authentication is required
        rate_limit: Delay between requests in seconds
        max_retries: Maximum number of retries for failed requests
    """
    
    # Default settings (can be overridden by subclasses)
    custom_settings = {
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
        'HTTPERROR_ALLOWED_CODES': [403, 404],
        'COOKIES_ENABLED': True,
        'TELNETCONSOLE_ENABLED': False,
        'LOG_LEVEL': 'INFO',
    }
    
    def __init__(self, platform_config: Optional[Dict[str, Any]] = None, 
                 credentials: Optional[Dict[str, str]] = None, 
                 *args, **kwargs):
        """
        Initialize the spider with platform configuration and credentials.
        
        Args:
            platform_config: Configuration dict for the platform
            credentials: Authentication credentials dict
        """
        super().__init__(*args, **kwargs)
        
        self.platform_config = platform_config or {}
        self.credentials = credentials or {}
        self.platform_name = self.name
        self.base_url = self.platform_config.get('base_url', '')
        self.auth_required = self.platform_config.get('auth_required', False)
        
        # Statistics
        self.stats = {
            'start_time': datetime.now(),
            'pages_scraped': 0,
            'items_extracted': 0,
            'errors': 0,
        }
        
        # Note: Scrapy Spider already has a logger property
        # We can use self.logger directly without reassigning
    
    def start_requests(self) -> Iterator[Request]:
        """
        Generate initial requests. Handles authentication if required.
        
        Yields:
            Initial scrapy requests
        """
        if self.auth_required:
            # First, perform authentication
            yield self.create_login_request()
        else:
            # Directly start scraping
            start_url = self.platform_config.get('start_url', self.base_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_list_page,
                errback=self.handle_error,
                meta={'platform': self.platform_name}
            )
    
    def create_login_request(self) -> Request:
        """
        Create a login request. Should be overridden by subclasses if needed.
        
        Returns:
            Login request
        """
        login_url = self.platform_config.get('login_url', f"{self.base_url}/login")
        
        return scrapy.FormRequest(
            url=login_url,
            formdata={
                'username': self.credentials.get('username', ''),
                'password': self.credentials.get('password', ''),
            },
            callback=self.after_login,
            errback=self.handle_error,
            meta={'platform': self.platform_name}
        )
    
    def after_login(self, response: Response) -> Iterator[Request]:
        """
        Handle response after login. Check if login was successful.
        
        Args:
            response: Response from login request
            
        Yields:
            Requests to start scraping
        """
        if self.check_login_success(response):
            self.logger.info(f"Login successful for {self.platform_name}")
            start_url = self.platform_config.get('start_url', self.base_url)
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_list_page,
                errback=self.handle_error,
                meta={'platform': self.platform_name}
            )
        else:
            self.logger.error(f"Login failed for {self.platform_name}")
            raise CloseSpider(f"Authentication failed for {self.platform_name}")
    
    def check_login_success(self, response: Response) -> bool:
        """
        Check if login was successful. Should be overridden by subclasses.
        
        Args:
            response: Response from login request
            
        Returns:
            True if login successful, False otherwise
        """
        # Default implementation: check for common success indicators
        return (
            response.status == 200 and
            'logout' in response.text.lower() or
            'dashboard' in response.text.lower()
        )
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse list/index pages to extract detail page URLs.
        MUST be implemented by subclasses.
        
        Args:
            response: Response from list page
            
        Yields:
            Requests to detail pages
        """
        raise NotImplementedError("Subclasses must implement parse_list_page()")
    
    def parse_detail_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse detail pages to extract target data.
        MUST be implemented by subclasses.
        
        Args:
            response: Response from detail page
            
        Returns:
            Extracted data as dictionary
        """
        raise NotImplementedError("Subclasses must implement parse_detail_page()")
    
    def extract_common_metadata(self, response: Response) -> Dict[str, Any]:
        """
        Extract common metadata fields present in all platforms.
        
        Args:
            response: Response object
            
        Returns:
            Dictionary with common metadata
        """
        return {
            'platform': self.platform_name,
            'source_url': response.url,
            'scraped_at': datetime.now().isoformat(),
            'response_status': response.status,
            'track_id': self.generate_track_id(response.url),
        }
    
    def generate_track_id(self, url: str) -> str:
        """
        Generate a unique track ID for a URL.
        
        Args:
            url: Source URL
            
        Returns:
            Unique track ID (UUID-like string)
        """
        hash_object = hashlib.md5(url.encode())
        return hash_object.hexdigest()
    
    def clean_text(self, text: Optional[str]) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters if needed
        # text = re.sub(r'[^\w\s\-.,;:!?()]', '', text)
        
        return text.strip()
    
    def handle_error(self, failure):
        """
        Handle request errors and failures.
        
        Args:
            failure: Twisted Failure object
        """
        self.stats['errors'] += 1
        self.logger.error(f"Request failed: {failure.request.url}")
        self.logger.error(f"Error: {failure.value}")
    
    def closed(self, reason: str):
        """
        Called when spider is closed. Log final statistics.
        
        Args:
            reason: Reason for closing
        """
        self.stats['end_time'] = datetime.now()
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        self.logger.info(f"Spider closed: {reason}")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Pages scraped: {self.stats['pages_scraped']}")
        self.logger.info(f"Items extracted: {self.stats['items_extracted']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        
        # Save statistics to file
        stats_file = f"data/logs/{self.platform_name}_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump({
                    **self.stats,
                    'start_time': self.stats['start_time'].isoformat(),
                    'end_time': self.stats['end_time'].isoformat(),
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save statistics: {e}")
