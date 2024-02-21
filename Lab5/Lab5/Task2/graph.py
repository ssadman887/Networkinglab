import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data1 = pd.read_csv('samplertt.csv')
data2 = pd.read_csv('estimatedrtt.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data1['no'], data1['sampleRTT'], label='Sample RTT')
plt.plot(data2['no'], data2['estimatedRTT'], label='Estimated RTT')

# Add labels and title
plt.xlabel('no')
plt.ylabel('time in milliseconds')
plt.title('RTT comparison')
plt.legend()

# Show the plot
plt.show()