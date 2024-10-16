# Importing required libraries

# Keras
import keras
from keras import regularizers
from keras_preprocessing import sequence
from keras_preprocessing.sequence import pad_sequences
from keras import Sequential, Model
from keras._tf_keras.keras.models import model_from_json
from keras._tf_keras.keras.layers import Dense, Embedding, LSTM, Input, Flatten, Dropout, Activation, \
    BatchNormalization, Conv1D, MaxPooling1D, AveragePooling1D
from keras._tf_keras.keras.utils import to_categorical
from keras._tf_keras.keras.callbacks import ModelCheckpoint
from keras._tf_keras.keras import utils
from keras._tf_keras.keras import optimizers
import np_utils

# sklearn
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Other
import librosa
print(librosa.__version__)
from librosa import feature
import json
from scipy.io import wavfile
from python_speech_features import mfcc
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
import pandas as pd
import seaborn as sns
import glob
import os
import pickle
import IPython.display as ipd  # To play sound in the notebook

import sys
import warnings

# Filter specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="librosa.core.audio")

# ignore general warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# let's pick up the meta-data that we got from our first part of the Kernel
ref = pd.read_csv(r"C:\Users\eo19181\Documents\All -  Datasets\sorted_data_paths.csv")
print(ref.head())

# Note this takes a couple of minutes (~10 mins) as we're iterating over 4 datasets
df = pd.DataFrame(columns=['feature'])

# loop feature extraction over the entire dataset
# Iterate over audio file paths and extract MFCCs
counter = 0
for index, path in enumerate(ref.path):
    X, sample_rate = librosa.load(path
                                  , res_type='kaiser_fast'
                                  , duration=2.5
                                  , sr=44100
                                  , offset=0.5
                                  )
    sample_rate = np.array(sample_rate)

    # mean as the feature. Could do min and max etc as well.
    mfccs = np.mean(feature.mfcc(y=X,
                                         sr=sample_rate,
                                         n_mfcc=13),
                    axis=0)
    df.loc[counter] = [mfccs]
    counter = counter + 1

# Check a few records to make sure its processed successfully
print(len(df))
print(df.head())
print(df.shape)
print(len(df[0]))
#
# # Now extract the mean bands to its own feature columns
# df = pd.concat([ref, pd.DataFrame(df['feature'].values.tolist())], axis=1)
# print(df[:5])
#
# # replace NA with 0
# df = df.fillna(0)
# print(df.shape)
# print(df[:5])
#
# # Split between train and test
# X_train, X_test, y_train, y_test = train_test_split(df.drop(['path', 'labels', 'source'], axis=1), df.labels, test_size=0.25, shuffle=True, random_state=42)
#
# # Let's see how the data present itself before normalisation
# print(X_train[150:160])
#
# # Lts do data normalization
# mean = np.mean(X_train, axis=0)
# std = np.std(X_train, axis=0)
#
# X_train = (X_train - mean) / std
# X_test = (X_test - mean) / std
#
# # Check the dataset now
# print(X_train[150:160])
#
# max_data = np.max(X_train)
# min_data = np.min(X_train)
# X_train = (X_train - min_data) / (max_data - min_data + 1e-6)
# X_train = X_train - 0.5
#
# max_data = np.max(X_test)
# min_data = np.min(X_test)
# X_test = (X_test - min_data) / (max_data - min_data + 1e-6)
# X_test = X_test - 0.5
#
# print(X_train[150:160])
#
# # Lets few preparation steps to get it into the correct format for Keras
# X_train = np.array(X_train)
# y_train = np.array(y_train)
# X_test = np.array(X_test)
# y_test = np.array(y_test)
#
# # one hot encode the target
# lb = LabelEncoder()
# y_train = to_categorical(lb.fit_transform(y_train))
# y_test = to_categorical(lb.fit_transform(y_test))
#
# print(X_train.shape)
# print(lb.classes_)
# # print(y_train[0:10])
# # print(y_test[0:10])
#
# # Pickel the lb object for future use
# filename = 'labels'
# outfile = open(filename, 'wb')
# pickle.dump(lb, outfile)
# outfile.close()
# print("finished this")
#
# X_train = np.expand_dims(X_train, axis=2)
# X_test = np.expand_dims(X_test, axis=2)
# print(X_train.shape)
#
# # New model
# model = Sequential()
# model.add(Conv1D(256, 8, padding='same', input_shape=(X_train.shape[1], 1)))  # X_train.shape[1] = No. of Columns
# model.add(Activation('relu'))
# model.add(Conv1D(256, 8, padding='same'))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
# model.add(Dropout(0.25))
# model.add(MaxPooling1D(pool_size=8))
# model.add(Conv1D(128, 8, padding='same'))
# model.add(Activation('relu'))
# model.add(Conv1D(128, 8, padding='same'))
# model.add(Activation('relu'))
# model.add(Conv1D(128, 8, padding='same'))
# model.add(Activation('relu'))
# model.add(Conv1D(128, 8, padding='same'))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
# model.add(Dropout(0.25))
# model.add(MaxPooling1D(pool_size=8))
# model.add(Conv1D(64, 8, padding='same'))
# model.add(Activation('relu'))
# model.add(Conv1D(64, 8, padding='same'))
# model.add(Activation('relu'))
# model.add(Flatten())
# model.add(Dense(14))  # Target class number
# model.add(Activation('softmax'))
# # opt = keras.optimizers.SGD(lr=0.0001, momentum=0.0, decay=0.0, nesterov=False)
# # opt = keras.optimizers.Adam(lr=0.0001)
# opt = optimizers.RMSprop(lr=0.00001, decay=1e-6)
# print(model.summary())
#
# model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
# model_history = model.fit(X_train, y_train, batch_size=16, epochs=100, validation_data=(X_test, y_test))
#
# plt.plot(model_history.history['loss'])
# plt.plot(model_history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()
#
# # Save model and weights
# model_name = 'Emotion_Model.h5'
# save_dir = os.path.join(os.getcwd(), 'saved_models')
#
# if not os.path.isdir(save_dir):
#     os.makedirs(save_dir)
# model_path = os.path.join(save_dir, model_name)
# model.save(model_path)
# print('Save model and weights at %s ' % model_path)
#
# # Save the model to disk
# model_json = model.to_json()
# with open("model_json.json", "w") as json_file:
#     json_file.write(model_json)
#
# print('Saved model to disk')
