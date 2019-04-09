from keras import backend as K
from keras import optimizers
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.preprocessing import LabelEncoder

import os
import numpy as np
import cv2


def load_dataset(path, height, width, least_num):
    
    image_list, label_list = [], []
    
    for root, dirs, files in os.walk(path):
        temp_images, temp_labels = [], []
        
        for file in files:
            image_path = os.path.join(root, file)
            image = cv2.imread(image_path)
            try:
                image = cv2.resize(image, (height, width))
                temp_labels.append(root.split('/')[-1])
                temp_images.append(image)
            except Exception as e:
                print(str(e))
    
        if len(temp_images) >= least_num:
            image_list.extend(temp_images)
            label_list.extend(temp_labels)

num_classes = len(np.unique(label_list))

le = LabelEncoder()
label_list = le.fit_transform(label_list)

return image_list, label_list, num_classes


def build_model(input_shape, classes_count):
    
    # Initialising the CNN Model
    model = Sequential()
    
    # Step 1 - Convolution & Pooling layers
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    
    model.add(Flatten())
    
    model.add(Dense(1024, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(256, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))
    
    model.add(Dense(classes_count, activation='softmax'))
    
    model.summary()
    
    sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)
    
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])
                  
    return model
