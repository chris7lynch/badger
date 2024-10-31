# Instructions for Generating and Using a QR Code on your GitHub Universe Badger

![Example Badge Display](badge_with_qr_example.jpg)

## Step 1: Generate the QR Code (Optional)

1. Ensure you have the necessary Python packages installed:
    ```sh
    pip install -r ./examples/badge_with_qr/generate_qr/requirements.txt
    ```

2. Run the `generate_qr.py` script to generate a QR code:
    ```sh
    python generate_qr.py
    ```

3. This will create a `qr_code.png` file in the same directory. The script generates a very clear QR code without any image compression.

4. If you have your own QR code, ensure it is 150x150 pixels and name it to match the `QR_CODE_PATH` constant in the `badge.py` script.

## Step 2: Prepare the Badge Files

1. Create or update the `badge.txt` file with your personal information in the following format:
    ```plaintext
    FirstName
    LastName
    Pronouns
    Company Name
    Title
    @GitHub Handle
    ```

2. Ensure the `badge.py` script is updated to use the generated QR code and the new badge file name:
    ```python
    # Path to the badge files for text and QR code data
    BADGE_PATH = "/badges/badge.txt"
    # The QR code must be approximately 150x150 pixels, and should be a PNG file
    QR_CODE_PATH = "/badges/qr_code.png"
    ```

3. The `badge.py` script contains constants that handle font size and spacing:
    - `LEFT_PADDING`, `FIRST_NAME_HEIGHT`, `LAST_NAME_HEIGHT`, `NAME_SIZE`: Layout and sizing for your name on the badge.
    - `PRONOUNS_HEIGHT`, `PRONOUNS_SIZE`: Layout and sizing for your pronouns on the badge.
    - `COMPANY_HEIGHT`, `TITLE_HEIGHT`, `GH_TAG_HEIGHT`, `DETAILS_TEXT_SIZE`: Layout and sizing for other details on the badge.
    - `TEXT_WIDTH`: Adjust width to leave space for the QR code, used to truncate the text.
    - `QR_CODE_X`, `QR_CODE_Y`: Layout and sizing for the QR code.

## Step 3: Upload Files to Badger 2040

1. Connect your Badger 2040 to your computer.
2. Replace the existing `badge.py` in the `examples` folder with the updated `badge.py` file.
3. Upload the following files to the `badges` folder on your Badger 2040:
    - `badge.txt`
    - `qr_code.png`

## Step 4: Run the Badge Script

1. On your Badger 2040, navigate to the `examples` folder.
2. Run the `badge.py` script to display your badge with the QR code.

You should now see your badge displayed on the Badger 2040 with your personal information and the generated QR code.

## Explanation of the `badge.py` Script

### Constants Section

- **Font Size and Spacing**: Constants like `LEFT_PADDING`, `FIRST_NAME_HEIGHT`, `LAST_NAME_HEIGHT`, `NAME_SIZE`, etc., control the layout and sizing of text elements on the badge.
- **Badge and QR Code Paths**: `BADGE_PATH` and `QR_CODE_PATH` specify the location of the badge text file and the QR code image.

### Functions

- **`draw_text_with_truncation`**: This function draws text on the display, truncating the size if it exceeds the maximum width. It ensures that the text fits within the specified area without overflowing.
- **`draw_badge`**: This function handles the drawing of all badge elements, including the name, pronouns, company, title, GitHub handle, and QR code. It uses the `draw_text_with_truncation` function to draw text elements and handles the QR code drawing separately.

### Main Script Flow

1. **Program Setup**: Initializes the Badger display and PNG decoder.
2. **Reading Badge File**: Opens and reads the `badge.txt` file to extract personal information.
3. **Drawing the Badge**: Calls the `draw_badge` function to render the badge on the display.
4. **Main Loop**: Keeps the display alive and halts the Badger to save power when on battery.

By following these instructions, you can customize and display your badge with a QR code on the Badger 2040.