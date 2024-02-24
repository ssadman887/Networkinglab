import socket
import time
import csv
# Configuration
IP = 'localhost'
PORT =  8000  # Assuming this is your local DNS server port
BUFFER_SIZE =  1024
FORMAT = 'utf-8'

def send_dns_query(query):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Encode the query
    query = query.encode(FORMAT)
    
    # Send the query to the server
    client_socket.sendto(query, (IP, PORT))
    
    # Receive the response
    response, _ = client_socket.recvfrom(BUFFER_SIZE)
    
    # Decode and print the response
    print(f"Received response: {response.decode(FORMAT)}")


def write_to_csv(query, time_taken):
    # Open the CSV file in append mode
    with open('dns_queries.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # Write the query and time taken
        writer.writerow([query, time_taken])

if __name__ == "__main__":
    while True:
        # Take query input from the keyboard
        query = input("Enter your DNS query: ")
        print(f"Sending query: {query}")
        starttime = time.time()
        send_dns_query(query)
        endtime = time.time()
        time_taken=((endtime-starttime)*1000)
        print(f"Time taken: {((endtime-starttime)*1000):.2f} milliseconds")
        
        
        write_to_csv(query, time_taken)
