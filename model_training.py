import os
import pandas as pd 
import numpy as np 
import cv2 
import tensorflow as tf
import random

from keras.layers import Conv2D, MaxPooling2D , BatchNormalization ,Dropout ,Flatten , Dense , Input , Rescaling , Resizing
from keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from tensorflow.keras.applications import MobileNetV2

dataDir = 'garbage_classification/'

selectedClasses = ['metal', 'glass', 'paper', 'trash', 'cardboard', 'plastic' ,'white-glass']

imgPaths = []
labels = []

for className in os.listdir(dataDir):
    if className in selectedClasses :
        classPath = os.path.join(dataDir,className)
        for img in os.listdir(classPath):
            imgPath = os.path.join(classPath,img)
            imgPaths.append(imgPath)
            if className == 'white-glass':
                className = 'glass'
            labels.append(className)

df = pd.DataFrame({
    'imgPath':imgPaths,
    'label':labels
})

df = df.sample(frac=1).reset_index(drop=True) #shuffles the dataframe

# get the ratio such as 15% of each class for testing 
def DataFrameSpliting(df , ratio , classesList):
    
    trainDf = pd.DataFrame(columns = ['imgPath','label'])
    testDf = pd.DataFrame(columns = ['imgPath','label'])
    for clas in classesList :
        tempDf = df[df['label'] == clas]
        lastIndex = int(len(tempDf) * ratio)
        trainClassDf = tempDf[:lastIndex]
        testClassDf = tempDf[lastIndex:]
        trainDf = pd.concat([trainDf , trainClassDf] , axis=0)
        testDf = pd.concat([testDf , testClassDf] , axis=0)
        
    return trainDf.sample(frac=1).reset_index(drop=True) , testDf.sample(frac=1).reset_index(drop=True)  # shuffling , reset index

classList = list(df['label'].unique())
trainDf , testDf = DataFrameSpliting(df , 0.85 , classList)


datagenTrain = ImageDataGenerator(
            rescale=1./255,
            zoom_range=(1.0, 1.2),   # zoom in 
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=45,
)

IMG_SIZE = (224,224)

trainGenerator = datagenTrain.flow_from_dataframe(
    trainDf ,
    x_col='imgPath',
    y_col='label',
    target_size=IMG_SIZE,
    batch_size=64 ,                    # Generate 64 image from the datagenTrain (flipped , rotated , zoomed , ....)  at once 
    class_mode='categorical'
)


datagenTest = ImageDataGenerator( rescale=1./255 )

testGenerator = datagenTest.flow_from_dataframe(
    testDf ,
    x_col='imgPath',
    y_col='label',
    target_size=IMG_SIZE,
    batch_size=8 ,
    class_mode='categorical',
    shuffle=False
)


print(f"Training set size: {trainGenerator.samples}")
print(f"Testing set size: {testGenerator.samples}")

with tf.device('/GPU:0'):          # to use GPU
    Model = Sequential([
#         Resizing(IMG_SIZE),
#         Rescaling(1./255),     These two steps ,we did perform them above with test and image generator 
        MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3)),
        Flatten(),                                     # because we ignore the flatten and dense layers when include_top = False 
        Dense(64,activation='relu'),
        BatchNormalization(),
        Dropout(0.08),
        Dense(6 ,activation='softmax')
    ])

preTrainedModel = Model.layers[0]
for layer in preTrainedModel.layers[:-4]: # freeze all layers except the first and last 3 layers, we will make them trainable (weghts changes with training)
    layer.trainable = False
Model.compile(optimizer='adam',loss='categorical_crossentropy' ,metrics=['accuracy'])

history = Model.fit(trainGenerator,
                    validation_data = testGenerator, 
                    epochs=50,
#                   batch_size=64,   # we define it above inside trainGenerator
                    verbose=1,
                    callbacks=[tf.keras.callbacks.EarlyStopping(
                                       patience=4,
                                       monitor='val_accuracy',
                                       restore_best_weights=True)])

test_loss, test_accuracy = Model.evaluate(testGenerator)
print(test_accuracy)