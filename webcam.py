from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows, imwrite
import cv2
import os
import time
import yolov9_predict as y9p

def takeSnapshot():
    try:
        # Initialize the camera
        cam = VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if s:    # Frame captured without any errors
            imshow("cam-test", img)
            key = waitKey(5000)  # Display the image for 5 seconds
            if key == 27:  # If ESC is pressed, exit
                destroyAllWindows()
                return None

            folder_name = 'cropped_plates'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            filename = os.path.join(folder_name, f'{round(time.time())}.jpg')
            imwrite(filename, img)  # Save image
            cam.release()  # Release the camera
            destroyAllWindows()
            return filename
        else:
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def camPredict(model_path='best.pt'):
    image_path = takeSnapshot() # Take a snapshot using the webcam
    if image_path is None:
        print(f'Unexpected error with the camera. {time.strftime("%Y-%m-%d %H:%M:%S")}')
        return None

    # Perform YOLOv9 prediction
    license_plate = y9p.yolo_predict(model_path, image_path)
    
    # If a license plate is detected, append it to the 'license_plates.txt' file
    if license_plate is not None:
        with open('license_plates.txt', 'a') as f:
            f.write(f'{license_plate}\n')
            print(f'License plate detected: {license_plate} at {time.strftime("%Y-%m-%d %H:%M:%S")}')
        return license_plate
    else:
        print(f'No license plate detected in image {time.strftime("%Y-%m-%d %H:%M:%S")}')
        return None
    
def plateScanner():
    while True:
        camPredict()
        time.sleep(15)  # Wait for 5 seconds before taking the next snapshot