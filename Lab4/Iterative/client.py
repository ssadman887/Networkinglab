import socket
import time
IP = 'localhost'
LOCAL_PORT = 8000
BUFFER_SIZE = 1024
FORMAT = "utf-8"

def send_query(query):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(query.encode(FORMAT), (IP, LOCAL_PORT))

    response, addr = client.recvfrom(BUFFER_SIZE)
        
    print(f"IP address from server: {response.decode(FORMAT)}")


if __name__ == "__main__":
    while True:
        query = input("Enter your DNS query: ")
        starttime = time.time()
        send_query(query)
        endtime = time.time()
        print(f"Time taken: {((endtime-starttime)*1000):.2f} milliseconds")
        