# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import random
import string
import re
from urllib.parse import urlparse

def generate_short_code(length: int = 6) -> str:
    """
    Generate a random short code of specified length
    Uses alphanumeric characters (a-z, A-Z, 0-9)
    
    Args:
        length: Length of the short code (default: 6)
        
    Returns:
        Random alphanumeric string
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url: str) -> bool:
    """
    Validate if a string is a valid URL
    Checks for proper URL format and scheme
    
    Args:
        url: The URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        
        parsed = urlparse(url)
        
       
        if not parsed.scheme or not parsed.netloc:
            return False
        
        
        if parsed.scheme not in ['http', 'https']:
            return False
        
        
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )
        
       
        hostname = parsed.netloc.split(':')[0]
        
       
        if not domain_pattern.match(hostname):
            return False
        
        return True
        
    except Exception:
        return False

def normalize_url(url: str) -> str:
    """
    Normalize URL by ensuring it has a proper scheme
    
    Args:
        url: The URL to normalize
        
    Returns:
        Normalized URL with proper scheme
    """
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url