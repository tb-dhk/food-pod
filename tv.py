import os
import shutil
import random

def redistribute_tv(directory, train_ratio):
    # Check if train and validation directories exist. If not, create them.
    train_dir = os.path.join(directory, 'train')
    val_dir = os.path.join(directory, 'val')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    # Gather all image files from the original directory (excluding cache files)
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".cache") and "test" not in root:
                all_files.append(os.path.join(root, file))

    # Shuffle the list of all files
    random.shuffle(all_files)

    def find_label_file(image_file):
        # Replace 'images' with 'labels' in the image file path
        label_file = image_file.replace('/images/', '/labels/').replace('\\images\\', '\\labels\\')
        label_file = os.path.splitext(label_file)[0] + '.txt'
        
        # Get the parent directory of the image file
        parent_dir = os.path.dirname(image_file)

        # Extract the directory inside 'labels'
        label_dir = parent_dir.split(os.path.sep)[-1]

        # Derive the label file paths for train and validation directories
        train_label_file = label_file.replace(f'/labels/{label_dir}/', '/labels/train/')
        val_label_file = label_file.replace(f'/labels/{label_dir}/', '/labels/val/')

        print(train_label_file)
        if os.path.exists(train_label_file):
            return train_label_file
        elif os.path.exists(val_label_file):
            return val_label_file

    # Calculate the number of files for train and validation directories
    total_files = len([file for file in all_files if file.endswith(('.jpg', '.jpeg', '.png'))])
    train_count = int(train_ratio * total_files)
    val_count = total_files - train_count

    train_image_count = 0
    val_image_count = 0

    # Move files to train and validation directories
    for file in all_files:
        if file.endswith(('.jpg', '.jpeg', '.png')):
            if train_image_count < train_count:
                dst_img = os.path.join(train_dir, os.path.basename(file))
                train_image_count += 1
            elif val_image_count < val_count:
                dst_img = os.path.join(val_dir, os.path.basename(file))
                val_image_count += 1

            shutil.move(file, dst_img)

            label_file = find_label_file(file)
            dst_label = os.path.join(os.path.dirname(dst_img.replace("images", "labels")), os.path.basename(label_file))
            if not os.path.exists(os.path.dirname(dst_label)):
                os.makedirs(os.path.dirname(dst_label))
            shutil.move(label_file, dst_label)

    print("Redistribution complete.")

# Example usage:
# redistribute_tv('./datasets/data/images/fast_food/popcorn_chicken/', 0.6, 0.2)

