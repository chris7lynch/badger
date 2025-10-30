"""
LinkedIn QR Code Generator for Badge

This script generates a QR code PNG image from a LinkedIn URL.
The QR code can then be copied to the badge and displayed.

Usage:
1. Update the LINKEDIN_URL in your secrets.py or pass it as an argument
2. Run this script to generate linkedin_qr.png
3. Copy the generated PNG to your badge's /system/apps/badge/assets/ directory
"""

import qrcode
from PIL import Image
import os
import sys
import argparse


def shorten_url(long_url):
    """
    Shorten a URL using TinyURL API (no authentication required).
    
    Args:
        long_url (str): The URL to shorten
        
    Returns:
        str: Shortened URL, or original URL if shortening fails
    """
    if not long_url:
        return None
    
    try:
        import urllib.request
        import urllib.parse
        # Use TinyURL API (free, no auth required)
        api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
        with urllib.request.urlopen(api_url) as response:
            shortened = response.read().decode('utf-8').strip()
        
        # Validate the response
        if shortened and shortened.startswith('http'):
            print(f"URL shortened: {long_url} -> {shortened}")
            return shortened
        else:
            print(f"Shortening failed, using original URL")
            return long_url
    except Exception as e:
        print(f"URL shortening failed: {e}")
        print("Using original URL")
        return long_url


def generate_qr_code(url, size=60, output_path=None, error_correction='H', use_shortener=True):
    """
    Generate a QR code PNG image optimized for the badge color screen.
    
    Args:
        url (str): The URL to encode
        size (int): Size of the QR code in pixels (default: 60 for badge display)
        output_path (str): Path to save the PNG (default: ./linkedin_qr.png)
        error_correction (str): Error correction level - 'L', 'M', 'Q', or 'H' (default: 'H')
        use_shortener (bool): Whether to shorten the URL first (default: True)
        
    Returns:
        str: Path to the generated QR code image
    """
    if not url:
        raise ValueError("URL cannot be empty")
    
    # Shorten URL if requested
    if use_shortener:
        url = shorten_url(url)
    
    # Map error correction level
    error_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,  # 7% correction
        'M': qrcode.constants.ERROR_CORRECT_M,  # 15% correction
        'Q': qrcode.constants.ERROR_CORRECT_Q,  # 25% correction
        'H': qrcode.constants.ERROR_CORRECT_H,  # 30% correction - best for color displays
    }
    error_level = error_levels.get(error_correction.upper(), qrcode.constants.ERROR_CORRECT_H)
    
    # Create QR code with optimized settings for badge display
    qr = qrcode.QRCode(
        version=None,  # Auto-detect version based on data
        error_correction=error_level,
        box_size=10,  # Size of each QR code "box" in pixels
        border=2,     # Minimum border size (reduced for more compact QR)
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Generate the image
    img = qr.make_image(fill_color='black', back_color='white')
    
    # Resize to target size while maintaining aspect ratio
    img = img.resize((size, size), Image.Resampling.NEAREST)
    
    # Set output path
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "assets", "linkedin_qr.png")
    
    # Save the image
    img.save(output_path)
    print(f"QR code saved to: {output_path}")
    print(f"QR code size: {size}x{size} pixels")
    print(f"Encoded URL: {url}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Generate LinkedIn QR code for GitHub Universe 2025 badge'
    )
    parser.add_argument(
        'url',
        nargs='?',
        help='LinkedIn profile URL (e.g., https://www.linkedin.com/in/username/)'
    )
    parser.add_argument(
        '--size',
        type=int,
        default=60,
        help='QR code size in pixels (default: 60)'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: ./linkedin_qr.png)'
    )
    parser.add_argument(
        '--error-correction',
        choices=['L', 'M', 'Q', 'H'],
        default='H',
        help='Error correction level (default: H for best scanning on color displays)'
    )
    parser.add_argument(
        '--no-shorten',
        action='store_true',
        help='Do not shorten the URL before generating QR code'
    )
    
    args = parser.parse_args()
    
    # Get URL from arguments or try to import from secrets
    url = args.url
    if not url:
        try:
            # Try to import from parent directory's secrets.py
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
            from secrets import LINKEDIN_URL
            url = LINKEDIN_URL
        except (ImportError, AttributeError):
            print("Error: No URL provided and couldn't import from secrets.py")
            print("Please provide a LinkedIn URL as an argument or set LINKEDIN_URL in secrets.py")
            sys.exit(1)
    
    if not url:
        print("Error: LinkedIn URL is empty")
        sys.exit(1)
    
    try:
        generate_qr_code(
            url,
            size=args.size,
            output_path=args.output,
            error_correction=args.error_correction,
            use_shortener=not args.no_shorten
        )
    except Exception as e:
        print(f"Error generating QR code: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
