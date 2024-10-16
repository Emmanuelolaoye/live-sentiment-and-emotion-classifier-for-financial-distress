# import sys
# import tkinter as tk
# import pyaudio
# import wave
# from tkinter.filedialog import asksaveasfilename
#
# from live_text_captioning.whisper_transcriber import WhisperTranscriber
# from text_sentiment_analyser.text import Text
# from faster_whisper import WhisperModel
# import threading
# import os
#
#
# class RecAUD:
#     def __init__(self, chunk=2048, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):
#         self.main = tk.Tk()
#         self.main.geometry('1500x300')
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
#         # Main window background color
#         self.main.configure(bg='#1a1a1a')  # Very dark grey background
#
#         self.buttons = tk.Frame(self.main, padx=10, pady=10, bg='#1a1a1a')  # Very dark grey background
#         self.buttons.grid(row=0, column=0, columnspan=2, sticky="ew")
#
#         button_bg = '#0d0d0d'  # Black background for buttons
#         button_fg = '#0d47a1'  # Dark blue text color for buttons
#
#         self.strt_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Start Recording',
#                                   command=self.start_record, bg=button_bg, fg=button_fg)
#         self.strt_rec.grid(row=0, column=0, padx=10, pady=5)
#
#         self.stop_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Stop Recording',
#                                   command=self.stop, bg=button_bg, fg=button_fg)
#         self.stop_rec.grid(row=0, column=1, padx=10, pady=5)
#
#         self.pause_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Pause',
#                                    command=self.pause, bg=button_bg, fg=button_fg)
#         self.pause_rec.grid(row=0, column=2, padx=10, pady=5)
#
#         self.resume_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Resume',
#                                     command=self.resume, bg=button_bg, fg=button_fg)
#         self.resume_rec.grid(row=0, column=3, padx=10, pady=5)
#
#         # Frame for transcription
#         self.transcription_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')  # Very dark grey background
#         self.transcription_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
#
#         self.transcription_label = tk.Label(self.transcription_frame, text="Transcriptions:",
#                                             padx=0, pady=0, bg='#1a1a1a',
#                                             fg=button_fg)  # Label with dark grey bg and blue text
#         self.transcription_label.pack()
#
#         self.transcription_text = tk.Text(self.transcription_frame, wrap=tk.WORD, height=20, width=110,
#                                           bg='#0d0d0d', fg='white',
#                                           insertbackground='white')  # Text widget with black bg and white text
#         self.transcription_text.pack(fill="both", expand=True)
#
#         # Frame for sentiment
#         self.sentiment_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')  # Very dark grey background
#         self.sentiment_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
#
#         self.sentiment_label = tk.Label(self.sentiment_frame, text="Sentiments:",
#                                         padx=0, pady=0, bg='#1a1a1a',
#                                         fg=button_fg)  # Label with dark grey bg and blue text
#         self.sentiment_label.pack()
#
#         self.sentiment_text = tk.Text(self.sentiment_frame, wrap=tk.WORD, height=20, width=70,
#                                       bg='#0d0d0d', fg='white',
#                                       insertbackground='white')  # Text widget with black bg and white text
#         self.sentiment_text.pack(fill="both", expand=True)
#
#         # Configure the grid to make columns and rows expand proportionally
#         self.main.grid_columnconfigure(0, weight=1)
#         self.main.grid_columnconfigure(1, weight=1)
#         self.main.grid_rowconfigure(1, weight=1)
#
#     def start_record(self):
#         self.is_recording = True
#         self.frames = []
#         self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
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
#                 chunk_file = "temp_chunk.wav"
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
#         #sentiment = text.get_nltk_sentiment(True)
#         finbert_sentiment, finbert_value = text.get_finbert_sentiment()
#         sentiment = f"Sentiment: {finbert_sentiment}, Value: {finbert_value:.4f}"
#
#
#         self.main.after(0, self.update_transcription_text, transcription)
#         self.main.after(0, self.update_sentiment_text, sentiment)
#         os.remove(file_path)
#
#     def update_transcription_text(self, text):
#         self.transcription_text.insert(tk.END, text + "\n")
#
#     def update_sentiment_text(self, sentiment):
#         self.sentiment_text.insert(tk.END, sentiment + "\n")
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
# if __name__ == "__main__":
#     guiAUD = RecAUD()
