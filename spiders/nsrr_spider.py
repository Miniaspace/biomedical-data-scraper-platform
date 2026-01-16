"""
National Sleep Research Resource (NSRR) Spider

Spider for scraping data from National Sleep Research Resource.
URL: https://sleepdata.org

Note: As of implementation date, the website was experiencing technical issues (502 error).
This spider provides the framework and will need to be tested once the site is back online.
"""

import scrapy
from typing import Iterator, Dict, Any
from scrapy.http import Response, Request
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.base_spider import BaseSpider


class NsrrSpider(BaseSpider):
    """
    Spider for National Sleep Research Resource platform.
    
    Extracts:
    - Sleep study datasets
    - Study descriptions and protocols
    - Data collection methods
    - Participant demographics
    - Available data files
    - Publications
    - Access requirements
    """
    
    name = 'nsrr'
    
    custom_settings = {
        **BaseSpider.custom_settings,
        'DOWNLOAD_DELAY': 2,
    }
    
    def __init__(self, *args, **kwargs):
        # Platform configuration
        platform_config = {
            'name': 'National Sleep Research Resource',
            'base_url': 'https://sleepdata.org',
            'start_url': 'https://sleepdata.org/datasets',
            'auth_required': False,  # Public data, but download may require registration
        }
        
        super().__init__(platform_config=platform_config, *args, **kwargs)
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse the datasets list page.
        
        Args:
            response: Response from list page
            
        Yields:
            Requests to dataset detail pages
        """
        self.logger.info(f"Parsing list page: {response.url}")
        
        # Extract dataset links
        # Note: Actual selectors need to be verified once site is accessible
        dataset_links = response.css('div.dataset-item a::attr(href), '
                                    'table.datasets tr td a::attr(href)').getall()
        
        if not dataset_links:
            # Try alternative selectors
            dataset_links = response.css('a[href*="/datasets/"]::attr(href)').getall()
        
        self.logger.info(f"Found {len(dataset_links)} dataset links")
        
        for link in dataset_links:
            dataset_url = response.urljoin(link)
            
            yield scrapy.Request(
                url=dataset_url,
                callback=self.parse_detail_page,
                errback=self.handle_error,
                meta={'platform': self.platform_name}
            )
            
            self.stats['pages_scraped'] += 1
        
        # Handle pagination
        next_page = response.css('a.next-page::attr(href), '
                                'a[rel="next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_list_page,
                errback=self.handle_error
            )
    
    def parse_detail_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse dataset detail page.
        
        Args:
            response: Response from detail page
            
        Returns:
            Dictionary with extracted data
        """
        self.logger.info(f"Parsing detail page: {response.url}")
        
        # Extract common metadata
        item = self.extract_common_metadata(response)
        
        # Extract dataset-specific fields
        # Note: Actual selectors need to be verified once site is accessible
        item.update({
            # Basic information
            'dataset_name': self.clean_text(response.css('h1.dataset-title::text').get()),
            'dataset_id': self.clean_text(response.css('span.dataset-id::text').get()),
            'acronym': self.clean_text(response.css('span.acronym::text').get()),
            
            # Description
            'description': self.clean_text(
                ' '.join(response.css('div.description *::text').getall())
            ),
            'objectives': self.clean_text(
                ' '.join(response.css('div.objectives *::text').getall())
            ),
            
            # Study information
            'study_type': self.clean_text(response.css('span.study-type::text').get()),
            'study_design': self.clean_text(response.css('div.study-design::text').get()),
            
            # Participants
            'participant_count': self.clean_text(response.css('span.participants::text').get()),
            'age_range': self.clean_text(response.css('span.age-range::text').get()),
            'gender_distribution': self.clean_text(response.css('span.gender::text').get()),
            
            # Data collection
            'collection_period': {
                'start': self.clean_text(response.css('span.collection-start::text').get()),
                'end': self.clean_text(response.css('span.collection-end::text').get()),
            },
            'data_collection_methods': response.css('div.methods li::text').getall(),
            
            # Sleep-specific data
            'sleep_measures': response.css('div.sleep-measures li::text').getall(),
            'polysomnography': self.clean_text(
                response.css('div.polysomnography::text').get()
            ),
            
            # Available data
            'data_files': self._extract_data_files(response),
            'data_formats': response.css('div.data-formats span::text').getall(),
            
            # Access information
            'access_type': self.clean_text(response.css('span.access-type::text').get()),
            'data_use_agreement': self.clean_text(
                response.css('div.data-use-agreement::text').get()
            ),
            
            # Principal investigator
            'principal_investigator': self.clean_text(response.css('span.pi-name::text').get()),
            'institution': self.clean_text(response.css('span.institution::text').get()),
            
            # Funding
            'funding_source': self.clean_text(response.css('span.funding::text').get()),
            'grant_number': self.clean_text(response.css('span.grant::text').get()),
            
            # Publications
            'publications': self._extract_publications(response),
            
            # Contact
            'contact_email': self.clean_text(
                response.css('a.contact-email::attr(href)').get()
            ),
        })
        
        self.stats['items_extracted'] += 1
        
        return item
    
    def _extract_data_files(self, response: Response) -> list:
        """Extract data file information."""
        files = []
        
        for file_item in response.css('div.data-file-item, tr.file-row'):
            file_info = {
                'filename': self.clean_text(file_item.css('span.filename::text').get()),
                'size': self.clean_text(file_item.css('span.filesize::text').get()),
                'format': self.clean_text(file_item.css('span.format::text').get()),
                'description': self.clean_text(file_item.css('div.description::text').get()),
                'download_url': file_item.css('a.download::attr(href)').get(),
            }
            
            if file_info['filename']:
                files.append(file_info)
        
        return files
    
    def _extract_publications(self, response: Response) -> list:
        """Extract publication information."""
        publications = []
        
        for pub in response.css('div.publication-item, li.publication'):
            publication = {
                'title': self.clean_text(pub.css('h4.pub-title::text').get()),
                'authors': self.clean_text(pub.css('div.pub-authors::text').get()),
                'journal': self.clean_text(pub.css('span.pub-journal::text').get()),
                'year': self.clean_text(pub.css('span.pub-year::text').get()),
                'pmid': self.clean_text(pub.css('span.pmid::text').get()),
                'doi': self.clean_text(pub.css('a.doi::attr(href)').get()),
            }
            
            if publication['title']:
                publications.append(publication)
        
        return publications


if __name__ == "__main__":
    # For testing purposes
    from scrapy.crawler import CrawlerProcess
    
    print("Note: NSRR website may be experiencing technical issues.")
    print("If you encounter errors, please try again later.")
    print()
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; BiomedicalResearchBot/1.0)',
        'LOG_LEVEL': 'INFO',
    })
    
    process.crawl(NsrrSpider)
    process.start()
