#!/usr/bin/env python3
"""
Generate a 65x65 LinkedIn QR code in the proper colors for the badge.
Green on black to match the 2025 badge theme.
"""

import qrcode
from PIL import Image, ImageDraw
import os

# LinkedIn URL to encode
LINKEDIN_URL = "https://www.linkedin.com/in/chris-lynch-039363a/"

# QR Code settings
QR_SIZE = 65  # 65x65 pixels to match badge requirements
QR_VERSION = 1  # Start with version 1, will auto-adjust if needed
QR_ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_M  # Medium error correction
QR_BOX_SIZE = 1  # 1 pixel per module for exact 65x65 size
QR_BORDER = 0  # No border to maximize QR area

# Badge theme colors (green on black)
QR_GREEN_COLOR = (86, 211, 100)  # Green for QR modules
QR_BLACK_COLOR = (0, 0, 0)       # Black background

# Output file path
OUTPUT_PATH = "/Users/chris/repos/badger/badge/assets/linkedin_qr_65x65.png"

def generate_linkedin_qr():
    """Generate the LinkedIn QR code with exact specifications"""
    
    print(f"Generating QR code for: {LINKEDIN_URL}")
    print(f"Target size: {QR_SIZE}x{QR_SIZE} pixels")
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=QR_ERROR_CORRECTION,
        box_size=QR_BOX_SIZE,
        border=QR_BORDER,
    )
    
    # Add data and generate
    qr.add_data(LINKEDIN_URL)
    qr.make(fit=True)
    
    print(f"QR Version: {qr.version}")
    print(f"Modules: {qr.modules_count}x{qr.modules_count}")
    
    # Create image with custom colors
    img = qr.make_image(fill_color=QR_GREEN_COLOR, back_color=QR_BLACK_COLOR)
    
    # Ensure exact size by resizing if necessary
    if img.size != (QR_SIZE, QR_SIZE):
        print(f"Resizing from {img.size} to {QR_SIZE}x{QR_SIZE}")
        img = img.resize((QR_SIZE, QR_SIZE), Image.NEAREST)
    
    # Convert to RGB if not already
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Save the image
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, 'PNG')
    
    print(f"QR code saved to: {OUTPUT_PATH}")
    print(f"Final image size: {img.size}")
    print(f"Image mode: {img.mode}")
    
    # Verify the colors
    pixels = list(img.getdata())
    unique_colors = list(set(pixels))
    print(f"Colors in image: {unique_colors}")
    
    return OUTPUT_PATH

def test_qr_code():
    """Test the generated QR code by trying to decode it"""
    try:
        from pyzbar import pyzbar
        import cv2
        
        # Load and decode the image
        image = cv2.imread(OUTPUT_PATH)
        decoded_objects = pyzbar.decode(image)
        
        if decoded_objects:
            for obj in decoded_objects:
                print(f"Decoded data: {obj.data.decode('utf-8')}")
                print(f"QR type: {obj.type}")
                return True
        else:
            print("Warning: Could not decode QR code - may not be scannable")
            return False
            
    except ImportError:
        print("Note: Install pyzbar and opencv-python to test QR code scanning")
        print("pip install pyzbar opencv-python")
        return None

if __name__ == "__main__":
    # Generate the QR code
    output_file = generate_linkedin_qr()
    
    # Test if possible
    test_result = test_qr_code()
    
    print("\n" + "="*50)
    print("QR Code Generation Complete!")
    print(f"File: {output_file}")
    print("Ready to copy to badge device")
    
    if test_result is True:
        print("✅ QR code verified as scannable!")
    elif test_result is False:
        print("⚠️  QR code may have issues")
    else:
        print("ℹ️  Install test dependencies to verify scanning")