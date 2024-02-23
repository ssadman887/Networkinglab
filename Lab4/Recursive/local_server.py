import socket
import struct
import time
import threading

IP = 'localhost'
LOCAL_PORT = 8000
ROOT_PORT = 8001
BUFFER_SIZE = 1024
FORMAT = "utf-8"
TTL = 3

local_records = {
}

def is_expired(record, ttl_value):
    start = time.time()
    while True:
        end = time.time()
        if end - start > ttl_value:
            local_records.pop(record)
            print(f"Record {record} expired after {ttl_value} seconds. Removed from Local records.")
            break

def encode_dns_query(question,answer,flag):
    id = int(time.time())
    q = 1
    a = 1
    auth_rr = 0
    add_rr = 0
    question = question.encode(FORMAT)
    answer = answer.encode(FORMAT)
    packed_data = struct.pack(f'!7i{len(question)}s{len(answer)}s', id, flag, q, a, auth_rr, add_rr, len(question), question, answer)
    return packed_data

def decode_dns_query(data):
    id, flag, q, a, auth_rr, add_rr, len_question = struct.unpack('!7i', data[:28])
    question = data[28:28+len_question].decode(FORMAT)
    answer = data[28+len_question:].decode(FORMAT)
    return id, flag, q, a, auth_rr, add_rr, question, answer


def handle_query(data, addr, server):

    query = data.decode(FORMAT)
    
    print(f"Local Server received query: {query} from {addr}")

    if query in local_records:
        print(f"IP address found in local records")
        server.sendto(local_records[query].encode(FORMAT), addr)
        print(f"IP address sent to {addr}")
        return

    packed_data = encode_dns_query(query, "None",0)

    # Send to Root Server
    print(f"Local Server sending query to Root Server {ROOT_PORT}")
    server.sendto(packed_data, (IP, ROOT_PORT))

    response, server_addr = server.recvfrom(BUFFER_SIZE)
    id, flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(response)

    print("Local Server received response from Root Server")
    if validate_ip(answer):
        local_records.update({query: answer})
        threading.Thread(target=is_expired, args=(query, TTL)).start()
        print(f"IP address added to local records")
        server.sendto(answer.encode(FORMAT), addr)
        print(f"IP address sent to {addr}")
        
    else:
        server.sendto(answer.encode(FORMAT), addr)
        print(f"IP address Not Found")
    
    

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, LOCAL_PORT))
    print(f"Local Server listening on {IP}:{LOCAL_PORT}")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()