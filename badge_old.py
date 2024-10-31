import badger2040
import pngdec  # Add PNG decoder for QR code

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

LEFT_PADDING = 0
FIRST_NAME_HEIGHT = 0
LAST_NAME_HEIGHT = 22
PRONOUNS_HEIGHT = 48 # Placeholder
COMPANY_HEIGHT = 65
TITLE_HEIGHT = 85
GH_TAG_HEIGHT = 112
TEXT_WIDTH = WIDTH - LEFT_PADDING - 40  # Adjust width to leave space for QR code
LINE_SPACING = 2
DETAILS_TEXT_SIZE = 2
PRONOUNS_SIZE = 1

BADGE_PATH = "/badges/badge.txt"
QR_CODE_PATH = "/badges/linkedin_qr.png"  # Use LinkedIn QR code image

# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    display.set_pen(15)
    display.clear()
    
    # Draw the firstname, scaling it based on the available width
    display.set_pen(0)
    display.set_font("bitmap8")
    display.set_thickness(4)
    name_size = 3  # A sensible starting scale
    while True:
        name_length = display.measure_text(first_name, name_size)
        if name_length >= TEXT_WIDTH and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(first_name, LEFT_PADDING, FIRST_NAME_HEIGHT, TEXT_WIDTH, name_size)
            break

    # Draw the lastname, scaling it based on the available width
    display.set_pen(0)
    display.set_font("bitmap8")
    display.set_thickness(4)

    
    lastname_size = 3  # A sensible starting scale
    while True:
        lastname_length = display.measure_text(last_name, lastname_size)
        if lastname_length >= TEXT_WIDTH and lastname_size >= 0.1:
            lastname_size -= 0.01
        else:
            display.text(last_name, LEFT_PADDING, LAST_NAME_HEIGHT, TEXT_WIDTH, lastname_size)
            break

    # Draw the pronouns
    display.set_pen(0)
    display.set_font("bitmap8")
    display.text(pronouns, LEFT_PADDING, PRONOUNS_HEIGHT, TEXT_WIDTH, PRONOUNS_SIZE)

    # Draw the company and title, aligned to the bottom & truncated to fit on one line
    display.set_pen(0)
    display.set_font("bitmap8")
    
    # Company
    display.text(company, LEFT_PADDING, COMPANY_HEIGHT, TEXT_WIDTH, DETAILS_TEXT_SIZE)
    
    # Title
    display.text(title, LEFT_PADDING, TITLE_HEIGHT, TEXT_WIDTH, DETAILS_TEXT_SIZE)
    
    # GH Handle
    display.text(gh_tag, LEFT_PADDING, GH_TAG_HEIGHT, TEXT_WIDTH, DETAILS_TEXT_SIZE)

    # Draw the QR code on the right side
    try:
        png.open_file(QR_CODE_PATH)
        png.decode(WIDTH - 138, -10)  # Adjust position as needed
    except OSError:
        print("QR code error")
    
    display.update()

# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

# jpeg = jpegdec.JPEG(display.display)
png = pngdec.PNG(display.display)  # Initialize PNG decoder

# Open the badge file
DEFAULT_TEXT = """Universe 2024
Mona Lisa
Octocat
She/Her
GitHub
Company Mascot
@octocat
"""
try:
    badge = open(BADGE_PATH, "r")
except OSError:
    with open(BADGE_PATH, "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open(BADGE_PATH, "r")

# Read in the next 7 lines
try:
    event = badge.readline().strip()         # "Universe 2024"
    first_name = badge.readline().strip()    # "Mona Lisa"
    last_name = badge.readline().strip()     # "Octocat"
    pronouns = badge.readline().strip()      # "She/Her"
    company = badge.readline().strip()       # "GitHub"
    title = badge.readline().strip()         # "Company Mascot"
    gh_tag = badge.readline().strip()        # "@octocat"
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
