# importing necessary libraries
import pickle
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import keras

# preprocesing and general function implementations 

#defining base directory
directory_base_address = 'E:/OneDrive - TUNI.fi/Tampere University (MSc in CS-DS)/Year 2/Period 1/1. Data.ML.100 Introduction to Pattern Recognition and Machine Learning/Exercises/Exercise_3/cifar-10-python\cifar-10-batches-py'

# file reading function
def unpickle(file):
    with open(file, 'rb') as f:
        dict = pickle.load(f, encoding="latin1")
    return dict

# declare empty lists to store training data from different files
X =[]
Y =[]

# reading training data
for i in range(1,6):
    datadict = unpickle(directory_base_address+'/data_batch_'+str(i))
    X.append(datadict["data"])
    Y.append(datadict["labels"])

# reading test data
datadict_test = unpickle(directory_base_address+'/test_batch')

# merging all the training data into one    
X_train = np.concatenate(X, axis=0 )
Y_train = Y[0]+Y[1]+Y[2]+Y[3]+Y[4]

X_test= datadict_test["data"]
Y_test = datadict_test["labels"]

labeldict = unpickle(directory_base_address+'/batches.meta')
label_names = labeldict["label_names"]

X_train = X_train.reshape(50000, 3, 32, 32).transpose(0,2,3,1).astype("uint8")
Y_train = np.array(Y_train)

X_test = X_test.reshape(10000, 3, 32, 32).transpose(0,2,3,1).astype("uint8")
Y_test = np.array(Y_test)


# Normalizing images for better performance
X_train = X_train/255.0
X_test = X_test/255.0

#One hot encoding of the labels
Y_train = tf.one_hot(Y_train, depth=10)
Y_test = tf.one_hot(Y_test, depth=10)

# Simple Artificial Neural Network

model = Sequential()
#input layers
model.add(Flatten(input_shape=(32,32,3)))

# hidden layers
model.add(Dense(128, activation=tf.nn.sigmoid))
model.add(Dense(64, activation=tf.nn.sigmoid))
model.add(Dense(32, activation=tf.nn.sigmoid))
model.add(Dense(16, activation=tf.nn.sigmoid))
#output layers
model.add(Dense(10, activation=tf.nn.sigmoid))

#print(model.summary())

opt = keras.optimizers.SGD(lr=0.5)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

# fit model
training_hist= model.fit(X_train, Y_train,epochs=40)

# Plotting training loss in different epoch
plt.plot(training_hist.history['loss'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.title("Training Loss in different Epoch")
plt.show()

# Plotting training accuracy in different epoch
plt.plot(training_hist.history['accuracy'])
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.title("Training Accurcy in different Epoch")
plt.show()


# Evaluate model with test data
_, acc = model.evaluate(X_test, Y_test, verbose=0)

print("Classification Accuracy for Neural Network is: ", acc)

# Accuracy values comes from previous exercises.
algorithms = ['1-NN','Naive Bayes(1x1)','Bayesian(1x1)','Bayesian(2x2)','Bayesian(4x4)','Bayesian(8x8)','Bayesian(16x16)', 'Neural Network']
accuracies = [9.72, 11.02, 22.78, 28.85, 36.14, 11.04, 10.0, acc*100]

# Plotting the comparison of different algorithms
plt.figure(figsize = (15, 15))
plt.plot(algorithms, accuracies, '-bo')
plt.title("Classification accuracy for different algorithms")
plt.xlabel("algorithms")
plt.ylabel("Accuracy %")
plt.show()  
