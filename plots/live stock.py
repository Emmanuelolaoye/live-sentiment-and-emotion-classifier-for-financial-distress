import tkinter as tk
from tkinter import ttk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
import numpy as np
import matplotlib.dates as mdates

class LiveStockPlot(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Live Stock Prices")
        self.geometry("800x600")

        # Stock symbol input
        self.label = ttk.Label(self, text="Enter Stock Symbol (e.g., BARC for Barclays):")
        self.label.pack(pady=10)

        self.symbol_entry = ttk.Entry(self)
        self.symbol_entry.pack(pady=10)

        self.plot_button = ttk.Button(self, text="Plot Live Data", command=self.plot_stock)
        self.plot_button.pack(pady=10)

        # Figure for plotting
        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.running = False

    def fetch_stock_data(self, symbol):
        stock_data = yf.Ticker(symbol)
        hist = stock_data.history(period="1d", interval="1m")
        return hist['Close']


    def update_plot(self, symbol):
        try:
            data = self.fetch_stock_data(symbol)
            self.ax.clear()
            times = data.index
            prices = data.values

            self.ax.set_xlim([times[0], times[-1]])

            # Add alternating grey and white zones for every hour
            start_hour = times[0].replace(minute=0, second=0, microsecond=0)
            end_hour = start_hour + np.timedelta64(1, 'h')

            while start_hour < times[-1]:
                color = 'lightgrey' if start_hour.hour % 2 == 0 else 'white'
                self.ax.axvspan(start_hour, end_hour, facecolor=color, alpha=0.5)
                start_hour += np.timedelta64(1, 'h')
                end_hour = start_hour + np.timedelta64(1, 'h')

            for i in range(1, len(prices)):
                color = 'green' if prices[i] > prices[i - 1] else 'red'
                self.ax.plot(times[i - 1:i + 1], prices[i - 1:i + 1], color=color)

            self.ax.set_title(f"Live Stock Prices: {symbol.upper()}")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Price")

            latest_price = prices[-1]
            latest_time = times[-1]
            price_color = 'green' if latest_price > prices[-2] else 'red'

            self.ax.text(times[-1] + np.timedelta64(1, 'm'), latest_price, f"{latest_price:.2f}",
                         fontsize=9, verticalalignment='center',
                         horizontalalignment='left',
                         color="white",
                         bbox=dict(boxstyle="round,pad=0.2", edgecolor=price_color, facecolor=price_color),
                         transform=self.ax.transData)

            self.canvas.draw()
        except Exception as e:
            print(f"Error fetching or plotting data: {e}")

        # Schedule next update
        if self.running:
            self.after(60000, self.update_plot, symbol)  # update every 60 seconds


    def plot_stock(self):
        symbol = self.symbol_entry.get().strip()
        if symbol:
            if not symbol.endswith('.L'):
                symbol += '.L'
            self.running = True
            self.update_plot(symbol)  # Start the periodic update


    def on_close(self):
        self.running = False
        self.destroy()


if __name__ == "__main__":
    app = LiveStockPlot()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
