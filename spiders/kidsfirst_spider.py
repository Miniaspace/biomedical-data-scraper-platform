"""
Kids First Data Resource Spider

Spider for scraping data from Kids First Data Resource Center.
URL: https://kidsfirstdrc.org

This spider collects information about pediatric cancer and structural birth defect studies.
"""

import scrapy
from typing import Iterator, Dict, Any
from scrapy.http import Response, Request
import sys
from pathlib import Path
import json
import re

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.base_spider import BaseSpider


class KidsfirstSpider(BaseSpider):
    """
    Spider for Kids First Data Resource platform.
    
    Extracts:
    - Study information
    - Data modalities (WGS, RNA-Seq, WES, etc.)
    - Clinical data (phenotypes, diagnoses)
    - Genomic data availability
    - Access information
    - Publications and citations
    """
    
    name = 'kidsfirst'
    
    # Portal API (if available)
    PORTAL_URL = 'https://portal.kidsfirstdrc.org'
    
    custom_settings = {
        **BaseSpider.custom_settings,
        'DOWNLOAD_DELAY': 2,
    }
    
    def __init__(self, *args, **kwargs):
        # Platform configuration
        platform_config = {
            'name': 'Kids First Data Resource',
            'base_url': 'https://kidsfirstdrc.org',
            'start_url': 'https://kidsfirstdrc.org/resources/',
            'auth_required': False,  # Public information, but data access requires login
        }
        
        super().__init__(platform_config=platform_config, *args, **kwargs)
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse the resources page to find study links.
        
        Note: Kids First uses a modern JavaScript-based portal.
        For full data access, we would need to:
        1. Use the Portal API (requires authentication)
        2. Or use Playwright/Selenium for JavaScript rendering
        
        This implementation provides a basic scraper for public information.
        
        Args:
            response: Response from resources page
            
        Yields:
            Requests to study detail pages
        """
        self.logger.info(f"Parsing resources page: {response.url}")
        
        # Look for study links
        study_links = response.css('a[href*="/study/"]::attr(href)').getall()
        
        if not study_links:
            # Try alternative selectors
            study_links = response.css('a.study-link::attr(href)').getall()
        
        # Also look for data portal links
        portal_links = response.css('a[href*="portal.kidsfirstdrc.org"]::attr(href)').getall()
        
        self.logger.info(f"Found {len(study_links)} study links and {len(portal_links)} portal links")
        
        for link in study_links:
            study_url = response.urljoin(link)
            
            yield scrapy.Request(
                url=study_url,
                callback=self.parse_detail_page,
                errback=self.handle_error,
                meta={'platform': self.platform_name}
            )
            
            self.stats['pages_scraped'] += 1
        
        # Extract information from the current page
        yield self.parse_resources_page(response)
    
    def parse_resources_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse the main resources page for general information.
        
        Args:
            response: Response from resources page
            
        Returns:
            Dictionary with extracted data
        """
        item = self.extract_common_metadata(response)
        
        item.update({
            'page_type': 'resources_overview',
            'title': 'Kids First Data Resource - Resources Overview',
            
            # Extract data features
            'data_features': {
                'genomic': self._extract_list_items(
                    response, 
                    'div:contains("Genomic") + div li, div:contains("Genomic") ~ ul li'
                ),
                'clinical': self._extract_list_items(
                    response,
                    'div:contains("Clinical") + div li, div:contains("Clinical") ~ ul li'
                ),
            },
            
            # Extract data modalities
            'data_modalities': self._extract_list_items(
                response,
                'div:contains("Data Modalities") ~ div h4, '
                'div:contains("Data Modalities") ~ ul li'
            ),
            
            # Extract key features
            'key_features': {
                'stronger': self._extract_section_text(response, 'Stronger'),
                'faster': self._extract_section_text(response, 'Faster'),
                'greater': self._extract_section_text(response, 'Greater'),
            },
            
            # Extract FAQ information
            'faqs': self._extract_faqs(response),
            
            # Contact and access info
            'portal_url': 'https://portal.kidsfirstdrc.org',
            'dbgap_url': 'https://www.ncbi.nlm.nih.gov/gap',
            
            # Funding information
            'funding': {
                'program': 'Gabriella Miller Kids First Pediatric Research Program',
                'supported_by': 'NIH Common Fund',
                'award_number': 'U2CHL138346',
            },
        })
        
        self.stats['items_extracted'] += 1
        
        return item
    
    def parse_detail_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse study detail page.
        
        Args:
            response: Response from detail page
            
        Returns:
            Dictionary with extracted data
        """
        self.logger.info(f"Parsing detail page: {response.url}")
        
        item = self.extract_common_metadata(response)
        
        item.update({
            'page_type': 'study_detail',
            'title': self.clean_text(response.css('h1::text').get()),
            'description': self.clean_text(
                ' '.join(response.css('div.description *::text').getall())
            ),
            
            # Study information
            'study_id': self._extract_study_id(response),
            'principal_investigator': self.clean_text(
                response.css('div.pi-name::text, span.pi::text').get()
            ),
            
            # Data information
            'data_types': response.css('div.data-types span::text').getall(),
            'sample_count': self.clean_text(
                response.css('span.sample-count::text, div:contains("Samples")::text').get()
            ),
            'participant_count': self.clean_text(
                response.css('span.participant-count::text, div:contains("Participants")::text').get()
            ),
            
            # Disease/condition
            'conditions': response.css('div.conditions span::text').getall(),
            'disease_category': self.clean_text(
                response.css('span.disease-category::text').get()
            ),
            
            # Access information
            'dbgap_accession': self._extract_dbgap_accession(response),
            'access_type': self.clean_text(
                response.css('span.access-type::text').get()
            ),
            
            # Publications
            'publications': self._extract_publications(response),
        })
        
        self.stats['items_extracted'] += 1
        
        return item
    
    def _extract_list_items(self, response: Response, selector: str) -> list:
        """Extract list items using CSS selector."""
        items = []
        for item in response.css(selector):
            text = self.clean_text(' '.join(item.css('*::text').getall()))
            if text:
                items.append(text)
        return items
    
    def _extract_section_text(self, response: Response, section_title: str) -> list:
        """Extract text from a section by title."""
        items = []
        
        # Find section by title
        section = response.xpath(
            f'//h2[contains(text(), "{section_title}")]'
            f'|//h3[contains(text(), "{section_title}")]'
            f'|//div[contains(text(), "{section_title}")]'
        )
        
        if section:
            # Get following list items
            items = section.xpath(
                'following-sibling::ul[1]//li/text()|'
                'following-sibling::div[1]//li/text()'
            ).getall()
            items = [self.clean_text(item) for item in items if item.strip()]
        
        return items
    
    def _extract_faqs(self, response: Response) -> list:
        """Extract FAQ information."""
        faqs = []
        
        # Look for FAQ sections
        faq_items = response.css('div[role="button"]:contains("?"), button:contains("?")')
        
        for faq in faq_items:
            question = self.clean_text(faq.css('::text').get())
            
            # Try to get answer (might be in next sibling or hidden div)
            answer = self.clean_text(
                ' '.join(faq.xpath('following-sibling::div[1]//text()').getall())
            )
            
            if question:
                faqs.append({
                    'question': question,
                    'answer': answer if answer else 'See website for details',
                })
        
        return faqs
    
    def _extract_study_id(self, response: Response) -> str:
        """Extract study ID from page."""
        # Try to find study ID in various formats
        study_id = self.clean_text(
            response.css('span.study-id::text, div.study-id::text').get()
        )
        
        if not study_id:
            # Try to extract from URL
            match = re.search(r'/study/([^/]+)', response.url)
            if match:
                study_id = match.group(1)
        
        return study_id
    
    def _extract_dbgap_accession(self, response: Response) -> str:
        """Extract dbGaP accession number."""
        # Look for PHS accession number
        text = response.text
        match = re.search(r'(phs\d+)', text, re.IGNORECASE)
        
        if match:
            return match.group(1)
        
        return None
    
    def _extract_publications(self, response: Response) -> list:
        """Extract publication information."""
        publications = []
        
        for pub in response.css('div.publication-item, li.publication'):
            publication = {
                'title': self.clean_text(pub.css('h4::text, .pub-title::text').get()),
                'citation': self.clean_text(pub.css('.citation::text').get()),
                'doi': self.clean_text(pub.css('a[href*="doi.org"]::attr(href)').get()),
                'pmid': self.clean_text(pub.css('a[href*="pubmed"]::attr(href)').get()),
            }
            
            if publication['title'] or publication['citation']:
                publications.append(publication)
        
        return publications


if __name__ == "__main__":
    # For testing purposes
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; BiomedicalResearchBot/1.0)',
        'LOG_LEVEL': 'INFO',
    })
    
    process.crawl(KidsfirstSpider)
    process.start()
