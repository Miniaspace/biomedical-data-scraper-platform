"""
Comment Extraction Module

Provides utilities for extracting comments, reviews, and nested content
from web pages. Supports various comment structures and formats.
"""

from typing import List, Dict, Any, Optional
from scrapy.http import Response
import re
from datetime import datetime


class CommentExtractor:
    """
    Generic comment extractor that can be customized for different platforms.
    """
    
    def __init__(self, response: Response):
        """
        Initialize extractor with a response object.
        
        Args:
            response: Scrapy Response object
        """
        self.response = response
        self.comments = []
    
    def extract_comments(self, 
                        comment_selector: str,
                        author_selector: str = None,
                        date_selector: str = None,
                        content_selector: str = None,
                        attachment_selector: str = None) -> List[Dict[str, Any]]:
        """
        Extract comments using CSS selectors.
        
        Args:
            comment_selector: CSS selector for comment containers
            author_selector: CSS selector for author name (relative to comment)
            date_selector: CSS selector for date (relative to comment)
            content_selector: CSS selector for content (relative to comment)
            attachment_selector: CSS selector for attachments (relative to comment)
            
        Returns:
            List of comment dictionaries
        """
        comments = []
        
        for idx, comment_elem in enumerate(self.response.css(comment_selector), start=1):
            comment_data = {
                'comment_id': idx,
                'author': self._extract_text(comment_elem, author_selector),
                'date': self._extract_text(comment_elem, date_selector),
                'content': self._extract_text(comment_elem, content_selector),
                'attachments': [],
            }
            
            # Extract attachments if selector provided
            if attachment_selector:
                attachments = self._extract_attachments(comment_elem, attachment_selector)
                comment_data['attachments'] = attachments
            
            # Clean and normalize date
            if comment_data['date']:
                comment_data['date_normalized'] = self._normalize_date(comment_data['date'])
            
            comments.append(comment_data)
        
        return comments
    
    def extract_peer_reviews(self,
                            review_selector: str,
                            reviewer_selector: str = None,
                            decision_selector: str = None,
                            comments_selector: str = None,
                            attachment_selector: str = None) -> List[Dict[str, Any]]:
        """
        Extract peer review information.
        
        Args:
            review_selector: CSS selector for review containers
            reviewer_selector: CSS selector for reviewer info
            decision_selector: CSS selector for decision (accept/reject/revise)
            comments_selector: CSS selector for review comments
            attachment_selector: CSS selector for review attachments
            
        Returns:
            List of peer review dictionaries
        """
        reviews = []
        
        for idx, review_elem in enumerate(self.response.css(review_selector), start=1):
            review_data = {
                'review_id': idx,
                'reviewer': self._extract_text(review_elem, reviewer_selector),
                'decision': self._extract_text(review_elem, decision_selector),
                'comments': self._extract_text(review_elem, comments_selector),
                'attachments': [],
            }
            
            # Extract attachments
            if attachment_selector:
                attachments = self._extract_attachments(review_elem, attachment_selector)
                review_data['attachments'] = attachments
            
            reviews.append(review_data)
        
        return reviews
    
    def extract_nested_comments(self,
                               parent_selector: str,
                               reply_selector: str,
                               **kwargs) -> List[Dict[str, Any]]:
        """
        Extract nested comments (comments with replies).
        
        Args:
            parent_selector: CSS selector for parent comments
            reply_selector: CSS selector for replies (relative to parent)
            **kwargs: Additional selectors for author, date, content, etc.
            
        Returns:
            List of comment dictionaries with nested replies
        """
        comments = []
        
        for idx, parent_elem in enumerate(self.response.css(parent_selector), start=1):
            # Extract parent comment
            parent_comment = {
                'comment_id': idx,
                'author': self._extract_text(parent_elem, kwargs.get('author_selector')),
                'date': self._extract_text(parent_elem, kwargs.get('date_selector')),
                'content': self._extract_text(parent_elem, kwargs.get('content_selector')),
                'replies': [],
                'attachments': [],
            }
            
            # Extract attachments for parent
            if kwargs.get('attachment_selector'):
                parent_comment['attachments'] = self._extract_attachments(
                    parent_elem, 
                    kwargs['attachment_selector']
                )
            
            # Extract replies
            for reply_idx, reply_elem in enumerate(parent_elem.css(reply_selector), start=1):
                reply_data = {
                    'reply_id': reply_idx,
                    'author': self._extract_text(reply_elem, kwargs.get('author_selector')),
                    'date': self._extract_text(reply_elem, kwargs.get('date_selector')),
                    'content': self._extract_text(reply_elem, kwargs.get('content_selector')),
                    'attachments': [],
                }
                
                # Extract attachments for reply
                if kwargs.get('attachment_selector'):
                    reply_data['attachments'] = self._extract_attachments(
                        reply_elem,
                        kwargs['attachment_selector']
                    )
                
                parent_comment['replies'].append(reply_data)
            
            comments.append(parent_comment)
        
        return comments
    
    def _extract_text(self, element, selector: Optional[str]) -> str:
        """
        Extract and clean text from element using selector.
        
        Args:
            element: Scrapy Selector element
            selector: CSS selector
            
        Returns:
            Cleaned text
        """
        if not selector:
            return ""
        
        text = element.css(selector + '::text').get()
        
        if not text:
            # Try to get all text within element
            text = ' '.join(element.css(selector + ' *::text').getall())
        
        return self._clean_text(text)
    
    def _extract_attachments(self, element, selector: str) -> List[Dict[str, str]]:
        """
        Extract attachment information from element.
        
        Args:
            element: Scrapy Selector element
            selector: CSS selector for attachment links
            
        Returns:
            List of attachment dictionaries
        """
        attachments = []
        
        for attach_elem in element.css(selector):
            url = attach_elem.css('::attr(href)').get()
            filename = attach_elem.css('::text').get() or attach_elem.css('::attr(title)').get()
            
            if url:
                # Make URL absolute
                url = self.response.urljoin(url)
                
                attachments.append({
                    'url': url,
                    'filename': self._clean_text(filename) if filename else None,
                    'type': self._guess_file_type(url),
                })
        
        return attachments
    
    def _clean_text(self, text: Optional[str]) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _normalize_date(self, date_str: str) -> Optional[str]:
        """
        Attempt to normalize date string to ISO format.
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            ISO format date string or None
        """
        if not date_str:
            return None
        
        # Common date patterns
        patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
            r'(\d{2})/(\d{2})/(\d{4})',  # MM/DD/YYYY
            r'(\d{2})-(\d{2})-(\d{4})',  # DD-MM-YYYY
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    # This is a simplified implementation
                    # In production, use dateutil.parser for robust parsing
                    return match.group(0)
                except:
                    pass
        
        return date_str  # Return as-is if can't parse
    
    def _guess_file_type(self, url: str) -> str:
        """
        Guess file type from URL extension.
        
        Args:
            url: File URL
            
        Returns:
            File type string
        """
        url_lower = url.lower()
        
        if url_lower.endswith('.pdf'):
            return 'pdf'
        elif url_lower.endswith(('.doc', '.docx')):
            return 'word'
        elif url_lower.endswith(('.xls', '.xlsx')):
            return 'excel'
        elif url_lower.endswith(('.zip', '.tar', '.gz')):
            return 'archive'
        elif url_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return 'image'
        else:
            return 'unknown'


# Convenience function for quick extraction
def extract_comments_from_response(response: Response, 
                                   comment_selector: str,
                                   **kwargs) -> List[Dict[str, Any]]:
    """
    Quick function to extract comments from a response.
    
    Args:
        response: Scrapy Response
        comment_selector: CSS selector for comments
        **kwargs: Additional selectors
        
    Returns:
        List of comments
    """
    extractor = CommentExtractor(response)
    return extractor.extract_comments(comment_selector, **kwargs)
