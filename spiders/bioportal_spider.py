"""
BioPortal Spider

Spider for scraping data from NCBO BioPortal (National Center for Biomedical Ontology BioPortal).
URL: https://bioportal.bioontology.org

This spider uses the BioPortal REST API for efficient data collection.
"""

import scrapy
import json
from typing import Iterator, Dict, Any
from scrapy.http import Response, Request
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.base_spider import BaseSpider


class BioportalSpider(BaseSpider):
    """
    Spider for BioPortal platform.
    
    Extracts:
    - Ontology metadata (name, acronym, description)
    - Ontology statistics (classes, properties, individuals)
    - Ontology categories and groups
    - Submission information
    - Contact information
    - Licensing information
    """
    
    name = 'bioportal'
    
    # API endpoints
    API_BASE = 'https://data.bioontology.org'
    API_ONTOLOGIES = f'{API_BASE}/ontologies'
    
    custom_settings = {
        **BaseSpider.custom_settings,
        'DOWNLOAD_DELAY': 1,  # API can handle faster requests
    }
    
    def __init__(self, api_key=None, *args, **kwargs):
        # Platform configuration
        platform_config = {
            'name': 'BioPortal',
            'base_url': 'https://bioportal.bioontology.org',
            'start_url': self.API_ONTOLOGIES,
            'auth_required': True,  # API key required
        }
        
        # Get API key from arguments or credentials
        self.api_key = api_key or kwargs.get('credentials', {}).get('api_key')
        
        if not self.api_key:
            self.logger.warning("No API key provided. You can get one from: "
                              "https://bioportal.bioontology.org/account")
        
        super().__init__(platform_config=platform_config, *args, **kwargs)
    
    def start_requests(self):
        """
        Start by requesting the ontologies list from API.
        """
        if not self.api_key:
            self.logger.error("API key is required. Please provide via --api_key argument "
                            "or in credentials.yaml")
            return
        
        headers = {
            'Authorization': f'apikey token={self.api_key}',
            'Accept': 'application/json',
        }
        
        yield scrapy.Request(
            url=self.API_ONTOLOGIES,
            headers=headers,
            callback=self.parse_list_page,
            errback=self.handle_error,
            meta={'platform': self.platform_name}
        )
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse the ontologies list from API response.
        
        Args:
            response: JSON response from API
            
        Yields:
            Requests to ontology detail endpoints
        """
        try:
            data = json.loads(response.text)
            
            # API returns list of ontologies
            ontologies = data if isinstance(data, list) else []
            
            self.logger.info(f"Found {len(ontologies)} ontologies")
            
            for ontology in ontologies:
                # Get the links object
                links = ontology.get('@id') or ontology.get('links', {}).get('self')
                
                if links:
                    yield scrapy.Request(
                        url=links,
                        headers={'Authorization': f'apikey token={self.api_key}'},
                        callback=self.parse_detail_page,
                        errback=self.handle_error,
                        meta={
                            'platform': self.platform_name,
                            'ontology_acronym': ontology.get('acronym'),
                        }
                    )
                    
                    self.stats['pages_scraped'] += 1
                    
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
        except Exception as e:
            self.logger.error(f"Error parsing ontologies list: {e}")
    
    def parse_detail_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse ontology detail page from API response.
        
        Args:
            response: JSON response from API
            
        Returns:
            Dictionary with extracted data
        """
        try:
            data = json.loads(response.text)
            
            # Extract common metadata
            item = self.extract_common_metadata(response)
            
            # Extract ontology-specific fields
            item.update({
                # Basic information
                'ontology_id': data.get('@id'),
                'acronym': data.get('acronym'),
                'name': data.get('name'),
                'description': self.clean_text(data.get('description')),
                
                # Administrative info
                'administeredBy': data.get('administeredBy', []),
                'accrualMethod': data.get('accrualMethod'),
                'accrualPeriodicity': data.get('accrualPeriodicity'),
                
                # Categorization
                'hasDomain': data.get('hasDomain', []),
                'group': data.get('group', []),
                'categories': data.get('categories', []),
                
                # Ontology details
                'ontologyType': data.get('ontologyType'),
                'hasOntologyLanguage': data.get('hasOntologyLanguage'),
                'isOfType': data.get('isOfType'),
                
                # Status and dates
                'status': data.get('status'),
                'creationDate': data.get('creationDate'),
                'dateReleased': data.get('dateReleased'),
                
                # Metrics (from latest submission)
                'metrics': self._extract_metrics(data),
                
                # Latest submission info
                'latest_submission': self._extract_submission_info(data),
                
                # Contact information
                'contacts': self._extract_contacts(data),
                
                # Links
                'homepage': data.get('homepage'),
                'documentation': data.get('documentation'),
                'publication': data.get('publication'),
                'repository': data.get('repository'),
                
                # Access info
                'viewingRestriction': data.get('viewingRestriction'),
                'licenseInformation': data.get('licenseInformation'),
                
                # Notes
                'notes': data.get('notes'),
            })
            
            self.stats['items_extracted'] += 1
            
            return item
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Error parsing ontology detail: {e}")
            return {}
    
    def _extract_metrics(self, data: dict) -> dict:
        """Extract metrics information."""
        metrics_link = data.get('links', {}).get('metrics')
        
        if not metrics_link:
            return {}
        
        # Note: In a full implementation, we would make another API call here
        # For now, return the link for future processing
        return {
            'metrics_url': metrics_link,
        }
    
    def _extract_submission_info(self, data: dict) -> dict:
        """Extract latest submission information."""
        submission_link = data.get('links', {}).get('latest_submission')
        
        if not submission_link:
            return {}
        
        return {
            'submission_url': submission_link,
            'submissionId': data.get('submissionId'),
            'version': data.get('version'),
        }
    
    def _extract_contacts(self, data: dict) -> list:
        """Extract contact information."""
        contacts = []
        
        for contact in data.get('contacts', []):
            contact_info = {
                'name': contact.get('name'),
                'email': contact.get('email'),
                'role': contact.get('role'),
            }
            contacts.append(contact_info)
        
        return contacts


if __name__ == "__main__":
    # For testing purposes
    import os
    from scrapy.crawler import CrawlerProcess
    
    # Try to get API key from environment
    api_key = os.getenv('BIOPORTAL_API_KEY')
    
    if not api_key:
        print("Error: BIOPORTAL_API_KEY environment variable not set")
        print("Get your API key from: https://bioportal.bioontology.org/account")
        print("\nUsage:")
        print("  export BIOPORTAL_API_KEY='your_key_here'")
        print("  python spiders/bioportal_spider.py")
        exit(1)
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; BiomedicalResearchBot/1.0)',
        'LOG_LEVEL': 'INFO',
    })
    
    process.crawl(BioportalSpider, api_key=api_key)
    process.start()
