import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data = pd.read_csv('congestion_data.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data['time'], data['cwnd'])

# Add labels and title
plt.xlabel('time(ms)')
plt.ylabel('cwnd')
plt.title('New Reno cwnd vs time')

# Show the plot
plt.show()