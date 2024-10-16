# audio_handler_1.py

from datetime import datetime
import pyaudio
import wave
import threading
import os
from live_text_captioning.whisper_transcriber import WhisperTranscriber
from text_sentiment_analyser.text import Text
from tools.colour_console_text import get_grey_text  # Import the grey_text function
from json_files.json_handler import Json  # Add this import
from live_text_captioning.audio_chunk import audio_chunk as chunk


class AudioHandler:
    def __init__(self, parent):
        self.parent = parent
        self.p = pyaudio.PyAudio()
        self.transcriber = WhisperTranscriber()
        self.json_handler = Json()  # Initialize the Json handler

    def open_stream(self, format, channels, rate, chunk):
        return self.p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    def start_record(self):
        self.parent.is_recording = True
        self.parent.frames = []
        self.parent.stream = self.open_stream(self.parent.audio_settings["format"],
                                              self.parent.audio_settings["channels"],
                                              self.parent.audio_settings["rate"],
                                              self.parent.audio_settings["chunk"])
        threading.Thread(target=self.record).start()

    def record(self):
        total_recording_frames = []
        total_recording_time = 0
        accumulated_frames = []
        accumulated_duration = 0
        chunk_duration = self.parent.audio_settings["chunk"] / self.parent.audio_settings["rate"]

        while self.parent.is_recording:
            data = self.parent.stream.read(self.parent.audio_settings["chunk"], exception_on_overflow=False)
            self.parent.frames.append(data)
            accumulated_frames.append(data)
            accumulated_duration += chunk_duration

            if accumulated_duration >= 5:
                chunk_file = "temp_file.wav"
                chunk_file_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_chunk = chunk.Chunk(chunk_file_name)
                new_chunk.save_chunk(chunk_file, self.parent.audio_settings["channels"],
                                     self.parent.audio_settings["format"],
                                     self.parent.audio_settings["rate"],
                                     accumulated_frames)

                self.save_chunk(chunk_file, self.parent.audio_settings["channels"],
                                self.parent.audio_settings["format"],
                                self.parent.audio_settings["rate"],
                                accumulated_frames)
                self.process_transcription(chunk_file)

                accumulated_frames = []
                accumulated_duration = 0

            self.parent.main.update()

    def stop(self):
        self.parent.is_recording = False
        self.parent.stream.close()
        self.close()

    def pause(self):
        self.parent.is_recording = False

    def resume(self):
        self.parent.is_recording = True
        threading.Thread(target=self.record).start()

    def process_transcription(self, file_path):
        text = Text(self.transcriber.transcribe_chunk(file_path))
        timestamp_text, timestamp_tag = get_grey_text(datetime.now())

        # Insert the timestamp with the grey tag
        self.parent.main.after(0, self.parent.ui_handler.update_transcription_text_with_tag, timestamp_text,
                               timestamp_tag)
        self.parent.main.after(0, self.parent.ui_handler.update_transcription_text, f" - {text.get_text()}")
        self.parent.main.after(0, self.parent.ui_handler.update_sentiment_text, text.get_finetuned_finbert_sentiment())

        # Save to JSON
        self.json_handler.add_content(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            text=text.get_text(),
            sentiments=text.get_finetuned_finbert_sentiment()
        )

        os.remove(file_path)

    def save_chunk(self, file_path, channels, format, rate, frames):
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(self.p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def close(self):
        self.p.terminate()
