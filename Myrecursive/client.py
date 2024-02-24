import socket
import time
import csv
import os

IP = 'localhost'
LOCAL_PORT =   8000
BUFFER_SIZE =   1024
FORMAT = "utf-8"

def send_query(query):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(query.encode(FORMAT), (IP, LOCAL_PORT))

    response, addr = client.recvfrom(BUFFER_SIZE)
        
    print(f"IP address from server: {response.decode(FORMAT)}")

def write_to_csv(query, time_taken):
    file_path = 'query_times.csv'
    header = ['Query', 'Time Taken (ms)']
    # Check if the file exists and if it's empty
    if not os.path.exists(file_path) or os.path.getsize(file_path) ==  0:
        # Write the header row
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    # Append the query and time taken
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([query, time_taken])

if __name__ == "__main__":
    while True:
        query = input("Enter your DNS query: ")
        starttime = time.time()
        send_query(query)
        endtime = time.time()
        time_taken = ((endtime-starttime)*1000)
        print(f"Time taken: {time_taken:.2f} milliseconds")
        write_to_csv(query, time_taken)
