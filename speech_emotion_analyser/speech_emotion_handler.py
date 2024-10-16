import os
import numpy as np
import librosa
import pickle
from keras._tf_keras.keras.models import model_from_json
from keras._tf_keras.keras import optimizers
import tensorflow as tf
import logging


import warnings
warnings.filterwarnings("ignore")

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class EmotionPredictor:
    def __init__(self):
        # Disable oneDNN custom operations if needed
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

        n_mfcc = 30
        sampling_rate = 44100
        audio_duration = 5

        model_json_path = r'M:\pythonProject\2D model_json 1.json (slightly improved)'
        model_weights_path = r"M:\pythonProject\saved_models\2D Emotion_Model (slightly improved).h5"
        label_path = r'C:\Users\eo19181\PycharmProjects\pythonProject\labeler'



        # Load the model
        with open(model_json_path, 'r') as json_file:
            loaded_model_json = json_file.read()
        self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights(model_weights_path)
        #print("Loaded model from disk")

        # Compile the loaded model
        opt = optimizers.Adam(0.001)
        self.loaded_model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['acc'])

        # Load the label encoder
        with open(label_path, 'rb') as infile:
            self.lb = pickle.load(infile)

        # Set parameters for MFCC extraction
        self.n_mfcc = n_mfcc
        self.sampling_rate = sampling_rate
        self.audio_duration = audio_duration

    def extract_mfcc_features(self, file_name):
        input_length = self.sampling_rate * self.audio_duration
        data, _ = librosa.load(file_name, sr=self.sampling_rate, res_type="kaiser_fast", duration=self.audio_duration,
                               offset=0.5)

        if len(data) > input_length:
            max_offset = len(data) - input_length
            offset = np.random.randint(max_offset)
            data = data[offset:(input_length + offset)]
        else:
            if input_length > len(data):
                max_offset = input_length - len(data)
                offset = np.random.randint(max_offset)
            else:
                offset = 0
            data = np.pad(data, (offset, int(input_length) - len(data) - offset), "constant")

        feature_mfcc = librosa.feature.mfcc(y=data, sr=self.sampling_rate, n_mfcc=self.n_mfcc)
        feature_mfcc = np.expand_dims(feature_mfcc, axis=-1)
        feature_mfcc = feature_mfcc.reshape(1, self.n_mfcc, -1, 1)  # Adjust based on your specific model input shape

        return feature_mfcc

    def predict_emotion(self, file_name):
        features = self.extract_mfcc_features(file_name)
        if features is not None:
            prediction = self.loaded_model.predict(features, batch_size=16 ,verbose=0)
            predicted_emotion = np.argmax(prediction, axis=1)
            predicted_emotion = predicted_emotion.astype(int).flatten()
            predicted_emotion = self.lb.inverse_transform(predicted_emotion)  # Corrected transformation
            return predicted_emotion[0]
        else:
            return None


# Example usage
if __name__ == "__main__":
    # Paths to your model files and label file

    # Instantiate the predictor
    predictor = EmotionPredictor()

    # Predict the emotion from an audio file
    file_name = r"C:\Users\eo19181\Documents\All -  Datasets\CREMA - Dataset\Male\Disgust\1001_IEO_DIS_HI.wav"
    predicted_emotion = predictor.predict_emotion(file_name)
    print(f'Predicted Emotion: {predicted_emotion}')
