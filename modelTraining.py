import numpy as np
import pandas as pd
from keras.src.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dropout

df = pd.read_csv('data3.csv')

X = df[['humidity']]

y = df['humidifierOn']

X = X.values
y = y.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #splits into 80% training 20% testing and ensures split is identical every time


#scale each centered data point by dividing by the standard deviation, meaning each variable has a variance of one (unit variance)
#this is because ML algorithms are sensitive to scale of input features
#for example humidity ranges from 15 to 60, but rating from 1 to 5, so the ML algorithm won't treat them with equal importance unless they're standardized

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

mlModel = keras.Sequential([ #sequential so layers are added one after another
    keras.layers.Input(shape=(1,)), #each input sample has 1 features, this is the INPUT LAYER

    keras.layers.Dense(16, activation='relu'), #first hidden layer that processes data, each neuron connected to every neuron in prev layer (dense)
    Dropout(0.3), #implemented later on to reduce overfitting

    #in relu activation function, each neuron receives weighted sum of inputs plus bias term, then applies max function that changes negatiue values to zero
    #  z = sum of all (weight * x)
    #  a = relu(z) = max (0,z)
    #  then output 'a' of each neuron becomes input to neuron in the next layer


    keras.layers.Dense(8, activation='relu'),
    #same thing as above except with 8 neurons instead of 16
    Dropout(0.3), #implemented later on to reduce overfitting

    keras.layers.Dense(1, activation='sigmoid')  # 1 output neuron for binary classification (on/off)
    # a = sigma(x) = 1/(1 + e^(-x))
    #this sigmoid function outputs values between 0 and 1 which is needed since this is binary classification
])

#adam optimizer to adjust weights and minimize loss, the loss function binary crossentropy is good for quantifying error in binary classification
mlModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) #accuracy is % of correct predictions on the testeing data

#epochs is passes through training data, not more so it doesn't overfit
#batch size because smaller samples being processed by the model uses less memory and this'll be deployed on ESP32 which is limiting
mlModel.fit(X_train, y_train, epochs=20, batch_size=8, validation_split=0.2) #20% of data is for testing

loss, accuracy = mlModel.evaluate(X_test, y_test) #evaluates performance of model on testing data
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

mlModel.save('humidifier_model.keras') #saves model so I can use it again without retraining

converter = tf.lite.TFLiteConverter.from_keras_model(mlModel) #converting to tflite for micro
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('humidifierML1.tflite', 'wb') as f:
    f.write(tflite_model)

print("Saved TFLite model")