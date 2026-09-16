import os
import shutil
import random
import kagglehub
from ultralytics import YOLO


dataset_path = kagglehub.dataset_download(
    "ismailnasri20/driver-drowsiness-dataset-ddd"
)

print("Dataset downloaded to:")
print(dataset_path)

# Find the main DDD folder
ddd_folder = os.path.join(
    dataset_path,
    "Driver Drowsiness Dataset (DDD)"
)

drowsy_folder = os.path.join(ddd_folder, "Drowsy")
non_drowsy_folder = os.path.join(ddd_folder, "Non Drowsy")

# Check folders
if not os.path.isdir(drowsy_folder):
    raise FileNotFoundError(f"Missing folder: {drowsy_folder}")

if not os.path.isdir(non_drowsy_folder):
    raise FileNotFoundError(f"Missing folder: {non_drowsy_folder}")

# -----------------------------
# 2. Create YOLO classification dataset
# -----------------------------
output = "drowsiness_dataset"

if os.path.exists(output):
    shutil.rmtree(output)

for split in ["train", "val"]:
    os.makedirs(os.path.join(output, split, "Drowsy"))
    os.makedirs(os.path.join(output, split, "Non Drowsy"))

random.seed(42)

def split_images(source, class_name):
    images = [
        f for f in os.listdir(source)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))
    ]

    random.shuffle(images)

    split_index = int(len(images) * 0.8)

    train_images = images[:split_index]
    val_images = images[split_index:]

    print(f"{class_name}: {len(images)} images")
    print(f"  Train: {len(train_images)}")
    print(f"  Val:   {len(val_images)}")

    for filename in train_images:
        shutil.copy2(
            os.path.join(source, filename),
            os.path.join(output, "train", class_name, filename)
        )

    for filename in val_images:
        shutil.copy2(
            os.path.join(source, filename),
            os.path.join(output, "val", class_name, filename)
        )


split_images(drowsy_folder, "Drowsy")
split_images(non_drowsy_folder, "Non Drowsy")

print("\nDataset preparation complete!")

model = YOLO("yolo11n-cls.pt")

model.train(
    data=output,
    epochs=10,
    imgsz=224,
    batch=32,
    device="cpu",
    workers=2
)

print("\nTraining complete!")
