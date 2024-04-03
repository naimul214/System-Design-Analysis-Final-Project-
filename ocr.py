import easyocr

def read_image(image):
    """
    Opens an image file and reads the text using OCR.
    """
    # Initialize OCR reader
    reader = easyocr.Reader(['en'])  # Specify language(s)

    # Read text from the license plate image
    text = reader.readtext(image)

    # Access the extracted license plate text (assuming single detection)
    license_plate_text = text[0][1]

    return license_plate_text