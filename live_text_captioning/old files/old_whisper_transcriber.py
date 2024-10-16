import os
import wave
import pyaudio
from faster_whisper import WhisperModel
import sys
from text_sentiment_analyser.text import Text

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_LENGTH = 6
INPUT = True

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

class AudioHandler:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=INPUT, frames_per_buffer=CHUNK)

    def record_chunk(self, file_path):
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        for _ in range(0, int(RATE // CHUNK * RECORD_LENGTH)):
            wf.writeframes(self.stream.read(CHUNK))

        wf.close()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class WhisperTranscriber:
    def __init__(self, model_size="tiny"):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int16")

    def transcribe_chunk(self, file_path):
        segments, info = self.model.transcribe(file_path, beam_size=7)
        transcription = ''.join(segment.text for segment in segments)
        return transcription

def transcriber():
    audio_handler = AudioHandler()
    transcriber = WhisperTranscriber()

    accumulated_transcription = ""

    try:
        while True:
            chunk_file = "../audio_chunk/temp_chunk.wav"
            audio_handler.record_chunk(chunk_file)

            transcription = transcriber.transcribe_chunk(chunk_file)
            text = Text(transcription)
            sentiment = text.get_nltk_sentiment(True)
            text_and_sentiment = transcription + " - " + sentiment

            print(text_and_sentiment)

            os.remove(chunk_file)

            accumulated_transcription += transcription + " "

    except KeyboardInterrupt:
        print("Stopping...")

        with open("../text_log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)

    finally:
        print("LOG" + accumulated_transcription)
        audio_handler.close()

if __name__ == "__main__":
    transcriber()
