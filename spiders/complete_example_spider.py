"""
Complete Example Spider

This spider demonstrates how to extract ALL types of data:
- Metadata
- PDF files
- Supplementary files
- Peer review files
- Comments and comment attachments
- Images

This serves as a template for implementing comprehensive data extraction.
"""

import scrapy
from typing import Iterator, Dict, Any
from scrapy.http import Response, Request
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from common.base_spider import BaseSpider
from common.extractors.comment_extractor import CommentExtractor


class CompleteExampleSpider(BaseSpider):
    """
    Complete example spider showing all extraction capabilities.
    
    This is a TEMPLATE spider. For real platforms, you need to:
    1. Update the selectors to match the actual HTML structure
    2. Adjust the parsing logic for the specific platform
    3. Configure the platform in config/platforms.yaml
    """
    
    name = 'complete_example'
    
    # Enable file downloads
    custom_settings = {
        **BaseSpider.custom_settings,
        
        # Enable file pipeline
        'ITEM_PIPELINES': {
            'common.pipeline.file_pipeline.BiomedicalFilesPipeline': 1,
            'common.pipeline.data_pipeline.ScrapyPipeline': 300,
        },
        
        # Configure file storage
        'FILES_STORE': 'data/files',  # Base directory for all files
        
        # File download settings
        'FILES_URLS_FIELD': 'file_urls',  # Field containing URLs to download
        'FILES_RESULT_FIELD': 'files',    # Field to store download results
        
        # Retry settings for file downloads
        'FILES_DOWNLOAD_TIMEOUT': 120,
        'MEDIA_ALLOW_REDIRECTS': True,
    }
    
    def __init__(self, *args, **kwargs):
        platform_config = {
            'name': 'Complete Example Platform',
            'base_url': 'https://example-research-platform.org',
            'start_url': 'https://example-research-platform.org/datasets',
            'auth_required': False,
        }
        
        super().__init__(platform_config=platform_config, *args, **kwargs)
    
    def parse_list_page(self, response: Response) -> Iterator[Request]:
        """
        Parse the dataset list page.
        
        Extract links to individual dataset pages.
        """
        self.logger.info(f"Parsing list page: {response.url}")
        
        # Example selector - adjust for your platform
        dataset_links = response.css('div.dataset-item a.dataset-link::attr(href)').getall()
        
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
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_list_page,
                errback=self.handle_error
            )
    
    def parse_detail_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse dataset detail page and extract ALL data.
        
        This method demonstrates comprehensive data extraction.
        """
        self.logger.info(f"Parsing detail page: {response.url}")
        
        # 1. Extract common metadata
        item = self.extract_common_metadata(response)
        
        # 2. Extract basic information
        item.update({
            'title': self.clean_text(response.css('h1.dataset-title::text').get()),
            'description': self.clean_text(
                ' '.join(response.css('div.description *::text').getall())
            ),
            'authors': response.css('span.author::text').getall(),
            'publication_date': self.clean_text(response.css('span.pub-date::text').get()),
            'doi': self.clean_text(response.css('span.doi::text').get()),
            'keywords': response.css('span.keyword::text').getall(),
        })
        
        # 3. Extract PDF URL (main file)
        pdf_url = response.css('a.download-pdf::attr(href)').get()
        if pdf_url:
            item['pdf_url'] = response.urljoin(pdf_url)
        
        # 4. Extract supplementary files
        supplementary_files = []
        for file_elem in response.css('div.supplementary-files li.file-item'):
            file_info = {
                'url': response.urljoin(file_elem.css('a::attr(href)').get()),
                'filename': self.clean_text(file_elem.css('span.filename::text').get()),
                'size': self.clean_text(file_elem.css('span.filesize::text').get()),
                'description': self.clean_text(file_elem.css('span.description::text').get()),
            }
            supplementary_files.append(file_info)
        
        item['supplementary_files'] = supplementary_files
        
        # 5. Extract peer review files (if available)
        peer_review_files = []
        for review_elem in response.css('div.peer-reviews li.review-file'):
            review_info = {
                'url': response.urljoin(review_elem.css('a::attr(href)').get()),
                'filename': self.clean_text(review_elem.css('span.filename::text').get()),
                'reviewer': self.clean_text(review_elem.css('span.reviewer::text').get()),
                'date': self.clean_text(review_elem.css('span.date::text').get()),
            }
            peer_review_files.append(review_info)
        
        item['peer_review_files'] = peer_review_files
        
        # 6. Extract comments using CommentExtractor
        comment_extractor = CommentExtractor(response)
        
        comments = comment_extractor.extract_comments(
            comment_selector='div.comment-item',
            author_selector='span.comment-author',
            date_selector='span.comment-date',
            content_selector='div.comment-content',
            attachment_selector='div.comment-attachments a.attachment-link'
        )
        
        item['comments'] = comments
        
        # 7. Extract images from the page
        image_urls = []
        for img in response.css('div.content img::attr(src)').getall():
            image_url = response.urljoin(img)
            image_urls.append(image_url)
        
        item['image_urls'] = image_urls
        
        # 8. Extract additional metadata
        item.update({
            'dataset_id': self.clean_text(response.css('span.dataset-id::text').get()),
            'version': self.clean_text(response.css('span.version::text').get()),
            'license': self.clean_text(response.css('span.license::text').get()),
            'access_type': self.clean_text(response.css('span.access-type::text').get()),
            
            # Statistics
            'download_count': self.clean_text(response.css('span.downloads::text').get()),
            'view_count': self.clean_text(response.css('span.views::text').get()),
            'citation_count': self.clean_text(response.css('span.citations::text').get()),
            
            # Related information
            'related_publications': self._extract_publications(response),
            'funding_information': self._extract_funding(response),
            'contact_information': self._extract_contact(response),
        })
        
        # 9. Check if there are additional pages (e.g., separate comments page)
        comments_page_url = response.css('a.view-all-comments::attr(href)').get()
        if comments_page_url:
            # Request the comments page
            yield scrapy.Request(
                url=response.urljoin(comments_page_url),
                callback=self.parse_comments_page,
                errback=self.handle_error,
                meta={
                    'platform': self.platform_name,
                    'parent_item': item,  # Pass the main item
                }
            )
        else:
            # No additional pages, yield the item now
            self.stats['items_extracted'] += 1
            yield item
    
    def parse_comments_page(self, response: Response) -> Dict[str, Any]:
        """
        Parse a separate comments page (if comments are on a different page).
        
        This demonstrates handling multi-page data extraction.
        """
        self.logger.info(f"Parsing comments page: {response.url}")
        
        # Get the parent item from meta
        item = response.meta.get('parent_item', {})
        
        # Extract comments from this page
        comment_extractor = CommentExtractor(response)
        
        additional_comments = comment_extractor.extract_comments(
            comment_selector='div.comment-item',
            author_selector='span.comment-author',
            date_selector='span.comment-date',
            content_selector='div.comment-content',
            attachment_selector='div.comment-attachments a.attachment-link'
        )
        
        # Merge with existing comments
        existing_comments = item.get('comments', [])
        item['comments'] = existing_comments + additional_comments
        
        # Handle pagination in comments
        next_comments_page = response.css('a.next-comments-page::attr(href)').get()
        if next_comments_page:
            yield scrapy.Request(
                url=response.urljoin(next_comments_page),
                callback=self.parse_comments_page,
                errback=self.handle_error,
                meta={
                    'platform': self.platform_name,
                    'parent_item': item,
                }
            )
        else:
            # No more pages, yield the complete item
            self.stats['items_extracted'] += 1
            yield item
    
    def _extract_publications(self, response: Response) -> list:
        """Extract related publications."""
        publications = []
        
        for pub_elem in response.css('div.related-publications li.publication'):
            publication = {
                'title': self.clean_text(pub_elem.css('h4.pub-title::text').get()),
                'authors': pub_elem.css('span.pub-author::text').getall(),
                'journal': self.clean_text(pub_elem.css('span.pub-journal::text').get()),
                'year': self.clean_text(pub_elem.css('span.pub-year::text').get()),
                'doi': self.clean_text(pub_elem.css('a.pub-doi::attr(href)').get()),
            }
            publications.append(publication)
        
        return publications
    
    def _extract_funding(self, response: Response) -> dict:
        """Extract funding information."""
        return {
            'agency': self.clean_text(response.css('span.funding-agency::text').get()),
            'grant_number': self.clean_text(response.css('span.grant-number::text').get()),
            'amount': self.clean_text(response.css('span.funding-amount::text').get()),
        }
    
    def _extract_contact(self, response: Response) -> dict:
        """Extract contact information."""
        return {
            'name': self.clean_text(response.css('span.contact-name::text').get()),
            'email': self.clean_text(response.css('a.contact-email::attr(href)').get()),
            'institution': self.clean_text(response.css('span.contact-institution::text').get()),
        }


if __name__ == "__main__":
    # For testing purposes
    from scrapy.crawler import CrawlerProcess
    
    print("=" * 60)
    print("Complete Example Spider - Demonstration")
    print("=" * 60)
    print()
    print("This spider demonstrates comprehensive data extraction:")
    print("  ✓ Metadata")
    print("  ✓ PDF files")
    print("  ✓ Supplementary files")
    print("  ✓ Peer review files")
    print("  ✓ Comments and comment attachments")
    print("  ✓ Images")
    print()
    print("Note: This is a TEMPLATE. You need to adjust selectors")
    print("      for your specific platform.")
    print("=" * 60)
    print()
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; BiomedicalResearchBot/1.0)',
        'LOG_LEVEL': 'INFO',
    })
    
    process.crawl(CompleteExampleSpider)
    process.start()
