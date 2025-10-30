# LinkedIn QR Code Setup for Badge App

This directory contains assets for the badge app, including the LinkedIn QR code.

## Quick Start

1. **Set your LinkedIn URL** in `/badge/secrets.py`:
   ```python
   LINKEDIN_URL = "https://www.linkedin.com/in/your-profile/"
   ```

2. **Generate the QR code** using the included script:
   ```bash
   cd badge/apps/badge
   pip install -r requirements.txt
   python3 generate_linkedin_qr.py
   ```
   
   The QR code will be generated in the `assets` directory automatically.

3. **Copy the generated QR code** to your badge:
   - Put your badge into disk mode (tap RESET twice)
   - Copy `linkedin_qr.png` to `/system/apps/badge/assets/` on the badge
   - Eject and reset your badge

## QR Code Generator Options

The generator script supports several options for customization:

```bash
# Basic usage (reads from secrets.py)
python3 generate_linkedin_qr.py

# Specify URL directly
python3 generate_linkedin_qr.py "https://www.linkedin.com/in/username/"

# Customize size (default: 60 pixels, optimal for badge display)
python3 generate_linkedin_qr.py --size 60

# Change error correction level (H is recommended for color displays)
python3 generate_linkedin_qr.py --error-correction H

# Skip URL shortening (use full URL)
python3 generate_linkedin_qr.py --no-shorten

# Custom output path
python3 generate_linkedin_qr.py --output /path/to/output.png
```

## Error Correction Levels

- **L** (Low): 7% correction - smallest QR code
- **M** (Medium): 15% correction - balanced
- **Q** (Quartile): 25% correction - good resilience
- **H** (High): 30% correction - **recommended for color badge** - best scanning reliability

## QR Code Display

The QR code will appear in the **bottom-right corner** of the badge display when:
- `LINKEDIN_URL` is set in `secrets.py`
- The QR code PNG exists in the `assets` directory
- The badge app is running

## Troubleshooting

**QR code not appearing on badge:**
- Verify `LINKEDIN_URL` is set in `/secrets.py` (not `/badge/secrets.py`)
- Check that `linkedin_qr.png` exists in `/system/apps/badge/assets/`
- Ensure the image is a valid PNG file
- Try regenerating the QR code

**QR code not scanning:**
- Try generating with `--error-correction H` (highest correction)
- Use a shorter URL or enable URL shortening
- Ensure good lighting when scanning
- Hold the scanner steady and at the right distance

**URL shortening fails:**
- The script will fall back to the original URL
- You can disable shortening with `--no-shorten`
- Check your internet connection

## Technical Details

- **Default size**: 60x60 pixels (optimal for 160x120 badge screen)
- **Position**: Bottom-right corner with 2px padding
- **Format**: PNG with black modules on white background
- **URL shortening**: Uses TinyURL API (free, no auth required)
