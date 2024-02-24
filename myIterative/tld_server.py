import socket
from dns_utils import encode_dns_query, decode_dns_query
from config import *

def handle_query(data, addr, server):
    id, flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(data)
    query = question
    print(f"TLD Server received query: {query}")
    if query in tld_records:
        print(f"TLD Server sending response: {tld_records[query]} to {addr}")
        server.sendto(encode_dns_query(query, str(tld_records[query]),  1), addr)
    else:
        print(f"Record is not found redirecting to Authoritative Server {AUTH_PORT}")
        server.sendto(encode_dns_query(query, str(AUTH_PORT),  1), addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, TLD_PORT))
    print(f"TLD Server listening on {IP}:{TLD_PORT}")
    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()
