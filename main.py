import yaml
from pathlib import Path
import torch
from ultralytics import YOLO

from tvt import redistribute_tvt

redistribute_tvt("./datasets/data/fast_food/popcorn_chicken/images", 0.6, 0.3)

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
    print("epoch", epoch * 5, "to", epoch * 5 + 4)

    checkpoint_path = f"checkpoint_epoch_{epoch}.pt"
    if Path(checkpoint_path).is_file():
        checkpoint = torch.load(checkpoint_path)
        try:
            model.load_state_dict(checkpoint['model_state_dict'])
        except:
            print("model loading error.")
        prev_loss = checkpoint['loss']  # Update prev_loss from checkpoint if available
        learning_rate = checkpoint['learning_rate']
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        print(f"Loaded checkpoint from epoch {epoch}")

    train_results = model.train(data=data_config_path, epochs=validation_interval, imgsz=640, batch=batch_size, lr0=learning_rate, device=device)

    val_results = model.eval()
    current_loss = val_results.get('val_loss')

    # Update best model if current validation loss is lower
    if current_loss < best_loss:
        best_loss = current_loss
        best_model_state_dict = model.state_dict()
        print(f"Found new best model with validation loss: {best_loss}")

    # Stop training if loss significantly increases
    if current_loss > threshold_factor * prev_loss:
        print(f"Training stopped due to significant loss increase! (Current: {current_loss}, Previous: {prev_loss})")
        print(f"Best model found at checkpoint: {checkpoint_path}")
        break

    checkpoint = {
        'model_state_dict': best_model_state_dict,  # Use best model state
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': prev_loss,
        'learning_rate': learning_rate,
    }
    torch.save(checkpoint, checkpoint_path)
    prev_loss = current_loss  # Update previous loss

print("Training and Validation Completed!" if prev_loss is None else "Training stopped due to loss increase.")

