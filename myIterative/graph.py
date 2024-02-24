import csv
import matplotlib.pyplot as plt

def plot_dns_queries():
    # Open the CSV file
    with open('dns_queries.csv', 'r') as file:
        reader = csv.reader(file)
        queries = []
        times = []
        for row in reader:
            queries.append(row[0])
            times.append(float(row[1]))

    # Create a line graph
    plt.plot(queries, times, marker='o', linestyle='-', color='blue')
    plt.xlabel('DNS Queries')
    plt.ylabel('Time Taken (ms)')
    plt.title('DNS Query Response Times')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Display the graph
    plt.show()

if __name__ == "__main__":
    plot_dns_queries()
