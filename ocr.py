import easyocr
import os
import time

def rename_image(image, detected_text):
    """
    Renames the image file based on the detected text.
    """
    # Remove spaces from the detected text to form the license plate number
    license_plate = detected_text.replace(' ', '')

    # Generate new filename with license plate and current timestamp
    timestamp = str(time.time()).replace('.', '')  # Convert timestamp to string
    new_filename = f"{license_plate}_{timestamp}.jpg"

    # Directory to save renamed image
    save_directory = 'cropped_plates'

    # Ensure the directory exists, create if it doesn't
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Path to the new image file
    new_image_path = os.path.join(save_directory, new_filename)

    # Check if the new filename already exists
    if os.path.exists(new_image_path):
        # If the filename already exists, add a suffix to make it unique
        new_filename = f"{license_plate}_{timestamp}_1.jpg"
        new_image_path = os.path.join(save_directory, new_filename)

    # Rename the image file
    os.rename(image, new_image_path)

    return new_filename

def read_image(image):
    """
    Opens an image file and reads the text using OCR.
    """
    # Initialize OCR reader
    reader = easyocr.Reader(['en'])  # Specify language(s)

    # Read text from the image
    text_data = reader.readtext(image)

    # Convert all detected text to a single string
    detected_text = ' '.join([result[1] for result in text_data])

    # Remove the word 'ontario' if it appears in the string
    detected_text = detected_text.replace('ONTARIO', '')

    # Rename the image file based on the detected text
    renamed_filename = rename_image(image, detected_text)

    return detected_text