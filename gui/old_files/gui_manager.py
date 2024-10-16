# import sys
# import tkinter as tk
# import pyaudio
# import wave
# from tkinter.filedialog import asksaveasfilename
# from faster_whisper import WhisperModel
# import threading
# import os
#
# from text_sentiment_analyser.text import Text
#
#
# class RecAUD:
#     def __init__(self, chunk=2048, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):
#         self.main = tk.Tk()
#         self.main.geometry('800x400')
#         self.main.title('Audio Recorder and Transcriber')
#
#         self.CHUNK = chunk
#         self.FORMAT = frmat
#         self.CHANNELS = channels
#         self.RATE = rate
#         self.p = py
#         self.frames = []
#         self.stream = None
#         self.is_recording = False
#
#         self.transcriber = WhisperTranscriber()
#
#         self.setup_ui()
#         self.audio_handler = AudioHandler()
#
#         tk.mainloop()
#
#     def setup_ui(self):
#         self.buttons = tk.Frame(self.main, padx=20, pady=20)
#         self.buttons.pack(fill=tk.BOTH)
#
#         self.strt_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Start Recording',
#                                   command=self.start_record)
#         self.strt_rec.grid(row=0, column=0, padx=50, pady=5)
#
#         self.stop_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Stop Recording', command=self.stop)
#         self.stop_rec.grid(row=1, column=0, padx=50, pady=5)
#
#         self.pause_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Pause', command=self.pause)
#         self.pause_rec.grid(row=0, column=1, padx=50, pady=5)
#
#         self.resume_rec = tk.Button(self.buttons, width=10, padx=10, pady=5, text='Resume', command=self.resume)
#         self.resume_rec.grid(row=1, column=1, padx=50, pady=5)
#
#         self.transcription_label = tk.Label(self.main, text="Transcriptions:", padx=20, pady=20)
#         self.transcription_label.pack()
#
#         self.transcription_text = tk.Text(self.main, wrap=tk.WORD, height=10, width=80)
#         self.transcription_text.pack()
#
#     def start_record(self):
#         self.is_recording = True
#         self.frames = []
#         self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
#                                   frames_per_buffer=self.CHUNK)
#         threading.Thread(target=self.record).start()
#
#     def record(self):
#         accumulated_frames = []
#         accumulated_duration = 0
#         chunk_duration = self.CHUNK / self.RATE
#
#         while self.is_recording:
#             data = self.stream.read(self.CHUNK, exception_on_overflow=False)
#             self.frames.append(data)
#             accumulated_frames.append(data)
#             accumulated_duration += chunk_duration
#
#             if accumulated_duration >= 5:  # Accumulate approximately 5 seconds of audio
#                 chunk_file = "../temp_chunk.wav"
#                 wf = wave.open(chunk_file, 'wb')
#                 wf.setnchannels(self.CHANNELS)
#                 wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
#                 wf.setframerate(self.RATE)
#                 wf.writeframes(b''.join(accumulated_frames))
#                 wf.close()
#
#                 self.process_transcription(chunk_file)
#
#                 accumulated_frames = []  # Clear accumulated frames after processing
#                 accumulated_duration = 0
#
#             self.main.update()
#
#     def stop(self):
#         self.is_recording = False
#         self.stream.close()
#         self.audio_handler.close()
#
#     def pause(self):
#         self.is_recording = False
#
#     def resume(self):
#         self.is_recording = True
#         threading.Thread(target=self.record).start()
#
#     def process_transcription(self, file_path):
#         transcription = self.transcriber.transcribe_chunk(file_path)
#         text = Text(transcription)
#         sentiment = text.get_nltk_sentiment(True)
#         result = transcription + " - " + sentiment
#
#         self.main.after(0, self.update_transcription_text, result)
#         os.remove(file_path)
#
#     def update_transcription_text(self, text):
#         self.transcription_text.insert(tk.END, text + "\n")
#
#
# class AudioHandler:
#     def __init__(self):
#         self.p = pyaudio.PyAudio()
#
#     def close(self):
#         self.p.terminate()
#
#
# class WhisperTranscriber:
#     def __init__(self, model_size="tiny"):
#         self.model = WhisperModel(model_size, device="cpu", compute_type="int16")
#
#     def transcribe_chunk(self, file_path):
#         segments, info = self.model.transcribe(file_path, beam_size=7)
#         transcription = ''.join(segment.text for segment in segments)
#         return transcription
#
#
# if __name__ == "__main__":
#     guiAUD = RecAUD()
