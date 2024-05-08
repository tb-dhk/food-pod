import os
import shutil
import random

def redistribute_ttv(directory, train_ratio, test_ratio, val_ratio):
    # Check if train, test, and val directories exist. If not, create them.
    train_dir = os.path.join(directory, 'train')
    test_dir = os.path.join(directory, 'test')
    val_dir = os.path.join(directory, 'val')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    # Gather all files from train, test, and val directories
    all_files = []
    for dir_path in [train_dir, test_dir, val_dir]:
        all_files.extend([os.path.join(dir_path, file) for file in os.listdir(dir_path)])

    # Shuffle the list of all files
    random.shuffle(all_files)

    # Calculate the number of files to move for each directory
    total_files = len(all_files)
    train_count = int(train_ratio * total_files)
    test_count = int(test_ratio * total_files)

    # Move files to train directory
    for file in all_files[:train_count]:
        dst = os.path.join(train_dir, os.path.basename(file))
        shutil.move(file, dst)

    # Move files to test directory
    for file in all_files[train_count:train_count+test_count]:
        dst = os.path.join(test_dir, os.path.basename(file))
        shutil.move(file, dst)

    # Move files to val directory
    for file in all_files[train_count+test_count:]:
        dst = os.path.join(val_dir, os.path.basename(file))
        shutil.move(file, dst)

    print("Redistribution complete.")

# Example usage:
# redistribute_ttv('/path/to/directory', 0.7, 0.2, 0.1)

