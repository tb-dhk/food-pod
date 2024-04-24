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

# Training
results = model.train(data=data_config, epochs=epochs, imgsz=640, batch=batch_size, lr0=learning_rate, device=device)
# Print training results (optional)
# print(results)  # Uncomment to print detailed training results

# Testing (optional)
# Replace 'path/to/image.jpg' with the path to your test image
# results = model('path/to/image.jpg')
# Print inference results (optional)
# print(results)  # Uncomment to print detailed inference results

print("Training and Testing Completed!")

