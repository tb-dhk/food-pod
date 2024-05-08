import yaml
from pathlib import Path
import torch
from ultralytics import YOLO

from tvt import redistribute_tvt

redistribute_tvt("./datasets/data/images/fast_food/popcorn_chicken/", 0.6, 0.3)

# Define data paths (modify these)
data_dir = Path("data")
data_config_path = data_dir / "data.yaml"  # Assuming your data configuration file (YAML) is here

# Load data configuration from YAML
with open(data_config_path, 'r') as file:
    data_config = yaml.safe_load(file)

# Extract train/val directories from data configuration
train_dir = Path(data_config['train'])
val_dir = Path(data_config['val'])

# Device configuration (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparameters (adjust these as needed)
epochs = 100
batch_size = 8
learning_rate = 0.001
validation_interval = 1  # Evaluate on validation set after each epoch

# Model loading
model = YOLO("yolov8s.pt").to(device)  # Replace 'yolov8s.pt' with your pre-trained weights file

# Initialize variables to track loss
prev_loss = float('inf')  # Initialize with a very large value
threshold_factor = 1.5  # 50% increase threshold

for epoch in range(epochs):
    # Training
    train_results = model.train(data=data_config_path, epochs=1, imgsz=640, batch=batch_size, lr0=learning_rate, device=device)

    # Validation
    if (epoch + 1) % validation_interval == 0:
        val_results = model.val(data=data_config_path, imgsz=640, batch=batch_size, device=device, single_cls=True)

        # Print validation results or perform other validation-related tasks

print("Training and Validation Completed!")

