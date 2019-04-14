### The Simpsons Classifier using Python, Swift and a Demo Mobile App.
<img width="240" src="https://user-images.githubusercontent.com/12527666/55711383-36a2a880-59f5-11e9-9cbe-5e4955f580a0.PNG">

#### 1. Installing the required tools and environment to start learning the model:
- python=3.6
- pip=19.0.3
    - tensorflow==1.13.1
    - keras==2.2.4
    - coremltools==2.1.0

#### 2. Learning process
- Layers: 11
- Epochs: 50
- Batch size: 610
- Accuracy: 0.8489 (but it seems to be much lower)

```python
model = Sequential()

model.add(Conv2D(filters=48, kernel_size=(3, 3), strides=(1, 1), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.3))

model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(classes_count, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
...
model.save('simpsons_model.h5')
```
![ModelAcc](https://user-images.githubusercontent.com/12527666/55710942-5e454100-59f4-11e9-9d89-4f69f4bb6731.png)
<img width="420" src="https://user-images.githubusercontent.com/12527666/55710983-79b04c00-59f4-11e9-8e0f-2ffadab6faac.png">

#### 3. Use CoremlTools. 
Convert the Keras model (.h5) to the CoreML model.

```python
coreml_model = coremltools.converters.keras.convert(model,
                                                    input_names='image',
                                                    image_input_names='image',
                                                    class_labels=labels)

coreml_model.author = 'Makarov Anton'
coreml_model.short_description = 'The Simpsons Classifier'
coreml_model.input_description['image'] = 'Image of one of the Simpsons characters'
coreml_model.output_description['output1'] = 'Character recognition probability'
coreml_model.save('simpsons_model.mlmodel')
```

#### 4. Sample iOS App
- Swift
- import CoreML, Vision, AVKit (Live Camera)

```swift
private func getCoreMLModel() -> VNCoreMLModel? {
    guard let model = try? VNCoreMLModel(for: simpsons_model().model) else {
        return nil
    }
    return model
}
```

