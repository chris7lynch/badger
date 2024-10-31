import qrcode
from PIL import Image
import os

# URL to encode in the QR code
URL = "https://www.linkedin.com/in/chris-lynch-039363a/"
# Size of the QR code image (width and height in pixels)
SIZE = 150
# Path to save the generated QR code image
IMAGE_SAVE_PATH = os.path.join(os.path.dirname(__file__), "qr_code.png")

def generate_qr(url, size=150):
    """
    Generate a QR code with the given URL and size.

    :param url: The URL to encode in the QR code.
    :param size: The size of the QR code image (width and height in pixels).
    :return: An Image object containing the QR code.
    """
    try:
        # Create a QRCode object with the specified parameters
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Calculate the size of the QR code matrix and the size of each box
        matrix_size = qr.modules_count + 2 * qr.border
        box_size = size // matrix_size

        # Update the box size in the QRCode object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Generate the image
        img = qr.make_image(fill='black', back_color='white')
        return img

    except Exception as e:
        print(f"An error occurred while generating the QR code: {e}")
        return None

# Example usage
if __name__ == "__main__":
    qr_image = generate_qr(URL, SIZE)
    if qr_image:
        qr_image.save(IMAGE_SAVE_PATH)
    else:
        print("Failed to generate QR code.")
