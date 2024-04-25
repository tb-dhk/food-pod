import csv
import json
import os
import sys
from pathlib import Path
import imgaug.augmenters as iaa
import numpy as np
import imgaug as ia
from PIL import Image

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

# Define augmentation functions for each category
geometric_transforms = {
    "rotation": ia.augmenters.Affine(rotate=(-45, 45)),
    "scaling": ia.augmenters.Affine(scale={"x": (0.5, 1.5), "y": (0.5, 1.5)}),
    "translation": ia.augmenters.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}),
    "shearing": ia.augmenters.Affine(shear=(-20, 20)),
    "perspective_transformations": ia.augmenters.PerspectiveTransform(scale=(0.01, 0.15)),
    "cropping_and_padding": ia.augmenters.CropAndPad(percent=(-0.1, 0.1))
}

flipping = {
    "horizontal_flip": ia.augmenters.Fliplr(1.0),
    "vertical_flip": ia.augmenters.Flipud(1.0)
}

color_space_manipulation = {
    "brightness_adjustment": ia.augmenters.MultiplyBrightness((0.5, 1.5)),
    "contrast_adjustment": ia.augmenters.GammaContrast((0.5, 2.0)),
    "saturation_adjustment": ia.augmenters.MultiplySaturation((0.5, 1.5)),
    "hue_adjustment": ia.augmenters.MultiplyHue((0.5, 1.5)),
    "color_channel_shifting": ia.augmenters.ChannelShuffle(p=1.0),
    "gamma_correction": ia.augmenters.GammaContrast((0.5, 2.0))
}

noise_injection = {
    "gaussian_noise": ia.augmenters.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.1*255)),
    "salt_and_pepper_noise": ia.augmenters.SaltAndPepper(0.05),
    "speckle_noise": ia.augmenters.Salt(0.05)
    # Add more noise injections as needed
}

blur_and_sharpen = {
    "gaussian_blur": ia.augmenters.GaussianBlur(sigma=(0.0, 3.0)),
    "average_blur": ia.augmenters.AverageBlur(k=(2, 7)),
    "median_blur": ia.augmenters.MedianBlur(k=(3, 11)),
    "bilateral_blur": ia.augmenters.BilateralBlur(d=(3, 10)),
    "sharpening": ia.augmenters.Sharpen(alpha=(0.0, 1.0), lightness=(0.75, 2.0))
}

distortion = {
    "elastic_deformations": ia.augmenters.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25),
    "piecewise_affine_transformations": ia.augmenters.PiecewiseAffine(scale=(0.01, 0.05)),
    "perspective_warping": ia.augmenters.PerspectiveTransform(scale=(0.01, 0.15))
}

augmenters_combining_multiple_techniques = {
    "sequential_augmentation": ia.augmenters.Sequential([
        ia.augmenters.Affine(rotate=(-45, 45)),
        ia.augmenters.Fliplr(0.5),
        ia.augmenters.MultiplyBrightness((0.5, 1.5))
    ]),
    # "someof_augmentation": ia.augmenters.SomeOf(2, [
    #     ia.augmenters.Affine(rotate=(-45, 45)),
    #     ia.augmenters.Fliplr(0.5),
    #     ia.augmenters.MultiplyBrightness((0.5, 1.5))
    # ]),
    # "oneof_augmentation": ia.augmenters.OneOf([
    #     ia.augmenters.Affine(rotate=(-45, 45)),
    #     ia.augmenters.Fliplr(0.5),
    #     ia.augmenters.MultiplyBrightness((0.5, 1.5))
    # ])
}

all_augmentations = {**geometric_transforms, **flipping, **color_space_manipulation,
                     **noise_injection, **blur_and_sharpen, **distortion,
                     **augmenters_combining_multiple_techniques}

augmentations_list = all_augmentations.keys()

def csv_to_yolo(yolo_dir):
    """
    Convert a CSV file containing bounding box annotations to YOLO format and apply augmentations.

    Args:
        yolo_dir (str): Directory where YOLO files will be saved.
    """
    labels_dir = os.path.join(yolo_dir, "labels")  # Create labels directory
    os.makedirs(labels_dir, exist_ok=True)  # Create directory if it doesn't exist
    images_dir = os.path.join(yolo_dir, "images")  # Images directory
    os.makedirs(images_dir, exist_ok=True)  # Create directory if it doesn't exist

    csv_file = find_latest_csv_downloads()

    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        return
    
    print(f"Processing CSV file: {csv_file}")

    # Dictionary to store bounding box information for each image
    image_bbox_dict = {}

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

    # Clear out existing augmented images
    for filename in os.listdir(images_dir):
        if "-aug" in filename:
            os.remove(os.path.join(images_dir, filename))

    # Clear out existing augmented YOLO files
    for filename in os.listdir(labels_dir):
        if "-aug" in filename:
            os.remove(os.path.join(labels_dir, filename))

    # Iterate through images and augmentations
    for filename, bounding_boxes in image_bbox_dict.items():
        print("starting", filename, bounding_boxes)
        # Load the image
        image_path = os.path.join(images_dir, filename)
        image = Image.open(image_path)

        # Apply augmentations
        augmentation_types = all_augmentations  # Add more augmentations here...
        for idx, aug_type in enumerate(augmentation_types):
            print("doing", aug_type)
            augmented_image = apply_augmentation(image, bounding_boxes, aug_type)

            # Save augmented image
            aug_image_filename = f"{os.path.splitext(filename)[0]}-aug{idx}.jpg"
            aug_image_path = os.path.join(images_dir, aug_image_filename)
            augmented_image.save(aug_image_path)

            # Save corresponding text file with YOLO format
            yolo_filename = os.path.join(labels_dir, os.path.splitext(filename)[0] + f"-aug{idx}.txt")
            with open(yolo_filename, 'w') as yolo_file:
                for box in bounding_boxes:
                    x_center = (box[0] + box[2]) / (2.0 * image.width)
                    y_center = (box[1] + box[3]) / (2.0 * image.height)
                    box_width = (box[2] - box[0]) / image.width
                    box_height = (box[3] - box[1]) / image.height
                    class_id = box[4]
                    yolo_file.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

    print("\n\nConversion and augmentation completed.\n\n")


def apply_augmentation(image, bounding_boxes, augmentation_name):
    """
    Apply the specified augmentation to the image and bounding boxes.

    Args:
        image (PIL.Image): The input image.
        bounding_boxes (list of tuples): List of bounding boxes in the format [(x_min, y_min, x_max, y_max), ...].
        augmentation_name (str): Name of the augmentation to apply.

    Returns:
        numpy.ndarray: The augmented image.
        list of tuples: List of augmented bounding boxes.
    """ 
    # Convert PIL image to numpy array
    image_np = np.array(image)

    # Check if the provided augmentation name is valid
    if augmentation_name not in all_augmentations:
        print("Invalid augmentation name. Available augmentations:")
        print(list(all_augmentations.keys()))
        return None 

    # Apply the selected augmentation to the image
    aug_function = all_augmentations[augmentation_name]
    augmented_image_np = aug_function(image=image_np)

    # Convert augmented image back to PIL format
    augmented_image_pil = Image.fromarray(augmented_image_np)

    # Convert bounding boxes to imgaug format (BoundingBoxesOnImage)
    bb_list = [ia.BoundingBox(x1=bb[0], y1=bb[1], x2=bb[2], y2=bb[3]) for bb in bounding_boxes]
    bbs = ia.BoundingBoxesOnImage(bb_list, shape=image_np.shape)

    # Apply the augmentation to the bounding boxes
    bbs_aug = aug_function(bounding_boxes=bbs)

    return augmented_image_pil 

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python script_name.py yolo_dir")
        sys.exit(1)

    # Get the output YOLO directory
    yolo_dir = sys.argv[1]

    # Call the function to convert CSV to YOLO format
    csv_to_yolo(yolo_dir)

