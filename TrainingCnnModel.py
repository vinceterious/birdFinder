import XenoCantoRestApi
import DataSetPrepare
import sys
import numpy as np
import skimage.io
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import joblib

class TrainingCnnModel:

    def __init__(self):
        self.api = XenoCantoRestApi.XenoCantoRestApi()
        self.r = DataSetPrepare.DataSetPrepare(self.api)

    def predict(self, filename):
        img = self.r.createSpectrograme(filename)
        out = str(filename).replace('mp3','png')
        skimage.io.imsave(out, img)
        x = [self.r.preprocessImg(out)]
        xSample = np.array(x).astype(np.float32)
        model = models.load_model("trainedmodel.keras")
        preds = model.predict(xSample)
        print(str(np.argmax(preds)))
        print(tf.nn.softmax(preds).numpy())


    def train(self):
        self.r.createAllSpectrogramesInDirDataSet()
        y, X = self.r.generateDataSet()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42)
        X_train = np.array(X_train).astype(np.float32)
        X_test = np.array(X_test).astype(np.float32)
        y_train = np.array(y_train).astype(np.float32)
        y_test = np.array(y_test).astype(np.float32)
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 1024, 1)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(len(y)))
        print(model.summary())
        model.compile(optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])

        history = model.fit(X_train, y_train, epochs=11, 
                            validation_data=(X_test, y_test))
        test_loss, test_acc = model.evaluate(X_test,  y_test, verbose=2)
        print(test_acc)
        model.save("trainedmodel_incomplete.keras")

def main():
    r = TrainingCnnModel()
    r.train()
    #r.predict()
    return 0

if __name__ == '__main__':
    sys.exit(main())