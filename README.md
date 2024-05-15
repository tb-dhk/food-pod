# data preparation and model training

this project helps you prepare image data, augment it, split it into training and validation sets, and train a model using yolo format annotations. the makefile automates these steps.

## prerequisites

ensure you have the following installed:
- python (version 3.6 or higher)
- required python packages (you can install them using `pip install -r requirements.txt`)
- make

## directory structure

the output of `tree -d` should look like this:

```
datasets/
└── data/
    └── <food_category>/
        └── <food_name>/
            ├── images/
            │   ├── train/
            │   ├── val/
            │   └── test/
            ├── labels/
            │   ├── train/
            │   └── val/
            └── boxes/
data/
└── data.yaml
```

## makefile targets

- **move_train_images**: moves training images to `./datasets/data/<food_category>/<food_name>/images/train`.
- **move_test_images**: moves testing images to `./datasets/data/<food_category>/<food_name>/images/test`.
- **move_labels**: moves label files to `./datasets/data/<food_category>/<food_name>/boxes`.
- **convert_and_augment**: converts and augments the training images using `convert.py`.
- **split_images**: splits the images between training and validation sets using `tv.py`.
- **train_model**: trains the model using a specified yaml configuration file. calls `update_yaml` to update paths in `data.yaml`.

## steps

### step 1: source images

collect images for your food category and food name. you should have separate sets of images for training and testing. place them in directories of your choice.

### step 2: annotate training images using vgg image annotator

use the [vgg image annotator (via)](https://www.robots.ox.ac.uk/~vgg/software/via/) to annotate objects in your training images. ensure that you label the correct file names and assign the correct classes to the annotated objects. 

when exporting the annotations from via, ensure that the output format matches the following:

- **csv format**: export the annotations as csv files.
- **annotation format**: each annotation should include the following information:
  - **image filename**: the filename of the annotated image.
  - **object identifier**: an identifier for the annotated object.
  - **attributes**: additional attributes associated with the annotation, such as shape, coordinates, and class id.
  - **bounding box coordinates**: the coordinates of the bounding box around the annotated object.
  - **class id**: the identifier or label assigned to the class of the annotated object.

make sure that the exported csv files contain accurate annotations for each image in your training dataset. the label files should accurately represent the objects present in the images and provide all necessary information for training your model.

note that label files are only required for training purposes and are thus not required for testing images.

### step 3: move training images

place your training images in a directory of your choice. this directory path will be used as `src_train_images`.

run the command:

```sh
make move_train_images category=<food_category> name=<food_name> src_train_images=<path/to/train/images>
```

### step 4: move testing images

place your testing images in a directory of your choice. this directory path will be used as `src_test_images`.

run the command:

```sh
make move_test_images category=<food_category> name=<food_name> src_test_images=<path/to/test/images>
```

### step 5: move label files

place your label files in a directory of your choice. this directory path will be used as `src_label_files`.

run the command:

```sh
make move_labels category=<food_category> name=<food_name> src_label_files=<path/to/label/files>
```

### step 6: convert and augment training images

convert and augment the training images using `convert.py`. this step uses the food category and food name to identify the correct directory.

run the command:

```sh
make convert_and_augment category=<food_category> name=<food_name>
```

### step 7: split images between train and validation sets

split the images into training and validation sets using `tv.py`. you need to provide the food category, food name, and the ratio of images to use for training.

run the command:

```sh
make split_images category=<food_category> name=<food_name> ratio=<train_ratio>
```

### step 8: train the model

train the model using the updated `data.yaml` file. this step also updates the paths in `data.yaml`.

run the command:

```sh
make train_model category=<food_category> name=<food_name>
```

### example

to run steps 3 to 8, use the following commands in order:

```sh
make move_train_images category=fast_food name=popcorn_chicken src_train_images=./my_train_images
make move_test_images category=fast_food name=popcorn_chicken src_test_images=./my_test_images
make move_labels category=fast_food name=popcorn_chicken src_label_files=./my_label_files
make convert_and_augment category=fast_food name=popcorn_chicken
make split_images category=fast_food name=popcorn_chicken ratio=0.8
make train_model category=fast_food name=popcorn_chicken
```

## updating data.yaml

the `train_model` target in the makefile updates the `data.yaml` file with the correct paths:

```yaml
train: "<food_category>/<food_name>/images/train"
val: "<food_category>/<food_name>/images/val"
test: "<food_category>/<food_name>/images/test"
nc: 1
```

## notes

- ensure the images and labels are correctly formatted and placed in the respective directories before running the makefile.
- modify the `convert.py`, `tv.py`, and `train.py` scripts according to your specific requirements.

