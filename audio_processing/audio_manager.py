# from tkinter import Tk
# import pyaudio
# from audio_processing.audio_handler import AudioHandler
# from gui.gui_handler import UIHandler
#
# class RecAUD:
#     def __init__(self, chunk=2048, frmat=pyaudio.paInt16, channels=1, rate=44100):
#         self.main = Tk()
#         self.main.geometry('1500x300')
#         self.main.title('Audio Recorder and Transcriber')
#
#         self.audio_settings = {
#             "chunk": chunk,
#             "format": frmat,
#             "channels": channels,
#             "rate": rate
#         }
#         self.frames = []
#         self.stream = None
#         self.is_recording = False
#
#         self.ui_handler = UIHandler(self)
#         self.audio_handler = AudioHandler(self)
#
#         # Initialize the text widgets
#         self.transcription_text = None
#         self.sentiment_text = None
#
#         self.ui_handler.setup_ui()
#
#         self.main.mainloop()
#
# if __name__ == "__main__":
#     guiAUD = RecAUD()


from tkinter import Tk
import pyaudio
from audio_processing.audio_handler import AudioHandler
from gui.gui_handler import UIHandler # changed to 2


# TODO: uses audio handler, audio manager, text, fine tuned finbert, gui handler etc
from text_sentiment_analyser.finbert import FinBertSentimentAnalyser

class AudioManager:
    def __init__(self, chunk=2048, frmat=pyaudio.paInt16, channels=1, rate=44100):
        self.main = Tk()
        self.main.geometry('1500x900')  # Adjust window size for the additional frame
        self.main.title('Audio Recorder and Transcriber')
        # self.main.resizable(width=False, height=False)

        self.audio_settings = {
            "chunk": chunk,
            "format": frmat,
            "channels": channels,
            "rate": rate
        }
        self.frames = []
        self.stream = None
        self.is_recording = False

        # self.finbert_analyser = FinBertSentimentAnalyser()  # Initialize FinBERT

        self.audio_handler = AudioHandler(self)
        self.ui_handler = UIHandler(self)

        # # Initialize the text widgets
        # self.transcription_text = None
        # self.sentiment_text = None
        # self.emotion_text = None

        self.ui_handler.setup_ui()

        self.main.mainloop()
