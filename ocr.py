import easyocr
import os
import time
import re

def rename_image(image, detected_text):
    """
    Renames the image file based on the detected text.
    """
    # Remove spaces from the detected text to form the license plate number
    license_plate = detected_text.replace(' ', '')

    # Generate new filename with license plate and current timestamp
    timestamp = str(time.time()).replace('.', '')  # Convert timestamp to string
    new_filename = f"{license_plate}_{timestamp}.jpg"

    # Apply regex to remove symbols from the filename
    new_filename = re.sub(r'[^\w]', ' ', new_filename)

    # Directory to save renamed image
    save_directory = 'cropped_plates'

    # Ensure the directory exists, create if it doesn't
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Path to the new image file
    new_image_path = os.path.join(save_directory, new_filename)

    # Rename the image file
    os.rename(image, new_image_path)

    return new_filename

def read_image(image_path):
    """
    Opens an image file and reads the text using OCR.
    """
    # Initialize OCR reader
    reader = easyocr.Reader(['en'])  # Specify language(s)

    # Read text from the image
    text_data = reader.readtext(image_path)

    # Convert all detected text to a single string
    detected_text = ' '.join([result[1] for result in text_data])

    
    # Remove specific phrases if they appear in the string
    phrases_to_remove = ['ONTARIO', 'ONTARIQ', 'YOURS TO DISCOVER', 'A PLACE TO GROW']
    for phrase in phrases_to_remove:
        detected_text = detected_text.upper().replace(phrase.upper(), '')

    # Rename the image file based on the detected text
    renamed_filename = rename_image(image_path, detected_text)

    return detected_text