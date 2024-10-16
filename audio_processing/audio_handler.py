import os
import queue
import shutil
import threading
import time
import wave
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pyaudio

from json_files.json_handler import Json  # Add this import
from live_text_captioning.audio_chunk import audio_chunk as chunk
from live_text_captioning.whisper_transcriber import WhisperTranscriber

"""

this class uses multithreading

ThreadPoolExecutor: Utilized ThreadPoolExecutor from concurrent.futures to handle chunk processing in a thread pool.
Multithreading: The queue_thread now submits chunk processing tasks to the thread pool, which can execute them concurrently.
Timeout Handling: Used a timeout for queue.get to avoid blocking indefinitely.

"""


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
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.start_queue_thread()

    def open_stream(self, format, channels, rate, chunk):
        return self.p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    def start_queue_thread(self):
        threading.Thread(target=self.queue_thread).start()

    def queue_thread(self):
        while True:
            try:
                chunk_name = self.chunk_queue.get(timeout=0.5)  # Waits for 1 second for an item
                # print(f"Processing chunk: {chunk_name}")
                self.executor.submit(self.process_chunk, chunk_name)
                self.chunk_queue.task_done()  # Signal that the task is done
            except queue.Empty:
                # print("....")
                continue

    def process_chunk(self, chunk_name):
        # print(f"audio handler process chunk", chunk_name)
        chunk_details = chunk.Chunk(chunk_name).process_chunk()
        print(chunk_details, "chunk")
        date_time, colour, text, sentiment, polarity, textblob, nltk, roberta, emotion, emotions = chunk_details

        print(text, "text")

        # print(str(date_time))

        # date_time, colour, self.chunk_text.get_text(), finbert, finbert_polarity, textblob, nltk, roberta, emotion, emotions

        # date_time, colour, self.chunk_text.get_text(), sentiment,polarity, emotion, emotions

        # Insert the timestamp with the grey tag
        self.parent.main.after(0, self.parent.ui_handler.update_transcription_date_with_colour, date_time,
                               colour)  # date time and colour
        self.parent.main.after(0, self.parent.ui_handler.update_transcription_text, f" - {text}")  # text
        self.parent.main.after(0, self.parent.ui_handler.update_sentiment_text, sentiment)
        self.parent.main.after(0, self.parent.ui_handler.update_emotion_text, emotion)
        self.parent.main.after(0, self.parent.ui_handler.add_polarity_data, polarity, date_time)  # TODO: fix here
        self.parent.main.after(0, self.parent.ui_handler.add_emotion_data, emotions)

        # time.sleep(1)


        self.json_handler.add_content(

            date=date_time,
            text=text,
            sentiments={
                "finBERT" : sentiment,#
                "roBERTa" : roberta,
                "textBlob" : textblob,
                "NLTK" : nltk},
            emotions=emotions

        )


        # self.parent.main.after(0, self.parent.ui_handler.plot_stock)
        # # Extract sentiment polarity and update UI
        # sentiment_text = self.parent.finbert_analyser.get_sentiment(text)
        # self.parent.main.after(0, self.parent.ui_handler.update_sentiment_text, sentiment_text)

        self.parent.main.update()
        self.delete_chunk(chunk_name)

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
                self.save_chunk(r"live_text_captioning/audio_chunk/chunk_queue/" + chunk_file_name,
                                self.parent.audio_settings["channels"],
                                self.parent.audio_settings["format"],
                                self.parent.audio_settings["rate"],
                                accumulated_frames)
                self.chunk_queue.put(chunk_file_name)
                accumulated_frames = []
                accumulated_duration = 0

    def stop(self):
        self.parent.is_recording = False
        self.parent.stream.close()
        self.save_total_recording()
        self.clear_chunk_queue()
        self.close()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
        threading.Thread(target=self.record).start()

    def clear_chunk_queue(self):
        folder = r'live_text_captioning/audio_chunk/chunk_queue'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

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
