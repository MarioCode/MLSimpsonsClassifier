from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense, Dropout
import coremltools
import matplotlib.pyplot as plt
import os

# Variables for learning neural network
img_width, img_height = 64, 64
input_shape = (img_width, img_height, 3)
epochs = 10
batch_size = 32

train_path = "/simpsons_dataset"
test_path = "/simpsons_testset"
labels = [dI for dI in os.listdir(train_path) if os.path.isdir(os.path.join(train_path, dI))]
labels = sorted(labels)

train_images_count = sum([len(files) for r, d, files in os.walk(train_path)])
test_images_count = sum([len(files) for r, d, files in os.walk(test_path)])
classes_count = len(next(os.walk(train_path))[1])

# Initialising the CNN Model
model = Sequential()

# Step 1 - Convolution & Pooling layers
model.add(Conv2D(filters=48,
                 kernel_size=(3, 3),
                 strides=(1, 1),
                 activation='relu',
                 input_shape=input_shape))

model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.3))

# Step 2 - Convolution & Pooling layers
model.add(Conv2D(filters=32,
                 kernel_size=(5, 5),
                 activation='relu'))

model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.2))

# Step 4 - Flattening
model.add(Flatten())

# Layer 5 - Full connection
model.add(Dense(128, activation='relu'))
model.add(Dense(classes_count, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Data augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255.0,
    shear_range=0.2,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    fill_mode='nearest',
    horizontal_flip=True)

# Flows the data directly from the directory structure, resizing where needed
train_set = train_datagen.flow_from_directory(
    train_path,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

# Only rescaling for validation
test_dataGen = ImageDataGenerator(rescale=1. / 255.0)

test_set = test_dataGen.flow_from_directory(
    test_path,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

# Generate model
result = model.fit_generator(
    train_set,
    steps_per_epoch=train_images_count // batch_size,
    epochs=epochs,
    validation_data=test_set,
    validation_steps=test_images_count // batch_size)

# Visualization
plt.plot(result.history['acc'])
plt.plot(result.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Validation
model.evaluate_generator(test_set, steps=100)

# Save CNN Model
model.save('simpsons_model.h5')

# Convert h5 and prepare to save the CoreML model
coreml_model = coremltools.converters.keras.convert(model,
                                                    input_names='image',
                                                    image_input_names='image',
                                                    class_labels=labels)

coreml_model.author = 'Makarov Anton'
coreml_model.license = 'MIT'
coreml_model.short_description = 'The Simpsons Classifier'
coreml_model.input_description['image'] = 'Image of one of the Simpsons characters'
coreml_model.output_description['output1'] = 'Character recognition probability'
coreml_model.save('simpsons_model.mlmodel')

