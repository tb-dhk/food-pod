# Data Preparation and Model Training

This project provides a streamlined way to prepare image data, augment it, split it into training and validation sets, and train a model using YOLO format annotations. The Makefile helps automate these steps.

## Prerequisites

Ensure you have the following installed:
- Python (version 3.6 or higher)
- Required Python packages (you can install them using `pip install -r requirements.txt`)
- Make

## Directory Structure

The output of `tree -d` should look like this:

```
datasets/
└── data/
    └── <food_category>/
        └── <food_name>/
            ├── images/
            │   ├── train/
            │   ├── val/
            │   └── test/
            └── boxes/
data/
└── data.yaml
```

## Setup

1. **Move Training Images**:
   Place your training images in a directory of your choice. This directory path will be used as `src_train_images`.

2. **Move Testing Images**:
   Place your testing images in a directory of your choice. This directory path will be used as `src_test_images`.

3. **Move Label Files**:
   Place your label files in a directory of your choice. This directory path will be used as `src_label_files`.

## Usage

To run the complete process, use the following command:

```sh
make category=<food_category> name=<food_name> ratio=<train_ratio> src_train_images=<path/to/train/images> src_test_images=<path/to/test/images> src_label_files=<path/to/label/files>
```

Replace the placeholders with your specific values:
- `<food_category>`: The category of the food (e.g., `fast_food`).
- `<food_name>`: The name of the food (e.g., `popcorn_chicken`).
- `<train_ratio>`: The ratio of images to use for training (e.g., `0.8` for 80% training and 20% validation).
- `<path/to/train/images>`: Path to the directory containing your training images.
- `<path/to/test/images>`: Path to the directory containing your testing images.
- `<path/to/label/files>`: Path to the directory containing your label files.

### Example

```sh
make category=fast_food name=popcorn_chicken ratio=0.8 src_train_images=./my_train_images src_test_images=./my_test_images src_label_files=./my_label_files
```

## Makefile Targets

- **move_train_images**: Moves training images to `./datasets/data/<food_category>/<food_name>/images/train`.
- **move_test_images**: Moves testing images to `./datasets/data/<food_category>/<food_name>/images/test`.
- **move_labels**: Moves label files to `./datasets/data/<food_category>/<food_name>/boxes`.
- **convert_and_augment**: Converts and augments the training images using `convert.py`.
- **split_images**: Splits the images between training and validation sets using `tv.py`.
- **train_model**: Trains the model using a specified YAML configuration file. Calls `update_yaml` to update paths in `data.yaml`.

## Customizing the Training Script

Ensure your `train.py` script is configured to read the paths from `data.yaml` and train the model accordingly.

## Updating data.yaml

The `train_model` target in the Makefile updates the `data.yaml` file with the correct paths:

```yaml
train: "<food_category>/<food_name>/images/train"
val: "<food_category>/<food_name>/images/val"
test: "<food_category>/<food_name>/images/test"
nc: 1
```

## Notes

- Ensure the images and labels are correctly formatted and placed in the respective directories before running the Makefile.
- Modify the `convert.py`, `tv.py`, and `train.py` scripts according to your specific requirements.

