import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from plots.live_stock_price_handler import LiveStockPlot
from plots.polarity_handler import SentimentPolarityPlot
from plots.emotion_score_handler import EmotionScorePlot
# from plots.vanguard import LiveStockPlot


class UIHandler:
    def __init__(self, parent):
        self.parent = parent
        self.main = parent.main

    def setup_ui(self):
        main_colour = '#0d0d0d'
        secondary_colour = '#1a1a1a'
        text_colour = '#0d47a1'

        self.main.configure(bg=main_colour)

        # Frame for input fields and buttons
        self.buttons = tk.Frame(self.main, padx=0, pady=0, bg=main_colour, height=70)
        self.buttons.pack(side=tk.TOP, fill=tk.X)

        # Buttons for recording
        self.start_recording_button = tk.Button(self.buttons, width=10, padx=5, pady=0, text='Start Recording',
                                                command=self.parent.audio_handler.start_record, bg=main_colour,
                                                fg=text_colour)
        self.start_recording_button.pack(side=tk.LEFT, padx=10, pady=0)

        self.stop_recording_button = tk.Button(self.buttons, width=10, padx=5, pady=0, text='Stop Recording',
                                               command=self.parent.audio_handler.stop, bg=main_colour, fg=text_colour)
        self.stop_recording_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.pause_recording_button = tk.Button(self.buttons, width=10, padx=5, pady=0, text='Pause',
                                                command=self.parent.audio_handler.pause, bg=main_colour, fg=text_colour)
        self.pause_recording_button.pack(side=tk.LEFT, padx=10, pady=0)

        self.resume_rec = tk.Button(self.buttons, width=10, padx=5, pady=0, text='Resume',
                                    command=self.parent.audio_handler.resume, bg=main_colour, fg=text_colour)
        self.resume_rec.pack(side=tk.LEFT, padx=10, pady=0)

        # Input frame for stock symbol
        self.input_frame = tk.Frame(self.buttons, bg=main_colour)
        self.input_frame.pack(side=tk.LEFT, padx=10, pady=5)

        self.label = tk.Label(self.input_frame, text="Enter Ticker Symbol (e.g., BARC for Barclays):",
                              background=main_colour, foreground=text_colour)
        self.label.pack(side=tk.LEFT, padx=5)

        self.symbol_entry = tk.Entry(self.input_frame, bg=main_colour, fg=text_colour)
        self.symbol_entry.pack(side=tk.LEFT, padx=5)

        self.plot_button = tk.Button(self.input_frame, text="Search", command=self.plot_stock, bg=main_colour,
                                     fg=text_colour)
        self.plot_button.pack(side=tk.LEFT, padx=5)
        #
        # # Frame for plots
        # self.plots = tk.Frame(self.main, bg="orange", height=400, width=500)
        # self.plots.pack(side=tk.TOP, fill=tk.X)
        #
        # # self.figure_box = tk.Frame(self.plots, bg=main_colour, width=1000, height=400)
        # # self.figure_box.pack(side=tk.LEFT, fill=tk.X)
        # #
        # # self.area_box = tk.Frame(self.plots, bg="green", width=500, height=400)
        # # self.area_box.pack(side=tk.RIGHT, fill=tk.X)
        # #
        # # # Create a single figure to be shared between both plots
        # # self.figure = Figure(figsize=(10, 4), facecolor=secondary_colour)
        # #
        # # # Initialize LiveStockPlot and SentimentPolarityPlot with the shared figure
        # # self.plot_frame = LiveStockPlot(self.figure_box, self.figure)
        # # self.polarity_frame = SentimentPolarityPlot(self.figure_box, self.figure)
        #
        #
        # # Frame for the entire figure area
        # self.figure_box = tk.Frame(self.plots, bg='#0d0d0d', width=1000, height=400)
        # self.figure_box.pack(side=tk.LEFT, fill=tk.X)
        # self.figure_box.pack_propagate(False)
        #
        # # self.live_stock_box = tk.Frame(self.figure_box, bg="green", width=1000, height=200)
        # # self.live_stock_box.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # # self.live_stock_box.pack_propagate(False)
        #
        # self.sentiment_polarity_box = tk.Frame(self.figure_box, bg="white", width=1000, height=200)
        # self.sentiment_polarity_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # self.sentiment_polarity_box.pack_propagate(False)
        #
        # # Create separate figures for each plot
        # self.sentiment_polarity_figure = Figure(figsize=(7, 4), facecolor='#1a1a1a')
        # self.live_stock_figure = Figure(figsize=(7, 4), facecolor='#1a1a1a')
        #

        # # Initialize LiveStockPlot and SentimentPolarityPlot with their respective figures and frames
        # # self.plot_frame = SentimentPolarityPlot(self.live_stock_box, self.live_stock_figure)
        # self.polarity_frame = LiveStockPlot(self.sentiment_polarity_box, self.sentiment_polarity_figure)

        # Force an initial drawing of the stock plot to ensure it shows up
        # self.plot_frame.canvas.draw()
        # self.plot_frame.canvas.get_tk_widget().update_idletasks()

        #todo buttons taken from here

        # # Frame for labels (transcription, sentiment, and emotion)
        # labels = tk.Frame(self.main, bg="teal", height=500)
        # labels.pack(side=tk.BOTTOM, fill=tk.X)
        # labels.pack_propagate(False)  # Ensure the frames don't auto-resize based on content

        # Frame for plots
        self.plots = tk.Frame(self.main, bg="yellow", height=400, width=500)
        self.plots.pack(side=tk.TOP, fill=tk.X)

        # Frame for the entire figure area
        self.figure_box = tk.Frame(self.plots, bg='#0d0d0d', width=1000, height=400)
        self.figure_box.pack(side=tk.LEFT, fill=tk.X)
        self.figure_box.pack_propagate(False)


        self.area_box = tk.Frame(self.plots, bg="green", width=500, height=400)
        self.area_box.pack(side=tk.RIGHT, fill=tk.X)



        self.live_stock_box = tk.Frame(self.figure_box, bg="orange", width=1000, height=200)
        self.live_stock_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.live_stock_box.pack_propagate(False)

        self.sentiment_polarity_box = tk.Frame(self.figure_box, bg="white", width=1000, height=200)
        self.sentiment_polarity_box.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.sentiment_polarity_box.pack_propagate(False)

        # Create a figure for polarity_frame
        self.sentiment_polarity_figure = Figure(figsize=(7, 4), facecolor='#1a1a1a')
        self.live_stock_figure = Figure(figsize=(7, 4), facecolor='#1a1a1a')
        self.emotion_figure = Figure(figsize=(5, 4), facecolor='#1a1a1a')

        # Initialize polarity_frame as a LiveStockPlot
        self.plot_frame = LiveStockPlot(self.live_stock_box, self.live_stock_figure)
        self.polarity_frame = SentimentPolarityPlot(self.sentiment_polarity_box, self.sentiment_polarity_figure)
        self.emotion_plot_frame = EmotionScorePlot(self.area_box, self.emotion_figure)

        #
        # self.polarity_frame.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # Transcription Frame
        self.transcription_frame = tk.Frame(self.main, bg='#1a1a1a', width=1000, height=500)
        self.transcription_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.transcription_frame.pack_propagate(False)

        self.transcription_label = tk.Label(self.transcription_frame, text="Transcriptions:", bg='#1a1a1a',
                                            fg=text_colour)
        self.transcription_label.pack()

        h_scroll = tk.Scrollbar(self.transcription_frame, orient='horizontal')
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        v_scroll = tk.Scrollbar(self.transcription_frame, orient='vertical')
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.transcription_text = tk.Text(self.transcription_frame, wrap=tk.NONE, bg='#0d0d0d', fg='white',
                                          insertbackground='white', xscrollcommand=h_scroll.set,
                                          yscrollcommand=v_scroll.set)
        self.transcription_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scroll.config(command=self.transcription_text.xview)
        v_scroll.config(command=self.transcription_text.yview)

        # Sentiment Frame
        self.sentiment_frame = tk.Frame(self.main, bg='#1a1a1a', width=250, height=500)
        self.sentiment_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sentiment_frame.pack_propagate(False)

        self.sentiment_label = tk.Label(self.sentiment_frame, text="Sentiments:", bg='#1a1a1a', fg=text_colour)
        self.sentiment_label.pack()

        v_scroll_sentiment = tk.Scrollbar(self.sentiment_frame, orient='vertical')
        v_scroll_sentiment.pack(side=tk.RIGHT, fill=tk.Y)

        self.sentiment_text = tk.Text(self.sentiment_frame, wrap=tk.WORD, bg='#0d0d0d', fg='white',
                                      insertbackground='white',
                                      yscrollcommand=v_scroll_sentiment.set)
        self.sentiment_text.pack(fill="both", expand=True)

        v_scroll_sentiment.config(command=self.sentiment_text.yview)

        # Emotion Frame
        self.emotion_frame = tk.Frame(self.main, bg='#1a1a1a', width=250, height=500)
        self.emotion_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.emotion_frame.pack_propagate(False)

        emotion_label = tk.Label(self.emotion_frame, text="Emotions:", bg='#1a1a1a', fg=text_colour)
        emotion_label.pack()

        v_scroll_emotion = tk.Scrollbar(self.emotion_frame, orient='vertical')
        v_scroll_emotion.pack(side=tk.RIGHT, fill=tk.Y)

        self.emotion_text = tk.Text(self.emotion_frame, wrap=tk.WORD, bg='#0d0d0d', fg='white',
                                    insertbackground='white',
                                    yscrollcommand=v_scroll_emotion.set)
        self.emotion_text.pack(fill="both", expand=True)

        v_scroll_emotion.config(command=self.emotion_text.yview)

        # self.plot_frame.plot_stock("NVDA")

        # self.test_plot_aapl()

        # # Transcription, sentiment, and emotion text areas in the same row
        # self.transcription_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')
        # self.transcription_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #
        # self.transcription_label = tk.Label(self.transcription_frame, text="Transcriptions:",
        #                                     padx=0, pady=0, bg='#1a1a1a', fg=text_colour)
        # self.transcription_label.pack()
        #
        # h_scroll = tk.Scrollbar(self.transcription_frame, orient='horizontal')
        # h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        #
        # v_scroll = tk.Scrollbar(self.transcription_frame, orient='vertical')
        # v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        #
        # self.transcription_text = tk.Text(self.transcription_frame, wrap=tk.NONE, height=20, width=80,
        #                                   bg='#0d0d0d', fg='white', insertbackground='white',
        #                                   xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        # self.transcription_text.pack(fill="both", expand=True)
        #
        # h_scroll.config(command=self.transcription_text.xview)
        # v_scroll.config(command=self.transcription_text.yview)
        #
        # self.parent.transcription_text = self.transcription_text
        #
        # self.sentiment_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')
        # self.sentiment_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #
        # self.sentiment_label = tk.Label(self.sentiment_frame, text="Sentiments:", padx=0, pady=0, bg='#1a1a1a',
        #                                 fg=text_colour)
        # self.sentiment_label.pack()
        #
        # v_scroll_sentiment = tk.Scrollbar(self.sentiment_frame, orient='vertical')
        # v_scroll_sentiment.pack(side=tk.RIGHT, fill=tk.Y)
        #
        # self.sentiment_text = tk.Text(self.sentiment_frame, wrap=tk.WORD, height=20, width=30,
        #                               bg='#0d0d0d', fg='white', insertbackground='white',
        #                               yscrollcommand=v_scroll_sentiment.set)
        # self.sentiment_text.pack(fill="both", expand=True)
        #
        # v_scroll_sentiment.config(command=self.sentiment_text.yview)
        # self.parent.sentiment_text = self.sentiment_text
        #
        # self.emotion_frame = tk.Frame(self.main, padx=0, pady=0, bg='#1a1a1a')
        # self.emotion_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #
        # self.emotion_label = tk.Label(self.emotion_frame, text="Emotions:", padx=0, pady=0, bg='#1a1a1a',
        #                               fg=text_colour)
        # self.emotion_label.pack()
        #
        # v_scroll_emotion = tk.Scrollbar(self.emotion_frame, orient='vertical')
        # v_scroll_emotion.pack(side=tk.RIGHT, fill=tk.Y)
        #
        # self.emotion_text = tk.Text(self.emotion_frame, wrap=tk.WORD, height=20, width=30,
        #                             bg='#0d0d0d', fg='white', insertbackground='white',
        #                             yscrollcommand=v_scroll_emotion.set)
        # self.emotion_text.pack(fill="both", expand=True)
        #
        # v_scroll_emotion.config(command=self.emotion_text.yview)
        # self.parent.emotion_text = self.emotion_text

    def update_transcription_text(self, text):
        self.transcription_text.insert(tk.END, text + "\n")
        self.transcription_text.see(tk.END)  # Scroll to the bottom

    def update_transcription_date_with_colour(self, date, colour):
        self.transcription_text.insert(tk.END, date, colour)
        self.transcription_text.see(tk.END)  # Scroll to the bottom

    def update_sentiment_text(self, sentiment):
        self.sentiment_text.insert(tk.END, sentiment + "\n")
        self.sentiment_text.see(tk.END)  # Scroll to the bottom

    def update_emotion_text(self, sentiment):
        self.emotion_text.insert(tk.END, sentiment + "\n")
        self.emotion_text.see(tk.END)  # Scroll to the bottom

    def add_polarity_data(self, polarity,  date_time):  # TODO: fix here too
        self.polarity_frame.add_polarity_data(polarity, date_time)
        # self.parent.polarity_frame.add_polarity_data(polarity)

    def add_emotion_data(self, emotion):
        self.emotion_plot_frame.add_emotion_data(emotion)




    # def plot_stock(self):
    #     symbol = self.symbol_entry.get().strip()
    #     print(f"Symbol retrieved from entry: '{symbol}'")
    #     if symbol:
    #         self.plot_frame.plot_stock(symbol)
    #         self.plot_frame.canvas.draw # Delay drawing slightly
    #     else:
    #         print("No symbol provided.")
    def test_plot_aapl(self):
        print("Testing direct plot with AAPL")
        self.plot_frame.plot_stock("AAPL")
        self.plot_frame.canvas.draw()
        self.plot_frame.canvas.get_tk_widget().update_idletasks()  # Force the GUI to update

        # print(f"Attempting to plot: {symbol}")
        #
        # self.parent.plot_stock("AAPL")

    def plot_stock(self):
        symbol = self.symbol_entry.get().strip()
        if symbol:
            # if not symbol.endswith('.L'):
            #     symbol += '.L'  # Automatically add the LSE suffix if it's not provided
            self.plot_frame.plot_stock(symbol)
