"""
Enhanced File Download Pipeline

This pipeline handles downloading of all file types (PDF, Word, Excel, etc.)
and organizes them according to the standard directory structure:
- main_file/: Main PDF files
- SI_file/: Supplementary Information files
- PR_file/: Peer Review files
- images/: Extracted images
"""

import os
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem


class BiomedicalFilesPipeline(FilesPipeline):
    """
    Enhanced files pipeline for biomedical data scraping.
    
    Features:
    - Organizes files by type (main, supplementary, peer review)
    - Maintains track_id association
    - Generates SHA256 checksums
    - Supports nested file structures
    """
    
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func=download_func, settings=settings)
        self.logger = logging.getLogger(__name__)
    
    def get_media_requests(self, item, info):
        """
        Generate download requests for all files in the item.
        
        Args:
            item: Scraped item containing file URLs
            info: Spider info
            
        Yields:
            Download requests
        """
        # Get track_id for this item
        track_id = item.get('track_id')
        
        if not track_id:
            self.logger.warning("Item missing track_id, skipping file downloads")
            return
        
        # Download main PDF
        main_pdf_url = item.get('pdf_url')
        if main_pdf_url:
            yield Request(
                url=main_pdf_url,
                meta={
                    'track_id': track_id,
                    'file_type': 'main',
                    'file_index': 0,
                }
            )
        
        # Download supplementary files
        supplementary_files = item.get('supplementary_files', [])
        for idx, file_info in enumerate(supplementary_files, start=1):
            file_url = file_info.get('url') if isinstance(file_info, dict) else file_info
            
            if file_url:
                yield Request(
                    url=file_url,
                    meta={
                        'track_id': track_id,
                        'file_type': 'supplementary',
                        'file_index': idx,
                        'file_info': file_info if isinstance(file_info, dict) else {},
                    }
                )
        
        # Download peer review files
        peer_review_files = item.get('peer_review_files', [])
        for idx, file_info in enumerate(peer_review_files, start=1):
            file_url = file_info.get('url') if isinstance(file_info, dict) else file_info
            
            if file_url:
                yield Request(
                    url=file_url,
                    meta={
                        'track_id': track_id,
                        'file_type': 'peer_review',
                        'file_index': idx,
                        'file_info': file_info if isinstance(file_info, dict) else {},
                    }
                )
        
        # Download comment attachments
        comments = item.get('comments', [])
        for comment_idx, comment in enumerate(comments, start=1):
            attachments = comment.get('attachments', [])
            
            for attach_idx, attach_info in enumerate(attachments, start=1):
                attach_url = attach_info.get('url') if isinstance(attach_info, dict) else attach_info
                
                if attach_url:
                    yield Request(
                        url=attach_url,
                        meta={
                            'track_id': track_id,
                            'file_type': 'comment_attachment',
                            'comment_index': comment_idx,
                            'file_index': attach_idx,
                            'file_info': attach_info if isinstance(attach_info, dict) else {},
                        }
                    )
    
    def file_path(self, request, response=None, info=None, *, item=None):
        """
        Generate file path according to standard directory structure.
        
        Args:
            request: Download request
            response: Download response
            info: Spider info
            item: Scraped item
            
        Returns:
            Relative file path
        """
        track_id = request.meta.get('track_id')
        file_type = request.meta.get('file_type', 'unknown')
        file_index = request.meta.get('file_index', 0)
        
        # Get file extension from URL or Content-Type
        file_ext = self._get_file_extension(request.url, response)
        
        # Generate filename based on file type
        if file_type == 'main':
            # Main PDF: main_file/{track_id}.pdf
            filename = f"{track_id}{file_ext}"
            return f"main_file/{filename}"
        
        elif file_type == 'supplementary':
            # Supplementary: SI_file/{track_id}/sup_{index}.{ext}
            filename = f"sup_{file_index}{file_ext}"
            return f"SI_file/{track_id}/{filename}"
        
        elif file_type == 'peer_review':
            # Peer review: PR_file/{track_id}/pr_{index}.{ext}
            filename = f"pr_{file_index}{file_ext}"
            return f"PR_file/{track_id}/{filename}"
        
        elif file_type == 'comment_attachment':
            # Comment attachment: PR_file/{track_id}/comment_{comment_idx}_attach_{attach_idx}.{ext}
            comment_idx = request.meta.get('comment_index', 0)
            filename = f"comment_{comment_idx}_attach_{file_index}{file_ext}"
            return f"PR_file/{track_id}/{filename}"
        
        else:
            # Unknown type: other/{track_id}/{filename}
            filename = os.path.basename(urlparse(request.url).path)
            if not filename:
                filename = f"file_{file_index}{file_ext}"
            return f"other/{track_id}/{filename}"
    
    def _get_file_extension(self, url: str, response=None) -> str:
        """
        Determine file extension from URL or Content-Type.
        
        Args:
            url: File URL
            response: HTTP response (optional)
            
        Returns:
            File extension with leading dot (e.g., '.pdf')
        """
        # Try to get extension from URL
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        if path:
            _, ext = os.path.splitext(path)
            if ext:
                return ext.lower()
        
        # Try to get extension from Content-Type header
        if response:
            content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
            
            ext_map = {
                'application/pdf': '.pdf',
                'application/msword': '.doc',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
                'application/vnd.ms-excel': '.xls',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
                'text/plain': '.txt',
                'text/csv': '.csv',
                'application/zip': '.zip',
                'application/x-gzip': '.gz',
            }
            
            for mime_type, extension in ext_map.items():
                if mime_type in content_type:
                    return extension
        
        # Default to .bin if unknown
        return '.bin'
    
    def item_completed(self, results, item, info):
        """
        Called when all file downloads for an item are completed.
        
        Args:
            results: List of (success, file_info) tuples
            item: Scraped item
            info: Spider info
            
        Returns:
            Updated item with file paths
        """
        # Separate successful and failed downloads
        successful = []
        failed = []
        
        for success, file_info in results:
            if success:
                successful.append(file_info)
            else:
                failed.append(file_info)
        
        # Add file information to item
        item['downloaded_files'] = {
            'successful': len(successful),
            'failed': len(failed),
            'files': successful,
        }
        
        # Log statistics
        self.logger.info(
            f"Downloaded {len(successful)} files for track_id={item.get('track_id')}, "
            f"{len(failed)} failed"
        )
        
        if failed:
            self.logger.warning(f"Failed downloads: {failed}")
        
        # Generate checksums for downloaded files
        for file_info in successful:
            file_path = file_info.get('path')
            if file_path:
                full_path = os.path.join(self.store.basedir, file_path)
                if os.path.exists(full_path):
                    file_info['sha256'] = self._calculate_sha256(full_path)
        
        return item
    
    def _calculate_sha256(self, file_path: str) -> str:
        """
        Calculate SHA256 checksum of a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            SHA256 hex digest
        """
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.logger.error(f"Failed to calculate SHA256 for {file_path}: {e}")
            return ""


class ImageExtractionPipeline:
    """
    Pipeline for extracting and downloading images from web pages.
    
    Images are saved to: images/{track_id}/sha256(image_url).{ext}
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_item(self, item, spider):
        """
        Extract image URLs from item and prepare for download.
        
        Args:
            item: Scraped item
            spider: Spider instance
            
        Returns:
            Updated item
        """
        track_id = item.get('track_id')
        
        if not track_id:
            return item
        
        # Extract image URLs from various fields
        image_urls = []
        
        # From explicit image_urls field
        if 'image_urls' in item:
            image_urls.extend(item['image_urls'])
        
        # From content (if HTML is included)
        if 'html_content' in item:
            # This would require BeautifulSoup to parse
            # For now, we'll skip this
            pass
        
        # Store image information
        if image_urls:
            item['images_to_download'] = [
                {
                    'url': url,
                    'filename': self._generate_image_filename(url),
                }
                for url in image_urls
            ]
        
        return item
    
    def _generate_image_filename(self, url: str) -> str:
        """
        Generate image filename using SHA256 of URL.
        
        Args:
            url: Image URL
            
        Returns:
            Filename
        """
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        
        # Get extension from URL
        parsed_url = urlparse(url)
        _, ext = os.path.splitext(parsed_url.path)
        
        if not ext:
            ext = '.jpg'  # Default
        
        return f"{url_hash}{ext}"
