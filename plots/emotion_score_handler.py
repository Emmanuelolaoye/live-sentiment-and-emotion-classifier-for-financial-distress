import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


class EmotionScorePlot:
    def __init__(self, parent, figure):
        self.figure = figure
        self.ax = figure.add_subplot(111)  # Use the entire figure for the emotion score plot

        self.ax.set_facecolor('#0d0d0d')

        self.canvas = FigureCanvasTkAgg(self.figure, parent)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ax.margins(0)  # Remove margins
        self.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # Further minimize white space

        self.emotion_data_over_time = []

    def add_emotion_data(self, data):
        """
        Adds emotion data as a new time point to the plot.

        data: list of dictionaries containing 'Emotion' and 'Score'.
        Example:
        [
            {'Emotion': 'angry', 'Score': '13.1%'},
            {'Emotion': 'calm', 'Score': '11.5%'},
            ...
        ]
        """
        # Convert scores to float and strip the '%' sign
        processed_data = {item['Emotion']: float(item['Score'].strip('%')) for item in data}
        self.emotion_data_over_time.append(processed_data)

        # Convert list of dictionaries to DataFrame
        self.df = pd.DataFrame(self.emotion_data_over_time)
        self.df.index.name = 'Time'  # Use the index as the time point
        self.update_emotion_plot()

    def update_emotion_plot(self):
        self.ax.clear()
        self.ax.set_facecolor('#0d0d0d')
        self.df.plot(kind='area', stacked=True, alpha=0.7, ax=self.ax)

        # Flip the x and y ticks to be inside the graph and adjust tick labels
        self.ax.tick_params(axis='x', direction='in', pad=-15, labelsize=10)
        self.ax.tick_params(axis='y', direction='in', pad=-30, labelsize=10)

        self.ax.margins(0)  # Remove margins
        self.figure.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # Further minimize white space

        self.canvas.draw()


# Example usage (you can integrate this within your Tkinter app):
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Emotion Score Over Time")
#
#     fig = plt.Figure(figsize=(8, 5))
#     emotion_plot = EmotionScorePlot(root, fig)
#
#     # Sample data for different time points
#     emotion_data_1 = [
#         {'Emotion': 'angry', 'Score': '13.1%'},
#         {'Emotion': 'calm', 'Score': '11.5%'},
#         {'Emotion': 'disgust', 'Score': '14.7%'},
#         {'Emotion': 'fearful', 'Score': '11.2%'},
#         {'Emotion': 'happy', 'Score': '12.7%'},
#         {'Emotion': 'neutral', 'Score': '12.1%'},
#         {'Emotion': 'sad', 'Score': '9.5%'},
#         {'Emotion': 'surprised', 'Score': '15.1%'}
#     ]
#
#     emotion_data_2 = [
#         {'Emotion': 'angry', 'Score': '12.5%'},
#         {'Emotion': 'calm', 'Score': '10.8%'},
#         {'Emotion': 'disgust', 'Score': '13.7%'},
#         {'Emotion': 'fearful', 'Score': '10.9%'},
#         {'Emotion': 'happy', 'Score': '13.1%'},
#         {'Emotion': 'neutral', 'Score': '11.9%'},
#         {'Emotion': 'sad', 'Score': '10.0%'},
#         {'Emotion': 'surprised', 'Score': '14.5%'}
#     ]
#
#     # Add data for different time points
#     emotion_plot.add_emotion_data(emotion_data_1)
#     emotion_plot.add_emotion_data(emotion_data_2)
#
#     emotion_plot.update_emotion_plot()
#
#     root.mainloop()
