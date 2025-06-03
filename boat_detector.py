from ultralytics import YOLO
import cv2
import os

def boat_detector(model_path: str, photo_path: str, output_path: str):
    model = YOLO(model_path)
    results = model.predict(source=photo_path, conf=0.4)
    for r in results:
        im = r.plot()
        cv2.imwrite(output_path, im)