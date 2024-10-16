from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.dates as mdates
from datetime import datetime


import numpy as np
import pandas as pd


class SentimentPolarityPlot:
    def __init__(self, parent, figure):
        self.figure = figure

        self.ax = figure.add_subplot(111)  # Use the entire figure for the sentiment polarity plot

        main_colour = '#0d0d0d'
        secondary_colour = '#1a1a1a'
        Text_colour = '#0d47a1'

        # Set up the figure's properties
        self.ax.set_facecolor('#0d0d0d')
        self.ax.tick_params(colors=Text_colour)
        self.ax.xaxis.label.set_color(Text_colour)
        self.ax.yaxis.label.set_color(Text_colour)

        self.ax.axhline(y=0, color='#1a1a1a', linestyle='--', linewidth=1)

        self.canvas = FigureCanvasTkAgg(self.figure, parent)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ax.tick_params(axis='x', direction='in', pad=-15, labelsize=7)
        self.ax.tick_params(axis='y', direction='in', pad=-30, labelsize=7)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.margins(0)  # Remove margins
        self.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # Further minimize white space

        self.sentiment_polarity_data = []
        self.timestamps = []

    def add_polarity_data(self, polarity, timestamp):
        self.sentiment_polarity_data.append(polarity)
        # Convert the timestamp string to a datetime object
        datetime_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.timestamps.append(datetime_obj)
        self.update_polarity_plot()

    def update_polarity_plot(self):
        self.ax.clear()
        self.ax.plot(self.timestamps, self.sentiment_polarity_data, color='blue')
        self.ax.axhline(y=0, color='#1a1a1a', linestyle='--', linewidth=1)  # Line at y=0

        # Shading areas above 0.4 green and below -0.4 red
        self.ax.fill_between(self.timestamps, 0.4, 1.5, color='green', alpha=0.3)
        self.ax.fill_between(self.timestamps, -1.5, -0.4, color='red', alpha=0.3)

        self.ax.set_title("Sentiment Polarity Over Time", color='black')
        self.ax.set_xlabel("Time", color='black')
        self.ax.set_ylabel("Polarity", color='black')

        # Format the x-axis to show time in "HH:MM:SS"
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        self.ax.set_ylim(-1.5, 1.5)

        self.ax.tick_params(axis='x', direction='in', pad=-15, labelsize=10)
        self.ax.tick_params(axis='y', direction='in', pad=-30, labelsize=10)

        self.ax.margins(0)  # Remove margins
        self.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # Further minimize white space

        self.canvas.draw()
