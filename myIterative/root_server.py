import socket
from dns_utils import encode_dns_query, decode_dns_query
from config import *

def handle_query(data, addr, server):
    id, flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(data)
    query = question.split('.')[-1]
    print(f"Root Server received query: {query}")
    if query in root_records:
        print(f"Root Server sending response: {root_records[query]} to {addr}")
        server.sendto(encode_dns_query(question, str(root_records[query]),  1), addr)
    else:
        print(f"Record not found redirecting to TLD Server {TLD_PORT}")
        server.sendto(encode_dns_query(question, str(TLD_PORT),  1), addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, ROOT_PORT))
    print(f"Root Server listening on {IP}:{ROOT_PORT}")
    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()
