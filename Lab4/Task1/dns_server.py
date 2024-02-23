import os
import socket
import threading
import struct
import time

IP = ''
PORT = 9000
ADDR = (IP, PORT)
VOLUME = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
dic={}

def handle_client(data, addr, server):
    print(f"[RECEIVED MESSAGE] {data} from {addr}.")
    question = data
    data = data.split()
    print(data[0])
    print(data[1])

    id = int(time.time())
    flag = 0
    q = 1
    a = 1
    auth_rr = 0
    add_rr = 0
    question = question.encode(FORMAT)
    answer = None

    file = open('dns_records.txt', 'r')


    i=0
    name =[]
    value = []
    type = []
    ttl = []
    for line in file:
        if(i==0):
            i+=1
            continue
        line = line.split()
        name.append(line[0])
        value.append(line[1])
        type.append(line[2])
        ttl.append(line[3]) 

    response = None

    if data[1] == 'A':
        for i in range(0, len(name)):
            if name[i] == data[0] and type[i] == 'A':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
    elif data[1] == 'AAAA': 
        for  i in range(0,len(name)):
            if name[i] == data[0] and type[i] == 'AAAA':
                print('IP address found in the file')
                answer = name[i]
                print(answer)
                break
        for i in range(0,len(name)):
            if name[i] == answer and type[i] == 'A':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
    elif data[1] == 'NS':
        for  i in range(0,len(name)):
            if name[i] == data[0] and type[i] == 'NS':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
        for i in range(0,len(name)):
            if name[i] == answer and type[i] == 'A':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
    elif data[1] == 'MX':
        answer =None
        for  i in range(0,len(name)):
            if name[i] == data[0] and type[i] == 'MX':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
        for i in range(0,len(name)):
            if name[i] == answer and type[i] == 'A':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
    elif data[1] == 'CNAME':
        answer =None
        for  i in range(0,len(name)):
            if name[i] == data[0] and type[i] == 'CNAME':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
        for i in range(0,len(name)):
            if name[i] == answer and type[i] == 'A':
                print('IP address found in the file')
                answer = value[i]
                print(answer)
                break
        
    print(answer)
    answer = answer.encode(FORMAT)
    packed_data = struct.pack(f'!7i{len(question)}s{len(answer)}s', id, flag, q, a, auth_rr, add_rr, len(question), question, answer)
    
    server.sendto(packed_data, addr)
    



            

def main():
   
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        data, addr = server.recvfrom(VOLUME)
        data = data.decode(FORMAT)
        thread = threading.Thread(target=handle_client, args=(data, addr,server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()