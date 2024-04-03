import yolov9_predict as y9p

model_path = 'best.pt'
image_path = 'test.png'

# Perform YOLOv9 prediction
license_plate = y9p.yolo_predict(model_path, image_path)


print(license_plate)