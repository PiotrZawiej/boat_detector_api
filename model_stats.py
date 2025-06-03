from ultralytics import YOLO
import os
import time
import glob

model_path = r"runs\weights\best.pt" 
test_folder = r"boat\test"

model = YOLO(model_path)

image_paths = glob.glob(os.path.join(test_folder, "*.jpg"))

true_positives = 0
false_negatives = 0
total_images = 0  

start_time = time.time()

for img_path in image_paths:
    txt_path = os.path.splitext(img_path)[0] + ".txt"

    if not (os.path.exists(txt_path) and os.path.getsize(txt_path) > 0):
        continue  

    total_images += 1

    results = model.predict(source=img_path, conf=0.2, verbose=False)

    detected_boat = any(int(box.cls[0]) == 0 for r in results for box in r.boxes)

    if detected_boat:
        true_positives += 1
    else:
        false_negatives += 1

end_time = time.time()

if true_positives + false_negatives > 0:
    accuracy = true_positives / (true_positives + false_negatives)
else:
    accuracy = 0.0

print(f"True Positives: {true_positives}")
print(f"False Negatives: {false_negatives}")
print(f"Accuracy: {accuracy:.2%}")
print(f"Czas całkowity: {end_time - start_time:.2f} sekund")
