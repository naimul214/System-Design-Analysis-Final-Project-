import yolov9_predict as y9p
import webcam

def read_license_plate(model_path='best.pt', image_path='test.png'):
	# Perform YOLOv9 prediction
	license_plate = y9p.yolo_predict(model_path, image_path)


	print(license_plate)
	

#read_license_plate()

webcam.camPredict()