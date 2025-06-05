import os
import shutil
import random

source_folder = r"boat"           
labels_folder = os.path.join(source_folder, "labels") 

train_folder = os.path.join(source_folder, "train")
valid_folder = os.path.join(source_folder, "valid")
test_folder = os.path.join(source_folder, "test")

# Tworzenie folderów, jeśli nie istnieją
os.makedirs(train_folder, exist_ok=True)
os.makedirs(valid_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

valid_ext = ('.jpg', '.jpeg', '.png')

# Pobranie listy obrazów w folderze źródłowym
images = [f for f in os.listdir(source_folder)
          if f.lower().endswith(valid_ext)
          and os.path.isfile(os.path.join(source_folder, f))]

# Losowe wymieszanie listy obrazów
random.shuffle(images)

# Określenie indeksów dla podziału (70% dla treningu, 15% dla walidacji, 15% dla testów)
split_train = int(len(images) * 0.7)
split_valid = int(len(images) * 0.85)  # 70% + 15%

train_images = images[:split_train]
valid_images = images[split_train:split_valid]
test_images = images[split_valid:]

# Funkcja do przenoszenia obrazów i odpowiadających im etykiet
def move_with_label(image_name, dest_folder):
    base_name, _ = os.path.splitext(image_name)
    label_name = base_name + '.txt'

    # Ścieżki źródłowe i docelowe dla obrazu
    image_src = os.path.join(source_folder, image_name)
    image_dest = os.path.join(dest_folder, image_name)

    shutil.move(image_src, image_dest)

    # Przenoszenie odpowiadającej etykiety, jeśli istnieje
    label_src = os.path.join(labels_folder, label_name)
    label_dest = os.path.join(dest_folder, label_name)

    if os.path.exists(label_src):
        shutil.move(label_src, label_dest)
    else:
        print(f"Brak etykiety dla: {label_name}")

# Przenoszenie obrazów i etykiet do odpowiednich folderów
for img in train_images:
    move_with_label(img, train_folder)

for img in valid_images:
    move_with_label(img, valid_folder)

for img in test_images:
    move_with_label(img, test_folder)

print("Podział danych zakończony.")
