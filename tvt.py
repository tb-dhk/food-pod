
import os
import shutil
import random

def redistribute_tvt(directory, train_ratio, val_ratio):
    # Check if train, val, and test directories exist. If not, create them.
    train_dir = os.path.join(directory, 'train')
    val_dir = os.path.join(directory, 'val')
    test_dir = os.path.join(directory, 'test')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Gather all files from train, val, and test directories
    all_files = []
    for dir_path in [train_dir, val_dir, test_dir]:
        all_files.extend([os.path.join(dir_path, file) for file in os.listdir(dir_path)])

    # Shuffle the list of all files
    random.shuffle(all_files)

    # Calculate the number of files to move for each directory
    total_files = len(all_files)
    train_count = int(train_ratio * total_files)
    val_count = int(val_ratio * total_files)

    # Move image files and corresponding label files to train directory
    for file in all_files[:train_count]:
        dst_img = os.path.join(train_dir, os.path.basename(file))
        shutil.move(file, dst_img)
        move_corresponding_label(file, train_dir, directory)

    # Move image files and corresponding label files to val directory
    for file in all_files[train_count:train_count+val_count]:
        dst_img = os.path.join(val_dir, os.path.basename(file))
        shutil.move(file, dst_img)
        move_corresponding_label(file, val_dir, directory)

    # Move image files and corresponding label files to test directory
    for file in all_files[train_count+val_count:]:
        dst_img = os.path.join(test_dir, os.path.basename(file))
        shutil.move(file, dst_img)
        move_corresponding_label(file, test_dir, directory)

    print("Redistribution complete.")

def move_corresponding_label(image_file, dest_dir, root_directory):
    # Extract the file name without extension
    filename = os.path.splitext(os.path.basename(image_file))[0]
    
    # Find the corresponding label file in labels directory
    labels_dir = root_directory.replace("images", "labels") 
    for subdir, _, files in os.walk(labels_dir):
        for file in files:
            if file.startswith(filename) and file.endswith('.txt'):
                src_label = os.path.join(subdir, file)
                dst_label = os.path.join(dest_dir.replace("images", "labels"), file)
                shutil.move(src_label, dst_label)
                print(f"Moved {src_label} to {dst_label} (label)")
                return

# Example usage:
# redistribute_ttv('./datasets/data/images/fast_food/popcorn_chicken/', 0.6, 0.2)

