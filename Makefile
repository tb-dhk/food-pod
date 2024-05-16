# Makefile for data preparation and model training

# Define variables for food category, food name, and train ratio
FOOD_CATEGORY := $(category)
FOOD_NAME := $(name)
TRAIN_RATIO := $(ratio)

# Define variables for source paths
SRC_TRAIN_IMAGES := $(src_train_images)
SRC_TEST_IMAGES := $(src_test_images)
SRC_LABEL_FILES := $(src_label_files)

# Define the paths
BASE_DIR := ./datasets/data/$(FOOD_CATEGORY)/$(FOOD_NAME)
IMAGE_DIR := $(BASE_DIR)/images
TRAIN_DIR := $(IMAGE_DIR)/train
VAL_DIR := $(IMAGE_DIR)/val
TEST_DIR := $(IMAGE_DIR)/test
BOXES_DIR := $(BASE_DIR)/boxes
DATA_YAML := ./data/data.yaml

# Targets

# Move training images
.PHONY: move_train_images
move_train_images:
	mkdir -p $(TRAIN_DIR)
	mv $(SRC_TRAIN_IMAGES)/* $(TRAIN_DIR)

# Move testing images
.PHONY: move_test_images
move_test_images:
	mkdir -p $(TEST_DIR)
	mv $(SRC_TEST_IMAGES)/* $(TEST_DIR)

# Move label files
.PHONY: move_labels
move_labels:
	mkdir -p $(BOXES_DIR)
	mv $(SRC_LABEL_FILES)/* $(BOXES_DIR)

# Convert and augment training images
.PHONY: convert_and_augment
convert_and_augment:
	python3 convert.py $(BASE_DIR)

# Split images between train and val
.PHONY: split_images
split_images:
	python3 tv.py $(FOOD_CATEGORY) $(FOOD_NAME) $(TRAIN_RATIO)

# Update the data.yaml file
.PHONY: update_yaml
update_yaml:
	@echo "train: $(FOOD_CATEGORY)/$(FOOD_NAME)/images/train" > $(DATA_YAML)
	@echo "val: $(FOOD_CATEGORY)/$(FOOD_NAME)/images/val" >> $(DATA_YAML)
	@echo "test: $(FOOD_CATEGORY)/$(FOOD_NAME)/images/test" >> $(DATA_YAML)
	@echo "nc: 1" >> $(DATA_YAML)

# Default target
.PHONY: all
all: move_train_images move_test_images move_labels convert_and_augment split_images train_model
	@echo "All tasks completed."

# Usage: make category=fast_food name=popcorn_chicken ratio=0.8 src_train_images=path/to/train/images src_test_images=path/to/test/images src_label_files=path/to/label/files

