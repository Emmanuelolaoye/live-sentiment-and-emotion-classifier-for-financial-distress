# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torchaudio
# from transformers import AutoConfig, Wav2Vec2FeatureExtractor
# from src.models import Wav2Vec2ForSpeechClassification
# import librosa
# import IPython.display as ipd
# import numpy as np
# import pandas as pd
#
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model_name_or_path = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
# config = AutoConfig.from_pretrained(model_name_or_path)
# feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name_or_path)
# sampling_rate = feature_extractor.sampling_rate
# model = Wav2Vec2ForSpeechClassification.from_pretrained(model_name_or_path).to(device)
#
#
# def speech_file_to_array_fn(path, sampling_rate):
#     speech_array, _sampling_rate = torchaudio.load(path)
#     resampler = torchaudio.transforms.Resample(_sampling_rate)
#     speech = resampler(speech_array).squeeze().numpy()
#     return speech
#
# def predict(path, sampling_rate):
#     speech = speech_file_to_array_fn(path, sampling_rate)
#     inputs = feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
#     inputs = {key: inputs[key].to(device) for key in inputs}
#     with torch.no_grad():
#         logits = model(**inputs).logits
#     scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
#     outputs = [{"Emotion": config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
#     return outputs
#
#
#
# # path for a sample
# path = r"C:\Users\eo19181\Documents\All -  Datasets\RAVDESS - Dataset\Female\Happy\03-01-03-01-01-01-08.wav"
# outputs = predict(path, sampling_rate)
# print(outputs, type(outputs))

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import warnings
# Suppress specific warnings
warnings.filterwarnings("ignore", message="Passing `gradient_checkpointing` to a config initialization is deprecated")
warnings.filterwarnings("ignore", message="Some weights of Wav2Vec2ForSpeechClassification were not initialized")



import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from transformers import AutoConfig, Wav2Vec2FeatureExtractor, logging
from src.models import Wav2Vec2ForSpeechClassification


logging.set_verbosity_error()



class HuggingFaceEmotionPredictor:
    def __init__(self, model_name_or_path="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name_or_path = model_name_or_path
        self.config = AutoConfig.from_pretrained(self.model_name_or_path)
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(self.model_name_or_path)
        self.sampling_rate = self.feature_extractor.sampling_rate
        self.model = Wav2Vec2ForSpeechClassification.from_pretrained(self.model_name_or_path).to(self.device)

    def speech_file_to_array_fn(self, path):
        speech_array, _sampling_rate = torchaudio.load(path)
        resampler = torchaudio.transforms.Resample(_sampling_rate)
        speech = resampler(speech_array).squeeze().numpy()
        return speech

    def predict_emotion(self, path):
        speech = self.speech_file_to_array_fn(path)
        inputs = self.feature_extractor(speech, sampling_rate=self.sampling_rate, return_tensors="pt", padding=True)
        inputs = {key: inputs[key].to(self.device) for key in inputs}
        with torch.no_grad():
            logits = self.model(**inputs).logits
        scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
        outputs = [{"Emotion": self.config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in
                   enumerate(scores)]
        return outputs

    def get_highest_emotion(self, path):
        predictions = self.predict_emotion(path)
        highest_emotion = max(predictions, key=lambda x: x["Score"])

        # print(type(highest_emotion["Score"]))
        return highest_emotion["Emotion"]

# Example usage
# if __name__ == "__main__":
#     # Instantiate the predictor
#     predictor = HuggingFaceEmotionPredictor()
#
#     # Predict the emotion from an audio file
#     file_name = r"C:\Users\eo19181\Documents\All -  Datasets\ESD - Dataset\Female\Happy\0016_000701.wav"
#     predicted_emotions = predictor.predict_emotion(file_name)
#     print(predicted_emotions)
#
#     # Get the highest predicted emotion
#     highest_emotion = predictor.get_highest_emotion(file_name)
#     print(f"Highest Emotion: {highest_emotion}")