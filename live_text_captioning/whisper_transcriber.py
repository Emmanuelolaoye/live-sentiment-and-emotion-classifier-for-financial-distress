# import os
# import wave
# import pyaudio
# import sys
# from text_sentiment_analyser.text import Text

from faster_whisper import WhisperModel
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import time


class WhisperTranscriber:
    def __init__(self, model_size="base.en"):
        self.model = WhisperModel(model_size, device="auto", compute_type="float32") # device="cpu",

    def transcribe_chunk(self, file_path):
        # print(f"Transcribing  ---------- {file_path}")
        segments, _ = self.model.transcribe(
            f"live_text_captioning/audio_chunk/chunk_queue/{file_path}",
            beam_size=16, vad_filter=True, vad_parameters=dict(threshold=0.5, max_speech_duration_s=5, min_silence_duration_ms=50), language="en")


        transcription = ''.join(segment.text for segment in segments)
        # print(transcription, ": transription complete")
        return transcription