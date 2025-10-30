"""
QR Code utilities for badge app
Handles loading and displaying pre-generated QR code images
"""
import gc
from badgeware import Image, file_exists


# Path to the pre-generated LinkedIn QR code
QR_CODE_PATH = "/system/apps/badge/assets/linkedin_qr.png"


def load_qr_code():
    """
    Load the pre-generated LinkedIn QR code PNG.
    
    Returns:
        Image: The loaded QR code image, or None if not found
    """
    try:
        if file_exists(QR_CODE_PATH):
            img = Image.load(QR_CODE_PATH)
            return img
        else:
            print(f"QR code not found at {QR_CODE_PATH}")
            return None
    except Exception as e:
        print(f"Error loading QR code: {e}")
        return None
    finally:
        gc.collect()

