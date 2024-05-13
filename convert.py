import csv
import json
import os
import sys

image_bbox_dict = {}

def csv_to_yolo(yolo_dir):
    """
    Convert a CSV file containing bounding box annotations to YOLO format.

    Args:
        yolo_dir (str): Directory where YOLO files will be saved.
    """
    labels_dir = os.path.join(yolo_dir, "labels")  # Create labels directory
    os.makedirs(labels_dir, exist_ok=True)  # Create directory if it doesn't exist
    images_dir = os.path.join(yolo_dir, "images")  # Images directory
    os.makedirs(images_dir, exist_ok=True)  # Create directory if it doesn't exist

    csv_files = os.listdir(os.path.join(yolo_dir, "boxes"))

    for csv_file in csv_files:
        csv_file = os.path.join(yolo_dir, "boxes", csv_file)

        # Check if the CSV file exists
        if not os.path.isfile(csv_file):
            print(f"Error: File '{csv_file}' not found.")
            return
        
        print(f"Processing CSV file: {csv_file}")

        # Dictionary to store bounding box information for each image
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
                    x = int(region_shape_attributes['x'])
                    y = int(region_shape_attributes['y'])
                    width = int(region_shape_attributes['width'])
                    height = int(region_shape_attributes['height'])
                    x_max = x + width
                    y_max = y + height

                    # Add bounding box information to dictionary
                    if filename not in image_bbox_dict:
                        image_bbox_dict[filename] = []
                    image_bbox_dict[filename].append((x, y, x_max, y_max, region_attributes['class_id']))
                except json.JSONDecodeError:
                    print(f"Warning: Unable to parse JSON in row '{row}'")
                    continue
            print("csv file processed")

    # Clear out existing files
    for filename in os.listdir(labels_dir):
        os.remove(os.path.join(labels_dir, filename))

    # Iterate through images and create YOLO format files
    for filename, bounding_boxes in image_bbox_dict.items():
        print("starting", filename, bounding_boxes)

        yolo_filename = os.path.join(labels_dir, f"{os.path.splitext(filename)[0]}.txt")
        with open(yolo_filename, 'w') as yolo_file:
            for box in bounding_boxes:
                x_center = (box[0] + box[2]) / (2.0 * width)
                y_center = (box[1] + box[3]) / (2.0 * height)
                box_width = (box[2] - box[0]) / width
                box_height = (box[3] - box[1]) / height
                class_id = box[4]
                yolo_file.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

    print("\n\nConversion completed.\n\n")

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py yolo_dir")
        sys.exit(1)

    # Get the output YOLO directory
    yolo_dir = sys.argv[1]

    # Call the function to convert CSV to YOLO format
    csv_to_yolo(yolo_dir)

