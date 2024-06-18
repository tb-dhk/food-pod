import os
import torch
from ultralytics import YOLO
import yaml
from pathlib import Path

# Enable CUDA launch blocking for detailed error reporting
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

data_dir = Path("data")
data_config_path = data_dir / "data.yaml"

with open(data_config_path, 'r') as file:
    data_config = yaml.safe_load(file)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

epochs = 100
batch_size = 8
learning_rate = 0.001

model = YOLO("models/yolov8s.pt").to(device)

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# Add a function to verify data and labels
def verify_data_and_labels(data_config_path):
    with open(data_config_path, 'r') as file:
        data_config = yaml.safe_load(file)
    for i in range(len(data_config['train'])):
        train_dir = Path(data_config['train'][i])
        val_dir = Path(data_config['val'][i])
    
    for dir_path in [train_dir, val_dir]:
        for label_file in dir_path.glob('*.txt'):
            with open(label_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) != 5:
                        print(f"Incorrect label format in file {label_file}: {line.strip()}")
                        continue
                    class_id, x_center, y_center, width, height = map(float, parts)
                    if not (0 <= class_id < len(data_config['names'])):
                        print(f"Class ID {class_id} out of range in file {label_file}")
                    if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1):
                        print(f"Invalid bounding box values in file {label_file}: {line.strip()}")

verify_data_and_labels(data_config_path)

# Train the model
try:
    train_results = model.train(data=data_config_path, epochs=100, patience=5, imgsz=640, batch=batch_size, lr0=learning_rate, device=device, val=False)
    print("Training and Validation Completed!")
except RuntimeError as e:
    print(f"RuntimeError during training: {e}")
    raise

