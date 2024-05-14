import yaml
from pathlib import Path
import torch
from ultralytics import YOLO, utils

from tt import redistribute_tt

redistribute_tt("./datasets/data/fast_food/popcorn_chicken/images", 0.8)

data_dir = Path("data")
data_config_path = data_dir / "data.yaml"

with open(data_config_path, 'r') as file:
    data_config = yaml.safe_load(file)

train_dir = Path(data_config['train'])
val_dir = Path(data_config['val'])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

epochs = 100
batch_size = 8
learning_rate = 0.001
validation_interval = 5
threshold_factor = 1.5  # Stop training if loss increases by this factor

model = YOLO("yolov8s.pt").to(device)

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

best_loss = float('inf')
best_model_state_dict = None

# Initialize prev_loss to a high value in the first epoch
prev_loss = float('inf')  

for epoch in range(epochs // 5):
    #print("epoch", epoch * 5, "to", epoch * 5 + 4)

    checkpoint_path = f"checkpoint_epoch_{epoch}.pt"
    if Path(checkpoint_path).is_file() and epoch and False: # loop closed
        checkpoint = torch.load(checkpoint_path)
        try:
            model.load_state_dict(checkpoint['model_state_dict'])
        except:
            print("model loading error.")
        prev_loss = checkpoint['loss']  # Update prev_loss from checkpoint if available
        learning_rate = checkpoint['learning_rate']
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        print(f"Loaded checkpoint from epoch {epoch}")

    #train_results = model.train(data=data_config_path, epochs=validation_interval, imgsz=640, batch=batch_size, lr0=learning_rate, device=device)

    checkpoint = {
        'model_state_dict': best_model_state_dict,  # Use best model state
        'optimizer_state_dict': optimizer.state_dict(),
        'learning_rate': learning_rate,
    }
    # torch.save(checkpoint, checkpoint_path)

train_results = model.train(data=data_config_path, epochs=100, patience=5, imgsz=640, batch=batch_size, lr0=learning_rate, device=device, val=False)

print("Training and Validation Completed!" if prev_loss is None else "Training stopped due to loss increase.")

