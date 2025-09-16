from ultralytics import YOLO
import cv2

model = YOLO("yolov8n-seg.pt")
result = model("/Container/cpr_app/uploads/debug/test.png",save=True)


image = result[0].plot()
cv2.imwrite("/Container/cpr_app/test_segmentation/result.jpg",image)