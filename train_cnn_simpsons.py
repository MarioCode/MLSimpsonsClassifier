from model import *

from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
import matplotlib.pyplot as plt
import numpy as np
import coremltools
import os

# Variables for learning neural network
img_width, img_height = 96, 96
input_shape = (img_width, img_height, 3)
epochs = 50
batch_size = 32

dataset_path = '/simpsons_dataset'

# Load dataset
image_list, labels, num_classes = load_dataset(dataset_path, img_width, img_height, 300)

# Split into train, dev sets
X_train, X_dev, y_train, y_dev = train_test_split(np.array(image_list),
                                                  labels,
                                                  test_size=0.2,
                                                  stratify=labels)
y_train = np_utils.to_categorical(y_train)
y_dev = np_utils.to_categorical(y_dev)

# Initialising the CNN Model
model = build_model(input_shape, num_classes)

# Data augmentation for training
data_generator = ImageDataGenerator(rescale=1./255,
                                    featurewise_center=False,
                                    samplewise_center=False,
                                    featurewise_std_normalization=False,
                                    samplewise_std_normalization=False,
                                    zca_whitening=False,
                                    rotation_range=15,
                                    width_shift_range=0.2,
                                    height_shift_range=0.2,
                                    horizontal_flip=True,
                                    vertical_flip=False)

# Model fit generator
result = model.fit_generator(data_generator.flow(X_train, y_train, batch_size=batch_size),
                             steps_per_epoch=len(X_train) / batch_size,
                             validation_data=data_generator.flow(X_dev, y_dev, batch_size=batch_size),
                             validation_steps=len(X_dev) / batch_size,
                             epochs=epochs)

# Save CNN Model
model.save('simpsons.h5')

# Convert h5 and prepare to save the CoreML model
labels = [dI for dI in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, dI))]
labels = sorted(labels)

coreml_model = coremltools.converters.keras.convert(model,
                                                    input_names='image',
                                                    image_input_names='image',
                                                    class_labels=labels)

coreml_model.author = 'Makarov Anton'
coreml_model.license = 'MIT'
coreml_model.short_description = 'The Simpsons Classifier'
coreml_model.input_description['image'] = 'Image of one of the Simpsons characters'
coreml_model.output_description['output1'] = 'Character recognition probability'
coreml_model.save('simpsons.mlmodel')

# Visualization
f, ax = plt.subplots(ncols=2, figsize=(15, 5))
ax[0].plot(result.history['acc'], label='Train')
ax[0].plot(result.history['val_acc'], label='Dev')
ax[0].legend()
ax[0].set_xlabel('Epochs')
ax[0].set_ylabel('Accuracy')

ax[1].plot(result.history['loss'], label='Train')
ax[1].plot(result.history['val_loss'], label='Dev')
ax[1].legend()
ax[1].set_xlabel('Epochs')
ax[1].set_ylabel('Loss')

