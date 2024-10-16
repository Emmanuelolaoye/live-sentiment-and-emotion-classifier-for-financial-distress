'''
this object is responsible for all operations nrelating to anysing a sound chunk and to get the sentiment of aid chunk
'''
import os
import wave
from datetime import datetime

import pyaudio

from text_sentiment_analyser.text import Text
from tools.colour_console_text import get_grey_text
from live_text_captioning.whisper_transcriber import WhisperTranscriber
# from json_files import json_handler
from speech_emotion_analyser.huggingface_speech_emotion import HuggingFaceEmotionPredictor


class Chunk:

    def __init__(self, name):
        self.name = name
        # print(self.name, "self")
        self.p = pyaudio.PyAudio()
        self.directory_path = "live_text_captioning/audio_chunk/chunk_queue"
        self.full_path_to_chunk = self.get_chunk_filename(True)
        # print(self.full_path_to_chunk, "path to chunk")

        self.chunk_name = datetime.strptime(self.get_chunk_filename().strip(".wav"), '%Y-%m-%d_%H-%M-%S').strftime(
            '%Y-%m-%d %H:%M:%S')

        # print(self.chunk_name, "self.name")
        self.transcriber = WhisperTranscriber()
        # print("whisper transcriber")
        self.chunk_text = Text(self.transcriber.transcribe_chunk(self.name))
        # print("inside constructor")

    def get_chunk_filename(self, directory=False):
        if directory:
            return f"{self.directory_path}/{self.name}"

        return self.name


    def get_chunk_text_and_datetime(
            self):  # returns the text of the chunk transcribed from the transcribing method
        timestamp_text, timestamp_colour = get_grey_text(self.chunk_name)  # for the datetime
        # print(timestamp_text, timestamp_colour, "time stamp")
        return timestamp_text, timestamp_colour

    def get_chunk_finbert_sentiment(self):
        sentiment = self.chunk_text.get_finbert_sentiment()
        # print(sentiment)
        return sentiment

    def get_chunk_finbert_polarity(self):
        polarity = self.chunk_text.finbert_polarity()
        return polarity


    def get_chunk_roberta_sentiment(self):
        sentiment = self.chunk_text.get_roberta_sentiment()
        return sentiment

    def get_chunk_nltk_sentiment(self):
        sentiment = self.chunk_text.get_nltk_sentiment()
        return sentiment


    def get_chunk_textblob_sentiment(self):
        sentiment = self.chunk_text.get_text_blob_sentiment()
        return sentiment


    def get_emotions(self):
        emotion = HuggingFaceEmotionPredictor()


        file_name = self.full_path_to_chunk
        predicted_emotions = emotion.predict_emotion(file_name)

        return predicted_emotions

    def get_chunk_emotion(self):
        # Paths to your model files and label file

        # Instantiate the predictor
        predictor = HuggingFaceEmotionPredictor()

        # Predict the emotion from an audio file
        file_name = self.full_path_to_chunk
        predicted_emotion = predictor.get_highest_emotion(file_name)
        # print(f'Predicted Emotion: {predicted_emotion}')

        return predicted_emotion

    def process_chunk(self):
        # print(self.chunk_text.get_finbert_sentiment())

        print("processing chunk")

        date_time, colour = self.get_chunk_text_and_datetime()
        finbert = self.get_chunk_finbert_sentiment()
        roberta = self.get_chunk_roberta_sentiment()
        nltk = self.get_chunk_nltk_sentiment()
        textblob = self.get_chunk_textblob_sentiment()
        finbert_polarity = self.get_chunk_finbert_polarity()
        emotions = self.get_emotions()
        emotion = self.get_chunk_emotion()

        print(date_time, colour, self.chunk_text.get_text(), finbert, finbert_polarity, textblob,nltk, roberta, emotion, emotions
)


        return date_time, colour, self.chunk_text.get_text(), finbert, finbert_polarity, textblob,nltk, roberta, emotion, emotions

    # def process_transcription(self, file_path):
    #     text = Text(self.transcriber.transcribe_chunk(file_path))
    #     timestamp_text, timestamp_tag = get_grey_text(datetime.now())
    #     print("time stamp text",timestamp_text, timestamp_tag)
    #
    #     # Insert the timestamp with the grey tag
    #     self.parent.main.after(0, self.parent.ui_handler.update_transcription_date_with_colour, timestamp_text,
    #                            timestamp_tag)  #datetime
    #     self.parent.main.after(0, self.parent.ui_handler.update_transcription_text, f" - {text.get_text()}")  # text
    #     self.parent.main.after(0, self.parent.ui_handler.update_sentiment_text,
    #                            text.get_finetuned_finbert_sentiment())  # - sentiment
    #
    #     # Save to JSON
    #     self.json_handler.add_content(
    #         date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #         text=text.get_text(),
    #         sentiments=text.get_finetuned_finbert_sentiment()
    #     )

    def delete_chunk(self):
        os.remove(self.get_chunk_filename())

    def save_chunk(self, file_path, channels, format, rate, frames):
        wf = wave.open(f"{self.directory_path}/{file_path}", 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(self.p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        # print(f"file saved at {file_path}")

    # def moveChunk(self):
    #     pass

    # def getChunk(self):
    #     pass

# chunk = Chunk("Chunk")
# chu
