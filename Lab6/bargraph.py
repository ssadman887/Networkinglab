import matplotlib.pyplot as plt
import numpy as np

# Define the labels and values
labels = ['Reno', 'New Reno']
upload_values = [6217648,7302366]  # replace with your upload values
download_values = [6152039,7240279]  # replace with your download values

# Define the x locations for the groups
x = np.arange(len(labels))

# Define the width of the bars
width = 0.35

# Plot the data
plt.figure(figsize=(10,6))
plt.bar(x - width/2, upload_values, width, label='Upload')
plt.bar(x + width/2, download_values, width, label='Download')

# Add labels and title
plt.xlabel('Tasks')
plt.ylabel('Bytes per second')
plt.title('Throughput comparison')

# Add xticks
plt.xticks(x, labels)

# Add legend
plt.legend()

# Show the plot
plt.show()