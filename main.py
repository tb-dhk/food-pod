import yaml
from pathlib import Path
import torch
from ultralytics import YOLO

from tvt import redistribute_tvt

redistribute_tvt("./datasets/data/fast_food/popcorn_chicken/images", 0.6, 0.3)

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
validation_interval = 5  # Evaluate on validation set after each epoch

# Model loading
model = YOLO("yolov8s.pt").to(device)  # Replace 'yolov8s.pt' with your pre-trained weights file

# Initialize optimizer
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# Initialize variables to track loss
prev_loss = float('inf')  # Initialize with a very large value
threshold_factor = 1.5  # 50% increase threshold

for epoch in range(epochs//5):
    print("epoch", epoch * 5, "to", epoch * 5 + 4)
    
    # Load model from the latest checkpoint
    checkpoint_path = f"checkpoint_epoch_{epoch}.pt"
    if Path(checkpoint_path).is_file():
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        prev_loss = checkpoint['loss']
        learning_rate = checkpoint['learning_rate']
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        print(f"Loaded checkpoint from epoch {epoch}")
    
    # Training
    train_results = model.train(data=data_config_path, epochs=validation_interval, imgsz=640, batch=batch_size, lr0=learning_rate, device=device)

    # Validation
    val_results = model.val(data=data_config_path, imgsz=640, batch=batch_size, device=device, single_cls=True)

        # Print validation results or perform other validation-related tasks
        
    # Save model to checkpoint
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': prev_loss,
        'learning_rate': learning_rate,
        # Add other relevant information to the checkpoint if needed
    }
    torch.save(checkpoint, checkpoint_path)

print("Training and Validation Completed!")

