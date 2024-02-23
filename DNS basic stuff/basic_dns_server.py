import socket
import struct
import threading
import time

IP = '' #the server will listen for incoming connections on all available network interfaces
PORT = 9000
ADDR = (IP, PORT)
VOLUME = 1024 #buffer size
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def handle_client(data, addr, server):
    print(f"[RECEIVED MESSAGE] {data} from {addr}.")
    question = data.split()[0].encode('utf-8') #extract the domain name
    id = int(time.time()) #the current time (in seconds since the epoch) to an integer.
    
    
    flag = q = a = auth_rr = add_rr = 0

    records = {} # store DNS records read from the file
    with open('dns_records.txt', 'r') as file:
        for line in file.readlines()[1:]: #skip meta data
            name, value, record_type, ttl = line.split() #get each line split it
            records.setdefault(name, []).append((value, record_type))

    answer = None
    query_type = data.split()[1] #we'll take type as query

    for name, value_type_pairs in records.items(): #key value diye record point kora dict e
        for value, record_type in value_type_pairs:
            if name == question.decode('utf-8'): #domain nam match korle
                if record_type == query_type or (query_type == 'AAAA' and record_type == 'A'): #type match korle
                    print('IP address found in the file')
                    answer = value #answer pathao
                    break

    if answer:# got answer? yes? then go
        for name, value_type_pairs in records.items():
            '''this condition checks if the current domain name (name) matches the answer previously identified. 
            This indicates that the answer corresponds to a CNAME (canonical name) record, and further
            resolution is needed to obtain the final IP address.'''
            if name == answer:
                for value, record_type in value_type_pairs:
                    if record_type == 'A':
                        print('IP address found in the file')
                        answer = value
                        break
                break

    if not answer:
        print('IP address not found in the file')
        answer = "NOT FOUND"

    answer = answer.encode('utf-8')
    packed_data = struct.pack(f'!7i{len(question)}s{len(answer)}s', id, flag, q, a, auth_rr, add_rr, len(question), question, answer)
    server.sendto(packed_data, addr)

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #user datagram protocol
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        data, addr = server.recvfrom(VOLUME)
        data = data.decode(FORMAT)
        #call the handle_client function with the received data, client address, and server socket as arguments.
        thread = threading.Thread(target=handle_client, args=(data, addr, server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
