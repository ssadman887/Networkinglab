import socket
import time
import struct

IP = 'localhost'
ROOT_PORT = 8001
TLD_PORT = 8002
BUFFER_SIZE = 1024
FORMAT = "utf-8"

root_records = {
    'bd': TLD_PORT,
    'com': TLD_PORT,
}

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
    id, flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(data)
    query = question
    query = query.split('.')[-1]
    print(f"Root Server received query: {query}")

    if query in root_records:
        print(f"Root Server sending response: {root_records[query]} to {addr}")
        server.sendto(encode_dns_query(question,str(root_records[query]),1), addr)
    else:
        print(f"Record not found redirecting to TLD Server {TLD_PORT}")
        server.sendto(encode_dns_query(question,str(TLD_PORT),1), addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, ROOT_PORT))
    print(f"Root Server listening on {IP}:{ROOT_PORT}")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()