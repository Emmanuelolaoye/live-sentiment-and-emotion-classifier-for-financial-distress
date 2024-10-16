import matplotlib.pyplot as plt
import pandas as pd

# Sample data
data = {
    'Date': ['2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04', '2024-08-05'],
    'Sentiment Polarity': [0.1, -0.2, 0.3, -0.1, 0.2],
    'Stock Price': [150, 145, 155, 148, 152]
}

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Stock Price on the primary y-axis
ax1.plot(df['Date'], df['Stock Price'], color='blue', marker='o', label='Stock Price')
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis to plot Sentiment Polarity
ax2 = ax1.twinx()
ax2.plot(df['Date'], df['Sentiment Polarity'], color='red', marker='x', label='Sentiment Polarity')
ax2.set_ylabel('Sentiment Polarity', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Title and grid
plt.title('Sentiment Polarity and Stock Price Over Time')
plt.grid(True)

# Show the plot
plt.show()