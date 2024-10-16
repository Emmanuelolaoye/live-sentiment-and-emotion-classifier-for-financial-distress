# # gui_handler.py
#
# import tkinter as tk
# from datetime import datetime
#
#
# class UIHandler:
#     def __init__(self, parent):
#         self.parent = parent
#         self.main = parent.main
#
#     def setup_ui(self):
#         self.main.configure(bg='#1a1a1a')
#
#         self.buttons = tk.Frame(self.main, padx=10, pady=10, bg='#1a1a1a')
#         self.buttons.grid(row=0, column=0, columnspan=2, sticky="ew")
#
#         button_bg = '#0d0d0d'
#         button_fg = '#0d47a1'
#
#         self.strt_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Start Recording',
#                                   command=self.parent.audio_handler.start_record, bg=button_bg, fg=button_fg)
#         self.strt_rec.grid(row=0, column=0, padx=10, pady=5)
#
#         self.stop_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Stop Recording',
#                                   command=self.parent.audio_handler.stop, bg=button_bg, fg=button_fg)
#         self.stop_rec.grid(row=0, column=1, padx=10, pady=5)
#
#         self.pause_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Pause',
#                                    command=self.parent.audio_handler.pause, bg=button_bg, fg=button_fg)
#         self.pause_rec.grid(row=0, column=2, padx=10, pady=5)
#
#         self.resume_rec = tk.Button(self.buttons, width=10, padx=5, pady=5, text='Resume',
#                                     command=self.parent.audio_handler.resume, bg=button_bg, fg=button_fg)
#         self.resume_rec.grid(row=0, column=3, padx=10, pady=5)
#
#
#
#
#
#
#         self.transcription_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')
#         self.transcription_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
#
#         self.transcription_label = tk.Label(self.transcription_frame, text="Transcriptions:",
#                                             padx=0, pady=0, bg='#1a1a1a',
#                                             fg=button_fg)
#         self.transcription_label.pack()
#
#         # Create horizontal scrollbar
#         h_scroll = tk.Scrollbar(self.transcription_frame, orient='horizontal')
#         h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
#
#         # Create vertical scrollbar
#         v_scroll = tk.Scrollbar(self.transcription_frame, orient='vertical')
#         v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
#
#         self.transcription_text = tk.Text(self.transcription_frame, wrap=tk.NONE, height=20, width=110,
#                                           bg='#0d0d0d', fg='white', insertbackground='white',
#                                           xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
#         self.transcription_text.pack(fill="both", expand=True)
#
#         # Configure scrollbars
#         h_scroll.config(command=self.transcription_text.xview)
#         v_scroll.config(command=self.transcription_text.yview)
#
#         # Assign the transcription_text widget to the parent (RecAUD)
#         self.parent.transcription_text = self.transcription_text
#
#         # Add tag for grey text
#         self.transcription_text.tag_configure('grey', foreground='#808080')
#
#
#
#
#
#         self.sentiment_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')
#         self.sentiment_frame.grid(row=1, column=1, padx=0, pady=0, sticky='nsew')
#
#         self.sentiment_label = tk.Label(self.sentiment_frame, text="Sentiments:", padx=0, pady=0, bg='#1a1a1a',
#                                         fg=button_fg)
#         self.sentiment_label.pack()
#
#         # Create vertical scrollbar
#         v_scroll_sentiment = tk.Scrollbar(self.sentiment_frame, orient='vertical')
#         v_scroll_sentiment.pack(side=tk.RIGHT, fill=tk.Y)
#
#         self.sentiment_text = tk.Text(self.sentiment_frame, wrap=tk.WORD, height=20, width=20,
#                                       bg='#0d0d0d', fg='white', insertbackground='white',
#                                       yscrollcommand=v_scroll_sentiment.set)
#         self.sentiment_text.pack(fill="both", expand=True)
#
#         # Configure scrollbar
#         v_scroll_sentiment.config(command=self.sentiment_text.yview)
#
#         # Assign the sentiment_text widget to the parent (RecAUD)
#         self.parent.sentiment_text = self.sentiment_text
#
#
#         self.emotion_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')
#         self.emotion_frame.grid(row=1, column=2, padx=0, pady=0, sticky='nsew')
#
#         self.emotion_label = tk.Label(self.emotion_frame, text="Emotions:", padx=0, pady=0, bg='#1a1a1a',
#                                       fg=button_fg)
#         self.emotion_label.pack()
#
#         # Create vertical scrollbar
#         v_scroll_emotion = tk.Scrollbar(self.emotion_frame, orient='vertical')
#         v_scroll_emotion.pack(side=tk.RIGHT, fill=tk.Y)
#
#         self.emotion_text = tk.Text(self.emotion_frame, wrap=tk.WORD, height=20, width=20,
#                                     bg='#0d0d0d', fg='white', insertbackground='white',
#                                     yscrollcommand=v_scroll_emotion.set)
#         self.emotion_text.pack(fill="both", expand=True)
#
#         # Configure scrollbar
#         v_scroll_emotion.config(command=self.emotion_text.yview)
#
#         # Assign the emotion_text widget to the parent (RecAUD)
#         self.parent.emotion_text = self.emotion_text
#
#
#
#
#
#
#
#         self.main.grid_columnconfigure(0, weight=1)
#         self.main.grid_columnconfigure(1, weight=1)
#         self.main.grid_rowconfigure(1, weight=1)
#
#     # def update_transcription_text(self, text):
#     #     self.parent.transcription_text.insert(tk.END, text + "\n")
#     #     self.parent.transcription_text.see(tk.END)  # Scroll to the bottom
#     #
#     # def update_transcription_date_with_colour(self, date, colour):
#     #     self.parent.transcription_text.insert(tk.END, date, colour)
#     #     self.parent.transcription_text.see(tk.END)  # Scroll to the bottom
#     #
#     # def update_sentiment_text(self, sentiment):
#     #     self.parent.sentiment_text.insert(tk.END, sentiment + "\n")
#     #     self.parent.sentiment_text.see(tk.END)  # Scroll to the bottom
#     #
#     #
#     # def update_emotion_text(self, sentiment):
#     #     self.parent.emotion_text.insert(tk.END, sentiment + "\n")
#     #     self.parent.emotion_text.see(tk.END)  # Scroll to the bottom
