
import csv
import json
import os
import sys
from pathlib import Path
import shutil

def find_latest_csv_downloads():
    """
    Find the latest modified CSV file in the ~/Downloads directory.

    Returns:
        str: Path to the latest modified CSV file.
    """
    downloads_dir = Path.home() / "Downloads"
    csv_files = list(downloads_dir.glob("*.csv"))
    if not csv_files:
        print("Error: No CSV files found in ~/Downloads directory.")
        sys.exit(1)
    latest_csv_file = max(csv_files, key=os.path.getmtime)
    return str(latest_csv_file)

def csv_to_yolo(yolo_dir):
    """
    Convert a CSV file containing bounding box annotations to YOLO format.

    Args:
        yolo_dir (str): Directory where YOLO files will be saved.
    """
    labels_dir = os.path.join(yolo_dir, "labels")  # Create labels directory
    os.makedirs(labels_dir, exist_ok=True)  # Create directory if it doesn't exist
    images_dir = os.path.join(yolo_dir, "images")
    print(os.listdir(images_dir))

    csv_file = find_latest_csv_downloads()

    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return
    
    print(f"Processing CSV file: {csv_file}")

    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                # Get the filename
                filename = row['filename']
                
                # Parse region_shape_attributes and region_attributes as dictionaries
                region_shape_attributes = json.loads(row['region_shape_attributes'])
                region_attributes = json.loads(row['region_attributes'])

                # Get bounding box coordinates
                x_min = int(region_shape_attributes['x'])
                y_min = int(region_shape_attributes['y'])
                width = int(region_shape_attributes['width'])
                height = int(region_shape_attributes['height'])
                x_max = x_min + width
                y_max = y_min + height

                # Normalize coordinates
                img_width = int(row['file_size'])
                img_height = int(row['file_size'])
                x_center = (x_min + x_max) / (2.0 * img_width)
                y_center = (y_min + y_max) / (2.0 * img_height)
                box_width = width / img_width
                box_height = height / img_height

                # Check if 'class_id' exists in region_attributes
                if 'class_id' in region_attributes:
                    class_id = region_attributes['class_id']
                else:
                    # If 'class_id' is missing, skip this row or assign a default value
                    print(f"Warning: 'class_id' not found for row '{row}'")
                    continue

                # Write YOLO format data to file
                yolo_filename = os.path.join(labels_dir, os.path.splitext(filename)[0] + ".txt")
                with open(yolo_filename, 'a') as yolo_file:
                    yolo_file.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

                # Copy image to the images directory
                image_path = os.path.join(images_dir, filename)
                if not os.path.isfile(image_path):
                    print(f"Error: Image '{filename}' not found in '{images_dir}'.")
            except json.JSONDecodeError:
                print(f"Warning: Unable to parse JSON in row '{row}'")
                continue

    print("\n\nConversion completed.\n\n")

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python script_name.py yolo_dir")
        sys.exit(1)

    # Get the output YOLO directory
    yolo_dir = sys.argv[1]

    # Call the function to convert CSV to YOLO format
    csv_to_yolo(yolo_dir)

