import csv
import json
import os
import sys
from pathlib import Path
import imgaug.augmenters as iaa
import numpy as np
import imgaug as ia
from PIL import Image

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

image_bbox_dict = {}

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

    # Clear out existing augmented images and label files in train, val, and directories
    for subset in ['train', 'val']:
        try:
            for filename in os.listdir(os.path.join(images_dir, subset)):
                if "-aug" in filename:
                    os.remove(os.path.join(images_dir, subset, filename))
        except:
            pass

        try:
            for filename in os.listdir(os.path.join(labels_dir, subset)):
                os.remove(os.path.join(labels_dir, subset, filename))
        except:
            pass

    # Iterate through images and augmentations
    for filename, bounding_boxes in image_bbox_dict.items():
        filename = filename.replace("jpeg", "jpg")
        print("starting", filename, bounding_boxes)
        # Load the image
        for subset in ['train', 'val']:
            image_path = os.path.join(images_dir, subset, filename)
            if os.path.exists(image_path):
                break
        else:
            print(f"Warning: Image '{filename}' not found in any subset.")
            continue
        
        image = Image.open(image_path)

        yolo_filename = os.path.join(labels_dir, subset, f"{os.path.splitext(filename)[0]}.txt")
        os.makedirs(os.path.dirname(yolo_filename), exist_ok=True)
        with open(yolo_filename, 'w') as yolo_file:
            for box in bounding_boxes:
                x_center = (box[0] + box[2]) / (2.0 * image.width)
                y_center = (box[1] + box[3]) / (2.0 * image.height)
                box_width = (box[2] - box[0]) / image.width
                box_height = (box[3] - box[1]) / image.height
                class_id = box[4]
                yolo_file.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

        # Apply augmentations
        augmentation_types = all_augmentations  # Add more augmentations here...
        for idx, aug_type in enumerate(augmentation_types):
            print("doing", aug_type)
            augmented_image = apply_augmentation(image, bounding_boxes, aug_type)

            # Save augmented image
            aug_image_filename = f"{os.path.splitext(filename)[0]}-aug{idx}.jpg"  # Update filename extension to 'jpg'
            aug_image_path = os.path.join(images_dir, subset, aug_image_filename)
            augmented_image.save(aug_image_path)

            # Save corresponding text file with YOLO format
            yolo_filename = os.path.join(labels_dir, subset, os.path.splitext(filename)[0] + f"-aug{idx}.txt")
            os.makedirs(os.path.dirname(yolo_filename), exist_ok=True)
            with open(yolo_filename, 'w') as yolo_file:
                for box in bounding_boxes:
                    x_center = (box[0] + box[2]) / (2.0 * image.width)
                    y_center = (box[1] + box[3]) / (2.0 * image.height)
                    box_width = (box[2] - box[0]) / image.width
                    box_height = (box[3] - box[1]) / image.height
                    class_id = box[4]
                    yolo_file.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

def apply_augmentation(image, bounding_boxes, augmentation_name):
    """
    Apply the specified augmentation to the image within the bounding boxes.

    Args:
        image (PIL.Image): The input image.
        bounding_boxes (list of tuples): List of bounding boxes in the format [(x_min, y_min, x_max, y_max), ...].
        augmentation_name (str): Name of the augmentation to apply.

    Returns:
        numpy.ndarray: The augmented image.
    """ 
    # Convert PIL image to numpy array
    image_np = np.array(image)

    # Check if the provided augmentation name is valid
    if augmentation_name not in all_augmentations:
        print("Invalid augmentation name. Available augmentations:")
        print(list(all_augmentations.keys()))
        return None 

    # Define the augmentation function
    aug_function = all_augmentations[augmentation_name]

    # Convert bounding boxes to imgaug format (BoundingBoxesOnImage)
    bb_list = [ia.BoundingBox(x1=bb[0], y1=bb[1], x2=bb[2], y2=bb[3]) for bb in bounding_boxes]
    bbs_aug = ia.BoundingBoxesOnImage(bb_list, shape=image_np.shape)

    # Apply the augmentation to each bounding box individually
    for bb_aug in bbs_aug:
        # Apply the selected augmentation to the image within the bounding box
        augmented_image_np = aug_function(image=image_np[bb_aug.y1_int:bb_aug.y2_int, bb_aug.x1_int:bb_aug.x2_int])
        # Overlay the augmented region onto the original image
        image_np[bb_aug.y1_int:bb_aug.y2_int, bb_aug.x1_int:bb_aug.x2_int] = augmented_image_np

    # Convert the modified image back to PIL format
    augmented_image_pil = Image.fromarray(image_np)

    return augmented_image_pil

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py yolo_dir")
        sys.exit(1)

    # Get the output YOLO directory
    yolo_dir = sys.argv[1]

    # Call the function to convert CSV to YOLO format
    csv_to_yolo(yolo_dir)
