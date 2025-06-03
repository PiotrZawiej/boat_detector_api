import os
import shutil
import random

source_folder = r"boat"           
labels_folder = os.path.join(source_folder, "labels") 

train_folder = os.path.join(source_folder, "train")
test_folder = os.path.join(source_folder, "test")

os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

valid_ext = ('.jpg', '.jpeg', '.png')
images = [f for f in os.listdir(source_folder)
          if f.lower().endswith(valid_ext)
          and os.path.isfile(os.path.join(source_folder, f))]

random.shuffle(images)
split_index = int(len(images) * 0.7)
train_images = images[:split_index]
test_images = images[split_index:]

def move_with_label(image_name, dest_folder):
    base_name, _ = os.path.splitext(image_name)
    label_name = base_name + '.txt'

    image_src = os.path.join(source_folder, image_name)
    image_dest = os.path.join(dest_folder, image_name)

    shutil.move(image_src, image_dest)

    label_src = os.path.join(labels_folder, label_name)
    label_dest = os.path.join(dest_folder, label_name)

    if os.path.exists(label_src):
        shutil.move(label_src, label_dest)
    else:
        print(f"Wrong label: {label_name}")

for img in train_images:
    move_with_label(img, train_folder)

for img in test_images:
    move_with_label(img, test_folder)

print("end")
