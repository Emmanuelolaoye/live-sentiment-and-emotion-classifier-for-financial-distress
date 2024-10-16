from alpha_vantage.timeseries import TimeSeries
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
import pandas as pd

class LiveStockPlot(tk.Frame):
    def __init__(self, parent, figure):
        super().__init__(parent)
        self.figure = figure
        self.api_key = 'D8WAS4Q08ZHKSI4K'
        self.ax = figure.add_subplot(211)  # Use the upper subplot for the live stock plot
        self.ts = TimeSeries(key=self.api_key, output_format='pandas')

        # Set up the figure's properties
        self.ax.set_facecolor('#0d0d0d')  # Dark background for the plot
        self.configure(bg='#1a1a1a')  # Set the frame background to match the dark theme

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.running = False

    def fetch_stock_data(self, symbol, specific_day=None):
        print('fetch_stock_data')
        try:
            data, meta_data = self.ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
            print(data)
            if specific_day:
                # Filter the data for the specific day
                data_filtered = data[data.index.date == pd.to_datetime(specific_day).date()]
                print(data_filtered)
                return data_filtered['4. close']
            else:
                return data['4. close']
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise

    def update_plot(self, symbol, specific_day=None):
        try:
            data = self.fetch_stock_data(symbol, specific_day)
            self.ax.clear()
            self.ax.set_facecolor('#1a1a1a')  # Keep the background dark after clearing
            times = data.index
            prices = data.values

            if len(times) == 0:
                self.ax.set_title(f"No data available for {symbol.upper()} on {specific_day}", color='white')
            else:
                self.ax.set_xlim([times[0], times[-1]])

                start_hour = times[0].replace(minute=0, second=0, microsecond=0)
                end_hour = start_hour + np.timedelta64(1, 'h')

                while start_hour < times[-1]:
                    color = 'grey' if start_hour.hour % 2 == 0 else '#1a1a1a'
                    self.ax.axvspan(start_hour, end_hour, facecolor=color, alpha=0.5)
                    start_hour += np.timedelta64(1, 'h')
                    end_hour = start_hour + np.timedelta64(1, 'h')

                for i in range(1, len(prices)):
                    color = 'green' if prices[i] > prices[i - 1] else 'red'
                    self.ax.plot(times[i - 1:i + 1], prices[i - 1:i + 1], color=color)

                self.ax.set_title(f"Stock Prices: {symbol.upper()} on {specific_day}", color='white')
                self.ax.set_xlabel("Time", color='white')
                self.ax.set_ylabel("Price", color='white')

                latest_price = prices[-1]
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

        if self.running:
            self.after(60000, self.update_plot, symbol, specific_day)  # update every 60 seconds

    def plot_stock(self, symbol, specific_day=None):
        symbol = symbol.strip()
        if symbol:
            self.running = True
            self.update_plot(symbol, specific_day)

    def stop_plotting(self):
        self.running = False
