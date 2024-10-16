import queue
from datetime import datetime
import pyaudio
import wave
import threading
import os
from live_text_captioning.whisper_transcriber import WhisperTranscriber
from json_files.json_handler import Json  # Add this import
from live_text_captioning.audio_chunk import audio_chunk as chunk
# from collections import deque

from queue import Empty

"""the old method that tries to used multithreading but was not optimised"""


class AudioHandler:
    def __init__(self, parent):
        self.parent = parent
        self.p = pyaudio.PyAudio()
        self.transcriber = WhisperTranscriber()
        self.json_handler = Json()  # Initialize the Json handler
        self.total_recording_frames = []
        self.total_recording_time = 0
        self.is_paused = False
        self.chunk_queue = queue.Queue()
        self.start_queue_thread()

    def open_stream(self, format, channels, rate, chunk):
        return self.p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    def start_queue_thread(self):
        threading.Thread(target=self.queue_thread).start()

    def queue_thread(self):
        while True:
            try:
                chunk_name = self.chunk_queue.get()  # Waits for 1 second for an item

                print(f"Processing chunk: {chunk_name}")
                self.process_chunk(chunk_name)

                self.chunk_queue.task_done()  # Signal that the task is done
            except Empty:
                print("nothing in queue")
                continue

    # def process_chunk(self, chunk_name):
    #
    #     chunk_details = chunk.Chunk(chunk_name).process_chunk()
    #     print(chunk_details)
    #     date_time, text, sentiment, emotion = chunk_details
    #
    #     # Insert the timestamp with the grey tag
    #     self.parent.main.after(0, self.parent.ui_handler.update_transcription_date_with_colour, date_time[0],
    #                            date_time[1])  #date time and colour
    #     self.parent.main.after(0, self.parent.ui_handler.update_transcription_text, f" - {text}")  # text
    #     self.parent.main.after(0, self.parent.ui_handler.update_sentiment_text,
    #                            sentiment)
    #
    #     self.parent.main.update()
    #
    #     self.delete_chunk(chunk_name)
    #
    #     pass

    def start_record(self):
        self.parent.is_recording = True
        self.parent.frames = []
        self.parent.stream = self.open_stream(self.parent.audio_settings["format"],
                                              self.parent.audio_settings["channels"],
                                              self.parent.audio_settings["rate"],
                                              self.parent.audio_settings["chunk"])
        threading.Thread(target=self.record).start()

    def record(self):
        accumulated_frames = []
        accumulated_duration = 0
        chunk_duration = self.parent.audio_settings["chunk"] / self.parent.audio_settings["rate"]

        while self.parent.is_recording:
            if self.is_paused:
                continue

            data = self.parent.stream.read(self.parent.audio_settings["chunk"], exception_on_overflow=False)
            self.parent.frames.append(data)
            self.total_recording_frames.append(data)
            accumulated_frames.append(data)
            accumulated_duration += chunk_duration

            if accumulated_duration >= 5:
                chunk_file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"  # Replaced colons and spaces

                self.save_chunk("live_text_captioning/audio_chunk/chunk_queue/" + chunk_file_name,
                                self.parent.audio_settings["channels"],
                                self.parent.audio_settings["format"],
                                self.parent.audio_settings["rate"],
                                accumulated_frames)
                self.chunk_queue.put(chunk_file_name)

                accumulated_frames = []
                accumulated_duration = 0

                # self.parent.main.update()

    def stop(self):
        self.parent.is_recording = False
        self.parent.stream.close()
        self.save_total_recording()
        self.close()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        threading.Thread(target=self.record).start()

    def save_chunk(self, file_path, channels, format, rate, frames):
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(self.p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def delete_chunk(self, file_path):
        os.remove("live_text_captioning/audio_chunk/chunk_queue/" + file_path)

    def save_total_recording(self):
        total_file_path = "total_recording.wav"
        self.save_chunk(total_file_path, self.parent.audio_settings["channels"],
                        self.parent.audio_settings["format"],
                        self.parent.audio_settings["rate"],
                        self.total_recording_frames)

    def close(self):
        self.p.terminate()
