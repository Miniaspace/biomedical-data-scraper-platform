"""
OpenICPSR Spider

Spider for scraping data from OpenICPSR (Open Inter-university Consortium for Political and Social Research).
URL: https://www.openicpsr.org/

This serves as another example implementation showing authentication handling.
"""

import scrapy
from typing import Iterator, Dict, Any
from scrapy.http import Response, Request
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.base_spider import BaseSpider


class OpenicpsrSpider(BaseSpider):
    """
    Spider for OpenICPSR platform.
    
    Extracts:
    - Project title and abstract
    - Authors and affiliations
    - Data files and documentation
    - Subject terms and keywords
    - Geographic coverage
    - Temporal coverage
    - Related publications
    """
    
    name = 'openicpsr'
    
    custom_settings = {
        **BaseSpider.custom_settings,
        'DOWNLOAD_DELAY': 2,
    }
    
    def __init__(self, *args, **kwargs):
        # Platform configuration
        platform_config = {
            'name': 'OpenICPSR',
            'base_url': 'https://www.openicpsr.org',
            'start_url': 'https://www.openicpsr.org/openicpsr/search/studies',
            'login_url': 'https://www.openicpsr.org/openicpsr/login',
            'auth_required': True,  # Some datasets require authentication
        }
        
        # Get credentials from environment or config
        credentials = kwargs.get('credentials', {})
        
        super().__init__(
            platform_config=platform_config,
            credentials=credentials,
            *args,
            **kwargs
        )
    
    def check_login_success(self, response: Response) -> bool:
        """
        Check if login was successful.
        
        Args:
            response: Response from login request
            
        Returns:
            True if login successful
        """
        # Check for user menu or logout link
        return (
            response.css('a.logout-link').get() is not None or
            response.css('div.user-menu').get() is not None
        )
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse search results page to extract project URLs.
        
        Args:
            response: Response from search page
            
        Yields:
            Requests to project detail pages
        """
        self.logger.info(f"Parsing list page: {response.url}")
        
        # Extract project links from search results
        project_links = response.css('div.search-result h3 a::attr(href)').getall()
        
        if not project_links:
            # Try alternative selector
            project_links = response.css('a.project-link::attr(href)').getall()
        
        self.logger.info(f"Found {len(project_links)} project links")
        
        for link in project_links:
            project_url = response.urljoin(link)
            
            yield scrapy.Request(
                url=project_url,
                callback=self.parse_detail_page,
                errback=self.handle_error,
                meta={'platform': self.platform_name}
            )
            
            self.stats['pages_scraped'] += 1
        
        # Handle pagination
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_list_page,
                errback=self.handle_error
            )
    
    def parse_detail_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse project detail page to extract all information.
        
        Args:
            response: Response from detail page
            
        Returns:
            Dictionary with extracted data
        """
        self.logger.info(f"Parsing detail page: {response.url}")
        
        # Extract common metadata
        item = self.extract_common_metadata(response)
        
        # Extract project-specific fields
        item.update({
            # Basic information
            'title': self.clean_text(response.css('h1.project-title::text').get()),
            'project_id': self.clean_text(response.css('span.project-id::text').get()),
            'doi': self.clean_text(response.css('span.doi::text').get()),
            
            # Abstract and description
            'abstract': self.clean_text(
                ' '.join(response.css('div.abstract *::text').getall())
            ),
            'methodology': self.clean_text(
                ' '.join(response.css('div.methodology *::text').getall())
            ),
            
            # Authors
            'authors': self._extract_authors(response),
            
            # Subject classification
            'subject_terms': response.css('div.subject-terms span::text').getall(),
            'keywords': response.css('div.keywords span::text').getall(),
            
            # Coverage
            'geographic_coverage': response.css('div.geo-coverage span::text').getall(),
            'temporal_coverage': {
                'start': self.clean_text(response.css('span.time-start::text').get()),
                'end': self.clean_text(response.css('span.time-end::text').get()),
            },
            'unit_of_analysis': self.clean_text(
                response.css('span.unit-analysis::text').get()
            ),
            
            # Data information
            'data_collection_dates': {
                'start': self.clean_text(response.css('span.collection-start::text').get()),
                'end': self.clean_text(response.css('span.collection-end::text').get()),
            },
            'data_type': self.clean_text(response.css('span.data-type::text').get()),
            'data_format': response.css('div.data-format span::text').getall(),
            
            # Files
            'data_files': self._extract_data_files(response),
            'documentation_files': self._extract_documentation_files(response),
            
            # Related materials
            'related_publications': self._extract_publications(response),
            'related_datasets': response.css('div.related-datasets a::attr(href)').getall(),
            
            # Access information
            'access_type': self.clean_text(response.css('span.access-type::text').get()),
            'license': self.clean_text(response.css('span.license::text').get()),
            'restrictions': self.clean_text(
                ' '.join(response.css('div.restrictions *::text').getall())
            ),
            
            # Funding
            'funding_agency': response.css('div.funding span.agency::text').getall(),
            'grant_number': response.css('div.funding span.grant::text').getall(),
            
            # Dates
            'deposit_date': self.clean_text(response.css('span.deposit-date::text').get()),
            'publication_date': self.clean_text(
                response.css('span.publication-date::text').get()
            ),
            'last_updated': self.clean_text(response.css('span.last-updated::text').get()),
        })
        
        self.stats['items_extracted'] += 1
        
        return item
    
    def _extract_authors(self, response: Response) -> list:
        """Extract author information."""
        authors = []
        
        for author in response.css('div.author-item'):
            author_info = {
                'name': self.clean_text(author.css('span.author-name::text').get()),
                'affiliation': self.clean_text(author.css('span.affiliation::text').get()),
                'orcid': self.clean_text(author.css('a.orcid::attr(href)').get()),
            }
            authors.append(author_info)
        
        return authors
    
    def _extract_data_files(self, response: Response) -> list:
        """Extract data file information."""
        files = []
        
        for file_item in response.css('div.data-file-item'):
            file_info = {
                'filename': self.clean_text(file_item.css('span.filename::text').get()),
                'size': self.clean_text(file_item.css('span.filesize::text').get()),
                'format': self.clean_text(file_item.css('span.format::text').get()),
                'description': self.clean_text(file_item.css('div.description::text').get()),
                'download_url': file_item.css('a.download::attr(href)').get(),
            }
            files.append(file_info)
        
        return files
    
    def _extract_documentation_files(self, response: Response) -> list:
        """Extract documentation file information."""
        docs = []
        
        for doc_item in response.css('div.doc-file-item'):
            doc_info = {
                'filename': self.clean_text(doc_item.css('span.filename::text').get()),
                'type': self.clean_text(doc_item.css('span.doc-type::text').get()),
                'download_url': doc_item.css('a.download::attr(href)').get(),
            }
            docs.append(doc_info)
        
        return docs
    
    def _extract_publications(self, response: Response) -> list:
        """Extract related publication information."""
        publications = []
        
        for pub in response.css('div.publication-item'):
            publication = {
                'citation': self.clean_text(pub.css('div.citation::text').get()),
                'doi': self.clean_text(pub.css('a.doi::attr(href)').get()),
                'url': self.clean_text(pub.css('a.pub-url::attr(href)').get()),
            }
            publications.append(publication)
        
        return publications


if __name__ == "__main__":
    # For testing purposes
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; BiomedicalResearchBot/1.0)',
        'LOG_LEVEL': 'INFO',
    })
    
    process.crawl(OpenicpsrSpider)
    process.start()
