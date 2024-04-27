import torch 
from pathlib import Path
from ultralytics import YOLO

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

# Model loading
model = YOLO("yolov8s.pt").to(device)  # Replace 'yolov8s.pt' with your pre-trained weights file

# Initialize variables to track loss
prev_loss = float('inf')  # Initialize with a very large value
threshold_factor = 1.5  # 50% increase threshold

# Training
results = model.train(data=data_config, epochs=70, imgsz=640, batch=batch_size, lr0=learning_rate, device=device)

print("Training Completed!")


