import os
import IPython.display
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense,Flatten,Dropout,BatchNormalization,Conv2D,MaxPool2D, MaxPooling2D
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tqdm import tqdm
from glob import glob
from skimage.transform import resize
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from sklearn.metrics import confusion_matrix,classification_report, accuracy_score
import itertools


train_dir=r"C:\Users\KIIT\Desktop\Hand3\Dataset\train"
test_dir=r"C:\Users\KIIT\Desktop\Hand3\Dataset\val"
folders=[folder for folder in sorted(os.listdir(train_dir))]
print(folders)
print("Total no. of folders are: ",len(folders))
map_characters={0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'Blank'}
print (map_characters)

def load_data(train_dir):
    images=list()
    labels=list()
    for file in folders:
        folder_path=os.path.join(train_dir,file)
        for img in tqdm(os.listdir(folder_path)):
            if file=='A':
                label=0
            elif file=='B':
                label=1
            elif file=='C':
                label=2
            elif file=='D':
                label=3
            elif file=='E':
                label=4
            elif file=='F':
                label=5
            elif file=='G':
                label=6
            elif file=='H':
                label=7
            elif file=='I':
                label=8
            elif file=='J':
                label=9
            elif file=='K':
                label=10
            elif file=='L':
                label=11
            elif file=='M':
                label=12
            elif file=='N':
                label=13
            elif file=='O':
                label=14
            elif file=='P':
                label=15
            elif file=='Q':
                label=16
            elif file=='R':
                label=17
            elif file=='S':
                label=18
            elif file=='T':
                label=19
            elif file=='U':
                label=20
            elif file=='V':
                label=21
            elif file=='W':
                label=22
            elif file=='X':
                label=23
            elif file=='Y':
                label=24
            elif file=='Z':
                label=25
            elif file=='blank':
                label=26
            if img is not None:
                image_path=folder_path+'/'+img
                image=cv2.imread(image_path)
                image=cv2.resize(image,(48,48))
                gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                images.append(gray)
                labels.append(label)
    images=np.asarray(images)
    labels=np.asarray(labels)

    return (images,labels)
X,y=load_data(train_dir)
X_test,y_test=load_data(test_dir)
print('There are total {} Images and {} unique Labels in the dataset.'.format(len(X),len(np.unique(y))))
X_train,X_valid,y_train,y_valid=train_test_split(X,y,test_size=0.2)
print(X_train.shape)
print(X_valid.shape)
y_train_vectors=to_categorical(y_train)
y_valid_vectors=to_categorical(y_valid)
y_test_vectors=to_categorical(y_test)
print(y_train_vectors.shape)

#CNN Model
model = Sequential()
# convolutional layers
model.add(Conv2D(128, kernel_size=(3,3), activation='relu', input_shape=(48,48,1)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))

model.add(Conv2D(256, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))

model.add(Conv2D(512, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))

model.add(Conv2D(512, kernel_size=(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.4))

model.add(Flatten())
# fully connected layers
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.3))
# output layer
model.add(Dense(27, activation='softmax'))

optimiser = Adam()
model.compile(optimizer=optimiser, loss='categorical_crossentropy', metrics=['categorical_accuracy'])
print(model.summary())
history=model.fit(X_train, y_train_vectors,
          batch_size=128,
          epochs=12,
          verbose=1,
          validation_data=(X_valid,y_valid_vectors))

plt.plot(history.history['categorical_accuracy'])
plt.plot(history.history['val_categorical_accuracy'])
plt.title('model accuracy of vgg16')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

predictions_probabilities=model.predict(X_test)
predictions = np.argmax(predictions_probabilities, axis=1)
print(classification_report(y_test, predictions))
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)
print("Accuracy (%):", accuracy * 100)
model_json = model.to_json()
with open(r"Model/sign_language_detection_model.json",'w') as json_file:
    json_file.write(model_json)
model.save(r"Model/sign_language_detection_model.h5")