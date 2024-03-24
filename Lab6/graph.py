import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data = pd.read_csv('data.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data['loss_rate'], data['rtt'])

# Add labels and title
plt.xlabel('Error(%)')
plt.ylabel('Round Trip Time(milliseconds)')
plt.title('TCP Loss Rate vs RTT')

# Show the plot
plt.show()