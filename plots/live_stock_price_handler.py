import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import threading
import numpy as np
import yfinance as yf

class LiveStockPlot:
    def __init__(self, parent_frame, figure):
        main_colour = '#0d0d0d'
        secondary_colour = '#1a1a1a'
        text_colour = '#0d47a1'

        self.parent_frame = parent_frame
        self.figure = figure
        self.ax = self.figure.add_subplot(111)

        self.ax.set_facecolor(main_colour)
        self.ax.tick_params(colors=text_colour)
        self.ax.xaxis.label.set_color(text_colour)
        self.ax.yaxis.label.set_color(text_colour)

        self.canvas = FigureCanvasTkAgg(self.figure, self.parent_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ax.tick_params(axis='x', direction='in', pad=-15, labelsize=7)
        self.ax.tick_params(axis='y', direction='in', pad=-30, labelsize=7)

        self.ax.margins(0)  # Remove margins
        self.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # Further minimize white space

        self.running = False

    def fetch_stock_data(self, symbol):
        stock_data = yf.Ticker(symbol)
        hist = stock_data.history(period="1d", interval="1m")
        return hist['Close']

    def update_plot(self, symbol):
        data = self.fetch_stock_data(symbol)
        if data.empty:
            print(f"No data fetched for symbol {symbol}.")
            return

        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')  # Keep the background dark after clearing
        times = data.index
        prices = data.values

        self.ax.set_xlim([times[0], times[-1]])

        # Format the x-axis to show only hour and minute
        self.ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

        start_hour = times[0].replace(minute=0, second=0, microsecond=0)
        end_hour = start_hour + np.timedelta64(1, 'h')

        while start_hour < times[-1]:
            color = '#0d0d0d' if start_hour.hour % 2 == 0 else '#1a1a1a'
            self.ax.axvspan(start_hour, end_hour, facecolor=color)
            start_hour += np.timedelta64(1, 'h')
            end_hour = start_hour + np.timedelta64(1, 'h')

        for i in range(1, len(prices)):
            color = 'green' if prices[i] > prices[i - 1] else 'red'
            self.ax.plot(times[i - 1:i + 1], prices[i - 1:i + 1], color=color)

        self.ax.set_title(f"Live Stock Prices: {symbol.upper()}", color='white')

        latest_price = prices[-1]
        price_color = 'green' if latest_price > prices[-2] else 'red'

        self.ax.text(times[-1] + np.timedelta64(1, 'm'), latest_price, f"{latest_price:.2f}",
                     fontsize=9, verticalalignment='center',
                     horizontalalignment='left',
                     color="white",
                     bbox=dict(boxstyle="round,pad=0.2", edgecolor=price_color, facecolor=price_color),
                     transform=self.ax.transData)

        self.ax.tick_params(axis='x', direction='in', pad=-15, labelsize=10)
        self.ax.tick_params(axis='y', direction='in', pad=-30, labelsize=10)

        self.ax.margins(0)  # Remove margins
        self.figure.subplots_adjust(left=0.01, right=0.95, top=0.99, bottom=0.01)  # Further minimize white space

        self.canvas.draw()

    def plot_stock(self, symbol):
        if symbol:
            self.running = True
            threading.Thread(target=self.update_plot, args=(symbol,), daemon=True).start()

    def stop_plot(self):
        self.running = False
