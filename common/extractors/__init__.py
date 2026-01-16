"""
Extractors module for common data extraction patterns.
"""

from .comment_extractor import CommentExtractor, extract_comments_from_response

__all__ = ['CommentExtractor', 'extract_comments_from_response']
