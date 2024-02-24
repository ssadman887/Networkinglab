import socket
from dns_utils import encode_dns_query, decode_dns_query
from config import IP, AUTH_PORT, BUFFER_SIZE, FORMAT, auth_records

def handle_query(data, addr, server):
    id, flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(data)
    query = question
    print(f"Authoritative Server received query: {query} from {addr}")
    if query in auth_records:
        print(f"Authoritative Server sending response: {auth_records[query]} to {addr}")
        server.sendto(encode_dns_query(question, auth_records[query],  1), addr)
    else:
        print(f"Sending response: Not Found to {addr}")
        server.sendto(encode_dns_query(question, "Not Found",  1), addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, AUTH_PORT))
    print(f"Authoritative Server listening on {IP}:{AUTH_PORT}")
    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()
