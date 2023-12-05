# -*- coding: utf-8 -*-
"""emotion_recognization_ApplicationMode.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c0cI7JsN8aZO6mK5AQowH5-nN6uffz5M
"""

import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
import torch.utils.data as td
from torchvision import datasets, transforms
from torchsummary import summary
import cv2
import os
import numpy as np
import torch.cuda as cuda
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance

from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import KFold



#for Evaluation
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score

from google.colab import drive
drive.mount('/content/drive')

!unzip "/content/drive/MyDrive/AI_Project/Dataset_Gender.zip"

!unzip "/content/drive/MyDrive/AI_Project/Age.zip"

device = "cpu"
if (cuda.is_available()):
    device = "cuda"

class CNN_Varient_1(nn.Module):
  def __init__(self,num_classes,kernel_size):
    self.kernel_size = kernel_size
    self.padding =1
    self.num_classes = num_classes


    #Initialize the parent class
    super(CNN_Varient_1,self) .__init__()


    self.conv_layer = nn.Sequential(

      #convolution layer-1
      nn.Conv2d(in_channels=1, out_channels=64, kernel_size=self.kernel_size, padding=1),
      nn.LeakyReLU(inplace=True),
      nn.Conv2d(in_channels=64, out_channels=64, kernel_size=self.kernel_size, padding=1),
      nn.LeakyReLU(inplace=True),
      nn.MaxPool2d(kernel_size=2, stride=2),

      #convolution layer -2
      nn.Conv2d(in_channels=64, out_channels=128, kernel_size=self.kernel_size, padding=1),
      nn.LeakyReLU(inplace=True),
      nn.Conv2d(in_channels=128, out_channels=128, kernel_size=self.kernel_size, padding=1),
      nn.LeakyReLU(inplace=True),
      nn.MaxPool2d(kernel_size=2, stride=2),

      # convolution layer 3
      nn.Conv2d(in_channels=128, out_channels=256, kernel_size=self.kernel_size, padding=1),
      nn.LeakyReLU(inplace=True),
      nn.Conv2d(in_channels=256, out_channels=256, kernel_size=self.kernel_size, padding=1),
      nn.LeakyReLU(inplace=True),
      nn.MaxPool2d(kernel_size=2, stride=2),

      )

    self.fc_layer = nn.Sequential(

      nn.Linear(9216 , 1024),
      nn.ReLU(inplace=True),
      nn.Dropout(p=0.5),

      nn.Linear(1024, 512),
      nn.ReLU(inplace=True),
      nn.Dropout(p=0.5),
      nn.Linear(512, self.num_classes),




    )
  def forward(self, x):
      # conv layers
      x = self.conv_layer(x)
      # flatten
      x = x.view(x.size(0), -1)
      # fc layer
      x = self.fc_layer(x)
      return x


model1_1 = CNN_Varient_1(kernel_size=3,num_classes=4).to(device)
# print(model1)

# if cuda.is_available():
#   model1_1 = model1_1.cuda()

summary(model1_1, (1, 48, 48))

model_path = '/content/drive/MyDrive/AI_Project/Saved_model/main_model.pth'
if cuda.is_available():
  loaded_model = CNN_Varient_1(kernel_size=3,num_classes=4).to(device)
  loaded_model.load_state_dict(torch.load(model_path))
else:
  loaded_model = CNN_Varient_1(kernel_size=3,num_classes=4).to(device)
  loaded_model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))

loaded_model.eval()

# for param in model.parameters():
#   print(param)



def preprocess_images(test_image_path):
  test_image = cv2.imread(test_image_path)
  test_image=cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
  test_image = cv2.resize(test_image, (48, 48))

  test_img_data = np.array(test_image)
  test_img_data = test_img_data.astype('float32')
  test_img_data = test_img_data/255

  input_image = torch.from_numpy(test_img_data)

  input_image = input_image.unsqueeze(0)


  input_image = input_image.repeat(1, 1, 1, 1)
  # print(input_image.shape)
  return input_image

def predict_class(preprocessed_input_image):

  with torch.no_grad():
    output = loaded_model(preprocessed_input_image)
  _, predicted = torch.max(output.data, 1)

  class_map = {0 : "angry", 1: "bored",2: "neutral",3: "focused"}
  predicted_class_index = int(predicted.item())

  predicted_class_name = class_map.get(predicted_class_index)
  print("Pridicted_class:",predicted_class_name)
  return predicted_class_name

#for pridicting single image

test_image_path = '/content/drive/MyDrive/AI_Project/focused_1.jpg'
preprocessed_input_image = preprocess_images(test_image_path)
Predicted_output= predict_class(preprocessed_input_image)

img = Image.open(test_image_path).convert('L')
img = img.resize((48, 48))

plt.figure(figsize=(1.5, 1.5))
plt.imshow(img, cmap = 'gray')
plt.title(f"true='focused', pred='{Predicted_output}'",fontsize=7)
plt.axis('off')

plt.show()

images = ['angry_1.jpg','angry_3.jpg','angry_2.jpg','focused_2.jpg','bored_2.jpg','bored_3.jpg','neutral_1.jpg','neutral_2.jpg','neutral_3.jpg','focused_1.jpg']
true_label = ["angry","angry","angry","focused","bored","bored","neutral","neutral","neutral","focused"]

# Showing Sample images for testing
fig, axes = plt.subplots(2, 5, figsize=(9, 4))

for i, ax in enumerate(axes.flat):
  # for i,image in enumarate(images):
    BASE_PATH = "/content/drive/MyDrive/AI_Project/"
    test_image_path = BASE_PATH + images[i]
    # print(test_image_path)
    preprocessed_input_image = preprocess_images(test_image_path)
    Predicted_output= predict_class(preprocessed_input_image)
    # print(Predicted_output)

    img = Image.open(test_image_path).convert('L')
    img = img.resize((48, 48))

    # Display the image
    ax.imshow(img, cmap = 'gray')
    ax.set_title(f"true='{true_label[i]}', pred='{Predicted_output}'",fontsize=7)
    ax.axis('off')

# Adjust the spacing between subplots
plt.tight_layout()
plt.subplots_adjust(wspace=0.6)
# Display the grid of images
plt.show()



"""**PART : 3**"""

# model

class CNN(nn.Module):
  def __init__(self,num_classes=4,kernel_size=3,padding=1):

    #Initialize the parent class
    super(CNN,self) .__init__()


    #Convolution Layers
    self.features = nn.Sequential(

        #convolution layer 1
        nn.Conv2d(in_channels=1,out_channels=64 ,kernel_size=kernel_size,padding=padding),
        nn.ReLU(inplace=True),
        nn.Conv2d(in_channels =64, out_channels=64,kernel_size = kernel_size,padding =padding),
        nn.ReLU(inplace = True),
        nn.MaxPool2d(kernel_size=2,stride=2),

        #convolution layer 2
        nn.Conv2d(in_channels=64, out_channels=128 ,kernel_size=kernel_size,padding=padding),
        nn.ReLU(inplace=True),
        nn.Conv2d(in_channels =128, out_channels=128,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.MaxPool2d(kernel_size=2,stride=2),

        #convolution layer 3
        nn.Conv2d(in_channels=128, out_channels=256 ,kernel_size=kernel_size,padding=padding),
        nn.ReLU(inplace=True),
        nn.Conv2d(in_channels =256, out_channels=256,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.Conv2d(in_channels =256, out_channels=256,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.Conv2d(in_channels =256, out_channels=256,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.MaxPool2d(kernel_size=2,stride=2),

        #convolution layer 4
        nn.Conv2d(in_channels=256, out_channels=512 ,kernel_size=kernel_size,padding=padding),
        nn.ReLU(inplace=True),
        nn.Conv2d(in_channels =512, out_channels=512,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.Conv2d(in_channels =512, out_channels=512,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.Conv2d(in_channels =512, out_channels=512,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.MaxPool2d(kernel_size=2,stride=2),

        #convolution layer 5
        nn.Conv2d(in_channels=512, out_channels=512 ,kernel_size=kernel_size,padding=padding),
        nn.ReLU(inplace=True),
        nn.Conv2d(in_channels =512, out_channels=512,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.Conv2d(in_channels =512, out_channels=512,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.Conv2d(in_channels =512, out_channels=512,kernel_size = kernel_size,padding = padding),
        nn.ReLU(inplace = True),
        nn.MaxPool2d(kernel_size=2,stride=2)

    )

    #Fully connected Layers

    self.avgpool = nn.AdaptiveAvgPool2d((7,7))
    self.classifier = nn.Sequential(
        nn.Linear(512* 7*7,4096),
        nn.ReLU(inplace=True),
        nn.Dropout(0.5),

        nn.Linear(4096,4096),
        nn.ReLU(inplace = True),
        nn.Dropout(0.5),
        nn.Linear(4096,num_classes),

    )
  def forward(self,x):
      # conv layers
    x = self.features(x)

    x = self.avgpool(x)

      #flatten
    # x = torch.flatten(x,1)
    x = x.view(x.size(0), -1)

      #fc layer
    x = self.classifier(x)



    return x



#Instantiate the Model
model = CNN(num_classes=4,kernel_size=3).to(device)

# if cuda.is_available():
#   model = model.cuda()

# print(model)

summary(model, (1, 48, 48))

model_path = '/content/drive/MyDrive/AI_Project/Saved_model/Varient_1.pth'
if cuda.is_available():
  loaded_model1 = CNN(kernel_size=3,num_classes=4).to(device)
  loaded_model1.load_state_dict(torch.load(model_path))
else:
  loaded_model1 = CNN(kernel_size=3,num_classes=4).to(device)
  loaded_model1.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
loaded_model1.eval()

# for param in model.parameters():
#   print(param)

#check accuracy on testing data
def find_accuracy1():
  true_labels_list = []
  predicted_labels_list = []

  loaded_model1.eval()
  with torch.no_grad():
    correct = 0
    total =0

    for i,(images,labels) in enumerate(dataset_loader):
      images = images.squeeze()
      images = images.unsqueeze(0)
      images = images.squeeze(0).unsqueeze(1)



      true_labels_list.extend(labels.numpy())
      images = images.to(device)
      labels = labels.to(device)
      # if cuda.is_available():
      #   images = images.cuda()
      #   labels = labels.cuda()

      # true.append(labels)
      outputs = loaded_model1(images)
      _,predicted = torch.max(outputs.data,1)

      predicted_labels_list.extend(predicted.cpu().numpy())
      total += labels.size(0)
      correct += (predicted == labels).sum().item()
    print("correct",correct)
    print("total",total)
    print('Test Accuracy of the model on the test images: {} %'.format((correct / total) * 100))

  return true_labels_list,predicted_labels_list





def find_P_R_A_F1_main(true_label,predicted_label,model_name):

  print(f'Evaluation of {model_name} on Testing Data :')
  pre_macro = precision_score(true_label, predicted_label, average='macro')
  pre_micro = precision_score(true_label, predicted_label, average='micro')
  print(f'Precision_macro: {pre_macro:.4f}')
  print(f'precision_micro: {pre_micro:.4f}')

  recall_macro = recall_score(true_label, predicted_label, average='macro')
  recall_micro = recall_score(true_label, predicted_label, average='micro')
  print(f'Recall_macro: {recall_macro:.4f}')
  print(f'recall_micro: {recall_micro:.4f}')

  accuracy = accuracy_score(true_label, predicted_label)
  print(f'Accuracy: {accuracy:.4f}')

  f1_macro = f1_score(true_label, predicted_label,average='macro')
  print(f'F1-Measure_macro: {f1_macro:.4f}')

  f1_micro = f1_score(true_label, predicted_label,average='micro')
  print(f'F1-Measure_micro: {f1_micro:.4f}')
  return pre_macro,pre_micro,recall_macro,recall_micro,accuracy,f1_macro,f1_micro

"""**bias on Gender**"""

def Collect_data_gender(base_path):

  dataset_dir_list = os.listdir("/content/drive/MyDrive/AI_Project/Dataset")
  gender = ['male', 'female']

  male_images = []
  female_images = []
  male_labels = []
  female_labels = []
  brightness_alpha = 1.5
  contrast_alpha = 1.5

  for emotion_label, emotion in enumerate(dataset_dir_list):
    for gender_label, g in enumerate(gender):
          folder_path = os.path.join(base_path, emotion, 'Gender', g)
          image_list = []
          for img_file in os.listdir(folder_path):

              img_path = os.path.join(folder_path, img_file)

              # input_img = preprocess_images(img_path)
              input_img = cv2.imread(img_path)

              # # Preprocess each image before adding it to the list
              input_img = cv2.convertScaleAbs(input_img, alpha=brightness_alpha, beta=0)
              input_img = cv2.convertScaleAbs(input_img, alpha=contrast_alpha, beta=0)
              # # convert image into gray scale image
              input_img=cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
              # # resize image
              input_img_resize = cv2.resize(input_img, (48, 48))

              # Add the preprocessed image to the corresponding lists
              if g == 'male':
                male_images.append(np.array(input_img_resize))
                male_labels.append(emotion_label)
              elif g == 'female':
                female_images.append(np.array(input_img_resize))
                female_labels.append(emotion_label)



  return male_images,male_labels,female_images,female_labels


BASE_PATH_gender = "/content/Dataset_Gender/Dataset"
male_images, male_labels, female_images, female_labels = Collect_data_gender(BASE_PATH_gender)

male_images = np.array(male_images)
male_images = male_images.astype('float32')
male_images = male_images/255

male_labels = np.array(male_labels)
male_labels = male_labels.astype('float32')

#training and testing split and train and test loader

def dataset_split_and_loader(img_data,img_label,batch_size,shuffle = False):


  X_train = img_data
  Y_train =  img_label

  X_train = np.array(X_train,'float32')
  Y_train = np.array(Y_train,'float32')



  X_train = X_train.reshape(X_train.shape[0], 48, 48, 1)
  # X_test = X_test.reshape(X_test.shape[0], 48, 48, 1)
  # X_val = X_val.reshape(X_val.shape[0],48,48,1)


  #creating data loaders for training and testing
  X_train = torch.from_numpy(X_train)
  Y_train = torch.from_numpy(Y_train)

  print("x_train:",X_train.shape)
  print("y_train:",Y_train.shape)


  train_dataset = td.TensorDataset(X_train, Y_train)
  train_loader = td.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True,pin_memory=True)

  return train_loader

# # Merge male and female data and labels
# img_data_gender = np.concatenate((male_images, female_images), axis=0)
# img_label_gender = np.concatenate((male_labels, female_labels), axis=0)

#check accuracy on testing data
def find_accuracy():
  true_labels_list = []
  predicted_labels_list = []

  loaded_model.eval()
  with torch.no_grad():
    correct = 0
    total =0

    for i,(images,labels) in enumerate(dataset_loader):
      images = images.squeeze()
      images = images.unsqueeze(0)
      images = images.squeeze(0).unsqueeze(1)



      true_labels_list.extend(labels.numpy())
      images = images.to(device)
      labels = labels.to(device)
      # if cuda.is_available():
      #   images = images.cuda()
      #   labels = labels.cuda()

      # true.append(labels)
      outputs = loaded_model(images)
      _,predicted = torch.max(outputs.data,1)

      predicted_labels_list.extend(predicted.cpu().numpy())
      total += labels.size(0)
      correct += (predicted == labels).sum().item()
    print("correct",correct)
    print("total",total)
    print('Test Accuracy of the model on the test images: {} %'.format((correct / total) * 100))

  return true_labels_list,predicted_labels_list

#check accuracy on testing data
def find_accuracy1():
  true_labels_list = []
  predicted_labels_list = []

  loaded_model1.eval()
  with torch.no_grad():
    correct = 0
    total =0

    for i,(images,labels) in enumerate(dataset_loader):
      images = images.squeeze()
      images = images.unsqueeze(0)
      images = images.squeeze(0).unsqueeze(1)



      true_labels_list.extend(labels.numpy())
      images = images.to(device)
      labels = labels.to(device)
      # if cuda.is_available():
      #   images = images.cuda()
      #   labels = labels.cuda()

      # true.append(labels)
      outputs = loaded_model1(images)
      _,predicted = torch.max(outputs.data,1)

      predicted_labels_list.extend(predicted.cpu().numpy())
      total += labels.size(0)
      correct += (predicted == labels).sum().item()
    print("correct",correct)
    print("total",total)
    print('Test Accuracy of the model on the test images: {} %'.format((correct / total) * 100))

  return true_labels_list,predicted_labels_list

def evalution(true_label,predicted_label):
  accuracy = accuracy_score(true_label, predicted_label)
  precision = precision_score(true_label, predicted_label,average='macro')
  recall = recall_score(true_label, predicted_label,average='macro')
  f1_mesure = f1_score(true_label, predicted_label,average='macro')

  return accuracy,precision,recall,f1_mesure

"""**For Male**"""

batch_size = 32
dataset_loader = dataset_split_and_loader(male_images,male_labels,batch_size)
y_test,y_pred = find_accuracy()
accuracy,precision,recall,f1_mesure = evalution(y_test,y_pred)
# folds_acc,accuracy,precision,recall,f1_mesure = testing_on_final_model(male_images,male_labels,batch_size)

print("accuracy:",accuracy)
print("precision:",precision)
print("recall:",recall)
print("f1_mesure:",f1_mesure)

"""**For Female**"""

batch_size = 32
dataset_loader = dataset_split_and_loader(female_images,female_labels,batch_size)
y_test,y_pred = find_accuracy()
accuracy,precision,recall,f1_mesure = evalution(y_test,y_pred)
# folds_acc,accuracy,precision,recall,f1_mesure = testing_on_final_model(male_images,male_labels,batch_size)

print("accuracy:",accuracy)
print("precision:",precision)
print("recall:",recall)
print("f1_mesure:",f1_mesure)

"""**Bias on Age Group**"""

def Collect_data_age_group(base_path):

  dataset_dir_list = os.listdir("/content/drive/MyDrive/AI_Project/Dataset")
  age_group = ['Young', 'Middle','Senior']


  young_age_images = []
  middle_age_images = []
  senior_age_images = []

  young_age_labels = []
  middle_age_labels = []
  senior_age_labels = []

  brightness_alpha = 1.5
  contrast_alpha = 1.5

  for emotion_label, emotion in enumerate(dataset_dir_list):
    for age_label, age in enumerate(age_group):
          folder_path = os.path.join(base_path, emotion, age)
          image_list = []
          for img_file in os.listdir(folder_path):
              img_path = os.path.join(folder_path, img_file)
              input_img = cv2.imread(img_path)
              # Preprocess each image before adding it to the list
              input_img = cv2.convertScaleAbs(input_img, alpha=brightness_alpha, beta=0)
              input_img = cv2.convertScaleAbs(input_img, alpha=contrast_alpha, beta=0)
              # convert image into gray scale image
              input_img=cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
              # resize image
              input_img_resize = cv2.resize(input_img, (48, 48))

              # Add the preprocessed image to the corresponding lists
              if age == 'Young':
                young_age_images.append(np.array(input_img_resize))
                young_age_labels.append(emotion_label)

              elif age == 'Middle':
                middle_age_images.append(np.array(input_img_resize))
                middle_age_labels.append(emotion_label)

              elif age == 'Senior':
                senior_age_images.append(np.array(input_img_resize))
                senior_age_labels.append(emotion_label)




  return young_age_images,young_age_labels, middle_age_images,middle_age_labels,senior_age_images,senior_age_labels


BASE_PATH_age = "/content/Age"
young_age_images, young_age_labels, middle_age_images, middle_age_labels, senior_age_images, senior_age_labels = Collect_data_age_group(BASE_PATH_age)

# # Merge age_groups data and labels
# img_data_age_group = np.concatenate((young_age_images, middle_age_images,senior_age_images), axis=0)
# img_label_age_group = np.concatenate((young_age_labels, middle_age_labels,senior_age_labels), axis=0)

# #[]

"""**For Young Age-group**"""

batch_size = 32
dataset_loader = dataset_split_and_loader(young_age_images,young_age_labels,batch_size)
y_test,y_pred = find_accuracy()
accuracy,precision,recall,f1_mesure = evalution(y_test,y_pred)
# folds_acc,accuracy,precision,recall,f1_mesure = testing_on_final_model(young_age_images,young_age_labels,batch_size)

print("accuracy:",accuracy)
print("precision:",precision)
print("recall:",recall)
print("f1_mesure:",f1_mesure)

"""**For Middle Age-group**"""

batch_size = 32
dataset_loader = dataset_split_and_loader(middle_age_images,middle_age_labels,batch_size)
y_test,y_pred = find_accuracy()
accuracy,precision,recall,f1_mesure = evalution(y_test,y_pred)
# folds_acc,accuracy,precision,recall,f1_mesure = testing_on_final_model(young_age_images,young_age_labels,batch_size)

print("accuracy:",accuracy)
print("precision:",precision)
print("recall:",recall)
print("f1_mesure:",f1_mesure)

"""**For Senior Age-group**"""

batch_size = 32
dataset_loader = dataset_split_and_loader(senior_age_images,senior_age_labels,batch_size)
y_test,y_pred = find_accuracy()
accuracy,precision,recall,f1_mesure = evalution(y_test,y_pred)
# folds_acc,accuracy,precision,recall,f1_mesure = testing_on_final_model(young_age_images,young_age_labels,batch_size)

print("accuracy:",accuracy)
print("precision:",precision)
print("recall:",recall)
print("f1_mesure:",f1_mesure)



# for 2nd model
batch_size = 32
dataset_loader = dataset_split_and_loader(male_images,male_labels,batch_size)
y_test,y_pred = find_accuracy1()
accuracy,precision,recall,f1_mesure = evalution(y_test,y_pred)
# folds_acc,accuracy,precision,recall,f1_mesure = testing_on_final_model(male_images,male_labels,batch_size)

print("accuracy:",accuracy)
print("precision:",precision)
print("recall:",recall)
print("f1_mesure:",f1_mesure)



