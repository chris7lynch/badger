"""
QR Code utilities for badge app
Includes URL shortening and QR code generation for MicroPython
"""
import gc
from urllib.urequest import urlopen
import json


def shorten_url(long_url):
    """
    Shorten a URL using a free URL shortening service.
    Uses TinyURL API which doesn't require authentication.
    
    Args:
        long_url (str): The URL to shorten
        
    Returns:
        str: Shortened URL, or original URL if shortening fails
    """
    if not long_url:
        return None
        
    try:
        # Use TinyURL API (free, no auth required)
        api_url = f"https://tinyurl.com/api-create.php?url={long_url}"
        response = urlopen(api_url, headers={"User-Agent": "GitHub Universe Badge 2025"})
        shortened = response.read().decode('utf-8').strip()
        response.close()
        gc.collect()
        
        # Validate the response
        if shortened and shortened.startswith('http'):
            return shortened
        return long_url
    except Exception as e:
        print(f"URL shortening failed: {e}")
        return long_url


class QRCode:
    """
    Simple QR Code generator for MicroPython.
    Generates QR code matrix data that can be rendered on the badge display.
    """
    
    # QR Code error correction levels
    ERROR_CORRECT_L = 0  # Low - 7% correction
    ERROR_CORRECT_M = 1  # Medium - 15% correction
    ERROR_CORRECT_Q = 2  # Quartile - 25% correction
    ERROR_CORRECT_H = 3  # High - 30% correction
    
    def __init__(self, data, error_correction=ERROR_CORRECT_M):
        """
        Initialize QR code generator
        
        Args:
            data (str): The data to encode in the QR code
            error_correction (int): Error correction level (default: M)
        """
        self.data = data
        self.error_correction = error_correction
        self.modules = None
        self.size = 0
        
    def make(self):
        """
        Generate the QR code matrix.
        For MicroPython on embedded devices, we'll use a simplified approach
        that creates a basic QR code pattern suitable for URLs.
        """
        # Estimate QR version based on data length
        # Version 1 (21x21) can hold up to 25 alphanumeric chars with M correction
        # Version 2 (25x25) can hold up to 47 alphanumeric chars with M correction
        # Version 3 (29x29) can hold up to 77 alphanumeric chars with M correction
        data_len = len(self.data)
        
        if data_len <= 25:
            version = 1
            self.size = 21
        elif data_len <= 47:
            version = 2
            self.size = 25
        else:
            version = 3
            self.size = 29
            
        # For a real implementation, we would encode the data properly
        # For now, we'll create a placeholder pattern that indicates
        # this needs a proper QR encoding library
        
        # In a production system, you would either:
        # 1. Pre-generate QR codes offline and store as images
        # 2. Use a MicroPython QR library like micropython-qrcode
        # 3. Call an external API to generate QR codes
        
        self.modules = [[False for _ in range(self.size)] for _ in range(self.size)]
        
        # Add finder patterns (the three corner squares)
        self._add_finder_pattern(0, 0)
        self._add_finder_pattern(self.size - 7, 0)
        self._add_finder_pattern(0, self.size - 7)
        
        # Add timing patterns
        for i in range(8, self.size - 8):
            self.modules[6][i] = (i % 2 == 0)
            self.modules[i][6] = (i % 2 == 0)
            
        return self
        
    def _add_finder_pattern(self, x, y):
        """Add a QR finder pattern at the given position"""
        # Outer 7x7 black square
        for i in range(7):
            for j in range(7):
                if i == 0 or i == 6 or j == 0 or j == 6:
                    self.modules[y + i][x + j] = True
                    
        # Inner 3x3 black square
        for i in range(2, 5):
            for j in range(2, 5):
                self.modules[y + i][x + j] = True
    
    def get_module(self, x, y):
        """Get the state of a module at the given coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.modules[y][x]
        return False


def generate_qr_image(data, error_correction=QRCode.ERROR_CORRECT_M):
    """
    Generate a QR code and return it as a bitmap that can be rendered.
    
    NOTE: This is a simplified implementation. For production use on actual
    badges, you should either:
    1. Pre-generate QR codes offline and include them as PNG images
    2. Use a proper MicroPython QR library
    3. Call an API to generate QR codes
    
    Args:
        data (str): The data to encode
        error_correction (int): Error correction level
        
    Returns:
        tuple: (QRCode instance, size) or (None, 0) on error
    """
    try:
        qr = QRCode(data, error_correction)
        qr.make()
        return qr, qr.size
    except Exception as e:
        print(f"QR generation error: {e}")
        return None, 0
