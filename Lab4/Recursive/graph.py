import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data = pd.read_csv('data.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data['request_no'], data['time_taken'])

# Add labels and title
plt.xlabel('Request_no')
plt.ylabel('Time taken in milliseconds')
plt.title('Time Delay over Request')

# Show the plot
plt.show()