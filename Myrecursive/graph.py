import pandas as pd
import matplotlib.pyplot as plt

# Assuming the CSV data is saved in a file named 'data.csv'
data = pd.read_csv('query_times.csv')

# Plotting the data
plt.figure(figsize=(10,  6))
plt.plot(data['Query'], data['Time Taken (ms)'], marker='o')
plt.title('Query Time Taken Over Time')
plt.xlabel('Query')
plt.ylabel('Time Taken (ms)')
plt.grid(True)
plt.show()
