# food pod ai model

the food pod ai model is designed to detect food items within the food pod, facilitating efficient waste sorting and management. this readme.md provides comprehensive documentation for the data preparation, model training, and usage of the ai model.

## prerequisites

ensure you have the following installed:
- python (version 3.6 or higher)
- required python packages (you can install them using `pip install -r requirements.txt`)
- make

## directory structure

the directory structure should resemble the following:

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

## steps

### step 1: source images

collect images for your food category and food name. ensure you have separate sets of images for training and testing. place them in directories of your choice.

### step 2: annotate training images using vgg image annotator

annotate objects in your training images using the [vgg image annotator (via)](https://www.robots.ox.ac.uk/~vgg/software/via/). export the annotations as csv files. ensure that the annotations contain accurate information about the annotated objects, including filename, object identifier, attributes, bounding box coordinates, and class id. the exported csv files should match the specified format.

### step 3: move training images

place your training images in a directory of your choice. use the following command to move the training images:

```sh
make move_train_images category=<food_category> name=<food_name> src_train_images=<path/to/train/images>
```

### step 4: move testing images

place your testing images in a directory of your choice. use the following command to move the testing images:

```sh
make move_test_images category=<food_category> name=<food_name> src_test_images=<path/to/test/images>
```

### step 5: move label files

place your label files in a directory of your choice. use the following command to move the label files:

```sh
make move_labels category=<food_category> name=<food_name> src_label_files=<path/to/label/files>
```

### step 6: convert and augment training images

convert and augment the training images using `convert.py`. use the following command:

```sh
make convert_and_augment category=<food_category> name=<food_name>
```

### step 7: split images between train and validation sets

split the images into training and validation sets using `tv.py`. use the following command:

```sh
make split_images category=<food_category> name=<food_name> ratio=<train_ratio>
```

### step 8: train the model

train the model using the updated `data.yaml` file. use the following command:

```sh
make train_model category=<food_category> name=<food_name>
```

## updating data.yaml

the `train_model` target in the makefile updates the `data.yaml` file with the correct paths.

```yaml
train: "<food_category>/<food_name>/images/train"
val: "<food_category>/<food_name>/images/val"
test: "<food_category>/<food_name>/images/test"
nc: 1
```

## notes

- ensure the images and labels are correctly formatted and placed in the respective directories before running the makefile.
- modify the `convert.py`, `tv.py`, and `train.py` scripts according to your specific requirements.

## food pod ai model documentation

### purpose

the food pod ai model detects food items within the food pod, aiding in waste sorting and management.

### use cases

- food waste management systems
- environmental monitoring in food establishments
- smart city initiatives for waste reduction

### dataset

trained on images of food due to the scarcity of food waste images.

### architecture

based on yolov8 architecture, optimized for real-time food item detection.

### training

- data augmentation: utilized 24 different augmentation techniques for enhanced model robustness.
- specialized training: focused on food-related images to adapt the model for food waste detection.

### inference

```python
# load the yolo model
model = yolo(model_weights_file)

# perform inference on images
results = model(image_paths)
for result in results:
    result.show()
```

### note

for optimal performance, deploy the model in environments with sufficient lighting and minimal occlusion.
