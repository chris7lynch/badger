import badger2040
import pngdec  # Add PNG decoder for QR code

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# Layout Constants

# Layout and sizing for your name on the badge
LEFT_PADDING = 0
FIRST_NAME_HEIGHT = 0
LAST_NAME_HEIGHT = 22
NAME_SIZE = 3

# Layout and sizing for your pronouns on the badge
PRONOUNS_HEIGHT = 48
PRONOUNS_SIZE = 1

# Layout and sizing for other details on the badge
COMPANY_HEIGHT = 65
TITLE_HEIGHT = 85
GH_TAG_HEIGHT = 112
LINE_SPACING = 2
DETAILS_TEXT_SIZE = 2

# Adjust width to leave space for QR code, used to truncate the text
TEXT_WIDTH = WIDTH - LEFT_PADDING - 40 

# Layout and sizing for the QR code
QR_CODE_X = WIDTH - 138
QR_CODE_Y = -10

# Path to the badge files for text and QR code data
BADGE_PATH = "/badges/badge.txt"
# The QR code must be approximately 150x150 pixels, and should be a PNG file
QR_CODE_PATH = "/badges/linkedin_qr.png"

# Font and Pen Settings
FONT = "bitmap8"
PEN_COLOR = 0
BACKGROUND_COLOR = 15
THICKNESS = 4

# ------------------------------
#      Drawing functions
# ------------------------------

def draw_text_with_truncation(text, x, y, max_width, initial_size):
    """
    Draws text on the display, truncating the size if it exceeds the maximum width.

    Args:
        text (str): The text to draw.
        x (int): The x-coordinate to start drawing.
        y (int): The y-coordinate to start drawing.
        max_width (int): The maximum width allowed for the text.
        initial_size (float): The initial size of the text.
    """
    try:
        display.set_pen(PEN_COLOR)
        display.set_font(FONT)
        display.set_thickness(THICKNESS)
        size = initial_size
        while True:
            length = display.measure_text(text, size)
            if length >= max_width and size >= 0.1:
                size -= 0.01  # Reduce the size slightly and re-measure
            else:
                display.text(text, x, y, max_width, size)  # Draw the text with the final size
                break
    except Exception as e:
        print(f"Error drawing text: {e}")

# Draw the badge, including user text
def draw_badge():
    try:
        display.set_pen(BACKGROUND_COLOR)
        display.clear()
        
        # Draw the firstname
        draw_text_with_truncation(first_name, LEFT_PADDING, FIRST_NAME_HEIGHT, TEXT_WIDTH, NAME_SIZE)

        # Draw the lastname
        draw_text_with_truncation(last_name, LEFT_PADDING, LAST_NAME_HEIGHT, TEXT_WIDTH, NAME_SIZE)

        # Draw the pronouns
        draw_text_with_truncation(pronouns, LEFT_PADDING, PRONOUNS_HEIGHT, TEXT_WIDTH, PRONOUNS_SIZE)

        # Draw the company
        draw_text_with_truncation(company, LEFT_PADDING, COMPANY_HEIGHT, TEXT_WIDTH, DETAILS_TEXT_SIZE)
        
        # Draw the title
        draw_text_with_truncation(title, LEFT_PADDING, TITLE_HEIGHT, TEXT_WIDTH, DETAILS_TEXT_SIZE)
        
        # Draw the GitHub handle
        draw_text_with_truncation(gh_tag, LEFT_PADDING, GH_TAG_HEIGHT, TEXT_WIDTH, DETAILS_TEXT_SIZE)

        # Draw the QR code on the right side
        try:
            png.open_file(QR_CODE_PATH)
            png.decode(QR_CODE_X, QR_CODE_Y)  # Adjust position as needed
        except OSError as e:
            print(f"QR code error: {e}")
        
        display.update()
    except Exception as e:
        print(f"Error drawing badge: {e}")

# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

# Initialize PNG decoder
png = pngdec.PNG(display.display)

# Open the badge file
DEFAULT_TEXT = """Mona Lisa
Octocat
She/Her
GitHub
Company Mascot
@octocat
"""
try:
    badge = open(BADGE_PATH, "r")
except OSError:
    try:
        with open(BADGE_PATH, "w") as f:
            f.write(DEFAULT_TEXT)
            f.flush()
        badge = open(BADGE_PATH, "r")
    except OSError as e:
        print(f"Error creating or opening badge file: {e}")
        badge = None

if badge:
    try:
        first_name = badge.readline().strip()    # "Mona Lisa"
        last_name = badge.readline().strip()     # "Octocat"
        pronouns = badge.readline().strip()      # "She/Her"
        company = badge.readline().strip()       # "GitHub"
        title = badge.readline().strip()         # "Company Mascot"
        gh_tag = badge.readline().strip()        # "@octocat"
    except Exception as e:
        print(f"Error reading badge file: {e}")
    finally:
        badge.close()

# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
