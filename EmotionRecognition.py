# -*- coding: utf-8 -*-
"""emotion_recognization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JcaWDZDir6eZA-5Ox-fZ4QizicR_agRx
"""

#importing libraries
import os
# import cv2
import cv2
import numpy as np
import random
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelBinarizer

from google.colab import drive
drive.mount('/content/drive')

#Extracting images from library

BASE_PATH = "/content/drive/MyDrive/AI Project/Dataset"
NUM_CLASSES = 4

dataset_dir_list = os.listdir(BASE_PATH)
print(dataset_dir_list)

emotion_counts = {label: 0 for label in dataset_dir_list}

# get each emotion's label  and load the corresponding images also convert into grayscale images and resize images
list_data = []
list_label = []
brightness_alpha = 1.5
contrast_alpha = 1.5

for emotion_type in dataset_dir_list:
    img_list = os.listdir(BASE_PATH + '/' + emotion_type)
    print('Loaded the images of dataset-' + '{}\n'.format(emotion_type))
    for img in img_list:
        input_img = cv2.imread(BASE_PATH + '/' + emotion_type + '/' + img)
        # add brightness and contrast factor it increase brightness 50%

        input_img = cv2.convertScaleAbs(input_img, alpha=brightness_alpha, beta=0)
        input_img = cv2.convertScaleAbs(input_img, alpha=contrast_alpha, beta=0)
        # convert image into gray scale image
        input_img=cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
        # resize image
        input_img_resize = cv2.resize(input_img, (48, 48))
        list_data.append(input_img_resize)
        list_label.append(emotion_type)
        emotion_counts[emotion_type] += 1

# perform one-hot encoding on the labels
lb = LabelBinarizer()
labels = lb.fit_transform(list_label)
# labels = to_categorical(labels)
labels = np.array(labels)

print(len(list_data))
print(len(list_label))

img_data = np.array(list_data)
img_data = img_data.astype('float32')
img_data = img_data/255
print(img_data)
print(img_data.shape)

# Showing Sample images
fig, axes = plt.subplots(5, 5, figsize=(8, 8))
# Randomly select and display one image from each class
for i, ax in enumerate(axes.flat):
    class_folder = random.choice(dataset_dir_list)
    class_path = os.path.join(BASE_PATH, class_folder)
    images = os.listdir(class_path)
    image_name = random.choice(images)
    image_path = os.path.join(class_path, image_name)

    # Load and resize the image
    img = Image.open(image_path).convert('L')
    img = img.resize((48, 48))

    # Display the image
    ax.imshow(img, cmap = 'gray')
    ax.set_title(class_folder)
    ax.axis('off')

# Adjust the spacing between subplots
plt.tight_layout()

# Display the grid of images
plt.show()

# ploat Class distribution
plt.figure(figsize=(8, 4))
plt.bar(emotion_counts.keys(), emotion_counts.values())
plt.title('Distribution of Emotion Samples')
plt.xlabel('Emotion Labels')
plt.ylabel('Number of Samples')
print(emotion_counts.keys())
print(emotion_counts.values())

# Select and plot a few sample images and their pixel intensity distribution
min_value = 0
max_value = (len(list_data)-1)
num_numbers = 5
sample_indices = [random.randint(min_value, max_value) for _ in range(num_numbers)]


for i, sample_idx in enumerate(sample_indices):

    # Create a figure with two subplots
    fig, (img1, img2) = plt.subplots(1, 2, figsize=(5, 2))


    # for gray scale image intensity histogram
    if len(img_data[sample_idx].shape) == 2:
      img1.imshow(img_data[sample_idx], cmap='gray')
      img1.set_title(f'Emotion: {list_label[sample_idx]}')
      img1.axis('off')


      plt.hist(img_data[sample_idx].ravel(), bins=256, range=(0, 1), density=True, color='blue', alpha=0.7)
      img2.set_title('Pixel Intensity Distribution Histogram')
      img2.set_xlabel('Pixel Intensity')
      img2.set_ylabel('Frequency')

      plt.subplots_adjust(wspace=1)

    # for RGB color image intensity histogram
    elif len(img_data[sample_idx].shape)==3:
      # Split the image into Red, Green, and Blue channels
      image = cv2.imread(img_data[sample_idx])
      b, g, r = cv2.split(image)

      plt.hist(r.flatten(), bins=256, range=(0, 256), color='red', alpha=0.5, label='Red Channel')
      plt.hist(g.flatten(), bins=256, range=(0, 256), color='green', alpha=0.5, label='Green Channel')
      plt.hist(b.flatten(), bins=256, range=(0, 256), color='blue', alpha=0.5, label='Blue Channel')

    # Plot the pixel intensity distribution for RGB image histogram

      img2.set_xlabel('Pixel Intensity')
      img2.set_ylabel('Frequency')
      img2.set_title('RGB Channel Intensity Distribution')
      img2.legend()


      plt.subplots_adjust(wspace=1)

plt.show()

image = cv2.imread('/content/drive/MyDrive/AI Project/Dataset/bored/24819.jpg')

fig, (img1, img2) = plt.subplots(1, 2, figsize=(12, 5))

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img1.set_title(f'Emotion: bored')
img1.imshow(image_rgb)
img1.axis('off')


b, g, r = cv2.split(image)


# img2.figure(figsize=(6, 4))

# Plot histograms for each channel on the same graph
plt.hist(r.flatten(), bins=256, range=(0, 256), color='red', alpha=0.5, label='Red',align='right')
plt.hist(g.flatten(), bins=256, range=(0, 256), color='green', alpha=0.5, label='Green',align='mid')
plt.hist(b.flatten(), bins=256, range=(0, 256), color='blue', alpha=0.5, label='Blue',align='right')
plt.subplots_adjust(wspace=1)

# Set labels and titles
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.title('RGB Channel Intensity Distribution')
plt.legend()

plt.subplots_adjust(wspace=1)
# Show the histogram
plt.show()

