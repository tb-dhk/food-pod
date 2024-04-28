import torch
from pathlib import Path
from ultralytics import YOLO
from sklearn.model_selection import train_test_split

# Define data paths (modify these)
data_dir = Path("data")
data_config = data_dir / "data.yaml"  # Assuming your data configuration file (YAML) is here
image_dir = data_dir / "images" / "fast_food" / "popcorn_chicken" / "images"
label_dir = data_dir / "images" / "fast_food" / "popcorn_chicken" / "labels"

# Device configuration (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparameters (adjust these as needed)
epochs = 100
batch_size = 8
learning_rate = 0.001

# Split the dataset into train/validation/test sets
image_files = sorted(image_dir.glob("*.jpg"))
label_files = sorted(label_dir.glob("*.txt"))
train_images, test_images, train_labels, test_labels = train_test_split(image_files, label_files, test_size=0.2, random_state=42)
train_images, val_images, train_labels, val_labels = train_test_split(train_images, train_labels, test_size=0.25, random_state=42)

# Model loading
model = YOLO("yolov8s.pt").to(device)  # Replace 'yolov8s.pt' with your pre-trained weights file

# Initialize variables to track loss
prev_loss = float('inf')  # Initialize with a very large value
threshold_factor = 1.5  # 50% increase threshold

# Training
train_results = model.train(data=data_config, epochs=epochs, imgsz=640, batch=batch_size, lr0=learning_rate, device=device, train_path=train_images, label_path=train_labels)
val_results = model.train(data=data_config, epochs=1, imgsz=640, batch=batch_size, lr0=learning_rate, device=device, train_path=val_images, label_path=val_labels, single_cls=True)

print("Training and Validation Completed!")

