import tkinter as tk
from matplotlib.figure import Figure
from plots.live_stock_price_handler import LiveStockPlot
from plots.polarity_handler import SentimentPolarityPlot

# Define colors used in the application
main_colour = '#0d0d0d'
secondary_colour = '#1a1a1a'
text_colour = '#0d47a1'

# Create the main Tkinter window
main = tk.Tk()
main.geometry('1500x900')
main.title('PACK HELPER')
main.config(bg='grey')
main.resizable(width=False, height=False)

# Top frame containing buttons
buttons = tk.Frame(main, bg=main_colour, height=70)
buttons.pack(side=tk.TOP, fill=tk.X)

# Buttons for recording
start = tk.Button(buttons, width=10, padx=5, pady=0, text='Start Recording', bg=main_colour, fg=text_colour)
start.pack(side=tk.LEFT, padx=10, pady=0)

stop = tk.Button(buttons, width=10, padx=5, pady=0, text='Stop Recording', bg=main_colour, fg=text_colour)
stop.pack(side=tk.LEFT, padx=10, pady=0)

pause = tk.Button(buttons, width=10, padx=5, pady=0, text='Pause', bg=main_colour, fg=text_colour)
pause.pack(side=tk.LEFT, padx=10, pady=0)

resume = tk.Button(buttons, width=10, padx=5, pady=0, text='Resume', bg=main_colour, fg=text_colour)
resume.pack(side=tk.LEFT, padx=10, pady=0)

# Input frame for stock symbol
input_frame = tk.Frame(buttons, bg=main_colour)
input_frame.pack(side=tk.LEFT, padx=10, pady=5)

label = tk.Label(input_frame, text="Enter Ticker Symbol (e.g., BARC for Barclays):", bg=main_colour, fg=text_colour)
label.pack(side=tk.LEFT, padx=5)

symbol_entry = tk.Entry(input_frame, bg='#1a1a1a')
symbol_entry.pack(side=tk.LEFT, padx=5)

plot_button = tk.Button(input_frame, text="Search", bg=main_colour)
plot_button.pack(side=tk.LEFT, padx=5)



# Frame for plots
plots = tk.Frame(main, bg="orange", height=400, width=500)
plots.pack(side=tk.TOP, fill=tk.X)

figure_box = tk.Frame(plots, bg=main_colour, width=1000, height=400)
figure_box.pack(side=tk.LEFT, fill=tk.X)

area_box = tk.Frame(plots, bg="green", width=500, height=400)
area_box.pack(side=tk.RIGHT, fill=tk.X)

# Create a single figure to be shared between both plots
figure = Figure(figsize=(10, 4), facecolor=secondary_colour)

# Initialize LiveStockPlot and SentimentPolarityPlot with the shared figure
plot_frame = LiveStockPlot(figure_box, figure)
polarity_frame = SentimentPolarityPlot(figure_box, figure)

# Frame for labels (transcription, sentiment, and emotion)
labels = tk.Frame(main, bg="teal", height=500)
labels.pack(side=tk.BOTTOM, fill=tk.X)
labels.pack_propagate(False)  # Ensure the frames don't auto-resize based on content


# Transcription Frame
transcription_frame = tk.Frame(labels, bg='#1a1a1a', width=1000, height=500)
transcription_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
transcription_frame.pack_propagate(False)

transcription_label = tk.Label(transcription_frame, text="Transcriptions:", bg='#1a1a1a', fg=text_colour)
transcription_label.pack()

h_scroll = tk.Scrollbar(transcription_frame, orient='horizontal')
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

v_scroll = tk.Scrollbar(transcription_frame, orient='vertical')
v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

transcription_text = tk.Text(transcription_frame, wrap=tk.NONE, bg='#0d0d0d', fg='white',
                             insertbackground='white', xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
transcription_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

h_scroll.config(command=transcription_text.xview)
v_scroll.config(command=transcription_text.yview)

# Sentiment Frame
sentiment_frame = tk.Frame(labels, bg='#1a1a1a', width=250, height=500)
sentiment_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
sentiment_frame.pack_propagate(False)

sentiment_label = tk.Label(sentiment_frame, text="Sentiments:", bg='#1a1a1a', fg=text_colour)
sentiment_label.pack()

v_scroll_sentiment = tk.Scrollbar(sentiment_frame, orient='vertical')
v_scroll_sentiment.pack(side=tk.RIGHT, fill=tk.Y)

sentiment_text = tk.Text(sentiment_frame, wrap=tk.WORD, bg='#0d0d0d', fg='white', insertbackground='white',
                         yscrollcommand=v_scroll_sentiment.set)
sentiment_text.pack(fill="both", expand=True)

v_scroll_sentiment.config(command=sentiment_text.yview)

# Emotion Frame
emotion_frame = tk.Frame(labels, bg='#1a1a1a', width=250, height=500)
emotion_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
emotion_frame.pack_propagate(False)

emotion_label = tk.Label(emotion_frame, text="Emotions:", bg='#1a1a1a', fg=text_colour)
emotion_label.pack()

v_scroll_emotion = tk.Scrollbar(emotion_frame, orient='vertical')
v_scroll_emotion.pack(side=tk.RIGHT, fill=tk.Y)

emotion_text = tk.Text(emotion_frame, wrap=tk.WORD, bg='#0d0d0d', fg='white', insertbackground='white',
                       yscrollcommand=v_scroll_emotion.set)
emotion_text.pack(fill="both", expand=True)

v_scroll_emotion.config(command=emotion_text.yview)

# Start the main event loop
main.mainloop()
