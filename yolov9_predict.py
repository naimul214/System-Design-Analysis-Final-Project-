import numpy as np
import cv2
from ultralytics import YOLO
from ocr import read_image
import time
import os
import zipfile

def yolo_predict(model_path, image_path):
    """
    Performs license plate detection using a YOLOv9 model and performs OCR on the cropped image.

    Args:
        model_path (str): Path to the YOLOv9 model weights file.
        image_path (str): Path to the image containing the license plate.
    Returns:
        str: The extracted license plate text, or None if no valid detections are found.
    """
    check_best_model() # Unzips the best.pt model if it doesn't exist

    # Load the YOLO model
    model = YOLO(model_path)

    # Perform object detection
    results = model(image_path)

    if results[0].boxes.xyxy.shape[0] == 0:  # Check for empty detection results (no license plate detected)
        print(f"No license plate detected in image {time.strftime('%Y-%m-%d %H:%M:%S')}")
        return None

    # Crop the image with the highest confidence bounding box
    cropped_image_path = crop_image(results, image_path)

    # Perform OCR on the cropped image
    license_plate_text = read_image(cropped_image_path)

    return license_plate_text



def crop_image(results, image_path):
    """
    Crop the image with the highest confidence bounding box from YOLOv9 detection results.

    Args:
        results (list): List of detection results returned by the YOLO model.
        image_path (str): Path to the image containing the license plate.

    Returns:
        str: Path to the cropped image.
    """
    # Extract bounding boxes and confidences from results
    boxes = results[0].boxes.xyxy.tolist()
    confidences = results[0].boxes.conf.tolist()

    # Find the index of the box with the highest confidence
    highest_conf_idx = np.argmax(confidences)
    highest_conf_box = boxes[highest_conf_idx]

    # Extract coordinates of the highest confidence box
    x1, y1, x2, y2 = highest_conf_box

    # Crop the image with the highest confidence bounding box
    img = cv2.imread(image_path)
    cropped_img = img[int(y1):int(y2), int(x1):int(x2)]

    # Find the folder to save cropped images
    cropped_folder = os.path.join(os.path.dirname(__file__), 'cropped_plates')

    # Generate the path for the cropped image inside the 'cropped_plates' folder
    cropped_image_path = os.path.join(cropped_folder, f'{time.time()}.jpg')

    cv2.imwrite(cropped_image_path, cropped_img)

    return cropped_image_path

def check_best_model():
  """
  Check if the best.pt YOLOv9c model file exists in the folder.
  If not, unzip the best.zip folder to extract the best.pt file.
  """
  # Get the directory of the current Python script
  script_dir = os.path.dirname(__file__)

  # Path to the best.pt file
  best_model_path = os.path.join(script_dir, 'best.pt')

  # Check if the best.pt file exists
  if not os.path.exists(best_model_path):
      print("best.pt model not found. Extracting from best.zip...")

      # Path to the best.zip file
      zip_file_path = os.path.join(script_dir, 'best.zip')

      # Check if the best.zip file exists
      if not os.path.exists(zip_file_path):
          print("best.zip not found. Please provide the best.pt model or the best.zip folder.")
          return

      # Unzip the best.zip folder
      with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
          zip_ref.extractall(script_dir)

      print("best.pt model extracted successfully.")