
import torch
from torch.utils.data import DataLoader
from torch.optim import Adam

from yolov8 import Dataset as YOLOv8Dataset  # Assuming Ultralytics YOLOv8 library
from yolov8 import COCOEval  # Assuming you have COCOEval for evaluation (optional)


def train_model(model, image_dir, label_dir, epochs, batch_size, learning_rate, device):
  """
  Trains a YOLOv8 model on a given dataset.

  Args:
      model: YOLOv8 model object.
      image_dir: Path to the directory containing images.
      label_dir: Path to the directory containing labels (e.g., YOLO format txt files).
      epochs: Number of training epochs.
      batch_size: Batch size for training.
      learning_rate: Learning rate for the optimizer.
      device: Device to use for training (CPU or GPU).
  """

  # Create YOLOv8 dataset object
  dataset = YOLOv8Dataset(root=image_dir, label_dir=label_dir, img_size=416)  # Adjust img_size if needed

  # Create data loader
  data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

  # Define optimizer
  optimizer = Adam(model.parameters(), lr=learning_rate)

  # Training loop
  for epoch in range(epochs):
    model.train()  # Set model to training mode
    for images, targets in data_loader:
      images, targets = images.to(device), targets.to(device)

      # Forward pass, calculate loss
      loss = model(images, targets)[0]  # Assuming loss is the first element in model output

      # Backward pass, update weights
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

    print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

  # Save the trained model (optional)
  # torch.save(model.state_dict
