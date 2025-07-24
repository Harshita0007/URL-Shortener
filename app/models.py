# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

from datetime import datetime
from typing import Dict, Optional

class URLStore:
    """
    Thread-safe in-memory storage for URL mappings
    Stores URL data with metadata including clicks and creation time
    """
    
    def __init__(self):
        # Dictionary to store URL mappings
        # Structure: {short_code: {original_url, clicks, created_at}}
        self._urls: Dict[str, Dict] = {}
    
    def store_url(self, short_code: str, original_url: str) -> None:
        """
        Store a URL mapping with metadata
        
        Args:
            short_code: The generated short code
            original_url: The original long URL
        """
        self._urls[short_code] = {
            'original_url': original_url,
            'clicks': 0,
            'created_at': datetime.utcnow()
        }
    
    def get_url(self, short_code: str) -> Optional[Dict]:
        """
        Retrieve URL data by short code
        
        Args:
            short_code: The short code to look up
            
        Returns:
            Dictionary with URL data or None if not found
        """
        return self._urls.get(short_code)
    
    def exists(self, short_code: str) -> bool:
        """
        Check if a short code already exists
        
        Args:
            short_code: The short code to check
            
        Returns:
            True if exists, False otherwise
        """
        return short_code in self._urls
    
    def increment_clicks(self, short_code: str) -> None:
        """
        Increment the click count for a short code
        
        Args:
            short_code: The short code to increment clicks for
        """
        if short_code in self._urls:
            self._urls[short_code]['clicks'] += 1
    
    def get_all_urls(self) -> Dict[str, Dict]:
        """
        Get all stored URLs (useful for testing)
        
        Returns:
            Dictionary of all URL mappings
        """
        return self._urls.copy()
    
    def clear(self) -> None:
        """
        Clear all stored URLs (useful for testing)
        """
        self._urls.clear()