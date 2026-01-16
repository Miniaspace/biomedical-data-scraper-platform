"""
BioLINCC Spider

Spider for scraping data from BioLINCC (Biologic Specimen and Data Repository Information Coordinating Center).
URL: https://biolincc.nhlbi.nih.gov/

This serves as an example implementation of a platform adapter.
"""

import scrapy
from typing import Iterator, Dict, Any
from scrapy.http import Response, Request
import sys
from pathlib import Path

# Add parent directory to path to import common modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from common.base_spider import BaseSpider


class BiolinccSpider(BaseSpider):
    """
    Spider for BioLINCC platform.
    
    Extracts:
    - Study title and description
    - Principal investigators
    - Study design and objectives
    - Data availability
    - Publications
    - Contact information
    """
    
    name = 'biolincc'
    
    custom_settings = {
        **BaseSpider.custom_settings,
        'DOWNLOAD_DELAY': 3,  # Be respectful to government servers
    }
    
    def __init__(self, *args, **kwargs):
        # Platform configuration
        platform_config = {
            'name': 'BioLINCC',
            'base_url': 'https://biolincc.nhlbi.nih.gov',
            'start_url': 'https://biolincc.nhlbi.nih.gov/studies/',
            'auth_required': False,
        }
        
        super().__init__(platform_config=platform_config, *args, **kwargs)
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse the studies list page to extract study detail URLs.
        
        Args:
            response: Response from list page
            
        Yields:
            Requests to study detail pages
        """
        self.logger.info(f"Parsing list page: {response.url}")
        
        # Extract study links
        # BioLINCC uses a table format with study links
        study_links = response.css('table.studies-table tr td a::attr(href)').getall()
        
        if not study_links:
            # Fallback: try alternative selectors
            study_links = response.css('div.study-item a::attr(href)').getall()
        
        self.logger.info(f"Found {len(study_links)} study links")
        
        for link in study_links:
            # Make absolute URL
            study_url = response.urljoin(link)
            
            yield scrapy.Request(
                url=study_url,
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
        Parse study detail page to extract all relevant information.
        
        Args:
            response: Response from detail page
            
        Returns:
            Dictionary with extracted data
        """
        self.logger.info(f"Parsing detail page: {response.url}")
        
        # Extract common metadata
        item = self.extract_common_metadata(response)
        
        # Extract study-specific fields
        item.update({
            # Basic information
            'title': self.clean_text(response.css('h1.study-title::text').get()),
            'study_id': self.clean_text(response.css('div.study-id::text').get()),
            'acronym': self.clean_text(response.css('div.acronym::text').get()),
            
            # Description
            'description': self.clean_text(
                ' '.join(response.css('div.study-description *::text').getall())
            ),
            'objectives': self.clean_text(
                ' '.join(response.css('div.objectives *::text').getall())
            ),
            
            # Study design
            'study_type': self.clean_text(response.css('div.study-type::text').get()),
            'study_design': self.clean_text(response.css('div.study-design::text').get()),
            'condition': response.css('div.condition span::text').getall(),
            'intervention': response.css('div.intervention span::text').getall(),
            
            # Investigators
            'principal_investigator': self.clean_text(
                response.css('div.pi-name::text').get()
            ),
            'investigators': response.css('div.investigators li::text').getall(),
            
            # Dates
            'start_date': self.clean_text(response.css('span.start-date::text').get()),
            'end_date': self.clean_text(response.css('span.end-date::text').get()),
            
            # Participants
            'enrollment': self.clean_text(response.css('span.enrollment::text').get()),
            'age_range': self.clean_text(response.css('span.age-range::text').get()),
            'gender': self.clean_text(response.css('span.gender::text').get()),
            
            # Data availability
            'data_available': self.clean_text(
                response.css('div.data-availability::text').get()
            ),
            'access_criteria': self.clean_text(
                ' '.join(response.css('div.access-criteria *::text').getall())
            ),
            
            # Publications
            'publications': self._extract_publications(response),
            
            # Contact
            'contact_email': self.clean_text(
                response.css('a.contact-email::attr(href)').get()
            ),
            'contact_phone': self.clean_text(response.css('span.contact-phone::text').get()),
            
            # Additional metadata
            'keywords': response.css('div.keywords span::text').getall(),
            'sponsor': self.clean_text(response.css('div.sponsor::text').get()),
        })
        
        self.stats['items_extracted'] += 1
        
        return item
    
    def _extract_publications(self, response: Response) -> list:
        """
        Extract publication information.
        
        Args:
            response: Response object
            
        Returns:
            List of publication dictionaries
        """
        publications = []
        
        for pub in response.css('div.publication-item'):
            publication = {
                'title': self.clean_text(pub.css('h4.pub-title::text').get()),
                'authors': self.clean_text(pub.css('div.pub-authors::text').get()),
                'journal': self.clean_text(pub.css('span.pub-journal::text').get()),
                'year': self.clean_text(pub.css('span.pub-year::text').get()),
                'pmid': self.clean_text(pub.css('span.pmid::text').get()),
                'doi': self.clean_text(pub.css('a.doi::attr(href)').get()),
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
    
    process.crawl(BiolinccSpider)
    process.start()
