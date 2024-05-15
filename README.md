# Data Preparation and Model Training

This project helps you prepare image data, augment it, split it into training and validation sets, and train a model using YOLO format annotations. The Makefile automates these steps.

## Prerequisites

Ensure you have the following installed:
- Python (version 3.6 or higher)
- Required Python packages (you can install them using `pip install -r requirements.txt`)
- Make

## Directory Structure

Your project directory should look like this:

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
convert.py
tv.py
train.py
Makefile
README.md
```

## Steps

### Step 1: Source Images

Collect images for your food category and food name. You should have separate sets of images for training and testing. Place them in directories of your choice.

### Step 2: Annotate Training Images Using VGG Image Annotator

Use the [VGG Image Annotator (VIA)](https://www.robots.ox.ac.uk/~vgg/software/via/) to create label files for your training images. Export the annotations as CSV files. Note that testing images do not require label files.

### Step 3: Move Training Images

Place your training images in a directory of your choice. This directory path will be used as `src_train_images`.

Run the command:

```sh
make move_train_images category=<food_category> name=<food_name> src_train_images=<path/to/train/images>
```

### Step 4: Move Testing Images

Place your testing images in a directory of your choice. This directory path will be used as `src_test_images`.

Run the command:

```sh
make move_test_images category=<food_category> name=<food_name> src_test_images=<path/to/test/images>
```

### Step 5: Move Label Files

Place your label files in a directory of your choice. This directory path will be used as `src_label_files`.

Run the command:

```sh
make move_labels category=<food_category> name=<food_name> src_label_files=<path/to/label/files>
```

### Step 6: Convert and Augment Training Images

Convert and augment the training images using `convert.py`. This step uses the food category and food name to identify the correct directory.

Run the command:

```sh
make convert_and_augment category=<food_category> name=<food_name>
```

### Step 7: Split Images Between Train and Validation Sets

Split the images into training and validation sets using `tv.py`. You need to provide the food category, food name, and the ratio of images to use for training.

Run the command:

```sh
make split_images category=<food_category> name=<food_name> ratio=<train_ratio>
```

### Step 8: Train the Model

Train the model using the updated `data.yaml` file. This step also updates the paths in `data.yaml`.

Run the command:

```sh
make train_model category=<food_category> name=<food_name>
```

### Example

To run the complete process, use the following commands in order:

```sh
make move_train_images category=fast_food name=popcorn_chicken src_train_images=./my_train_images
make move_test_images category=fast_food name=popcorn_chicken src_test_images=./my_test_images
make move_labels category=fast_food name=popcorn_chicken src_label_files=./my_label_files
make convert_and_augment category=fast_food name=popcorn_chicken
make split_images category=fast_food name=popcorn_chicken ratio=0.8
make train_model category=fast_food name=popcorn_chicken
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

