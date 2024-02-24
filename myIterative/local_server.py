import socket
from dns_utils import encode_dns_query, decode_dns_query
from config import IP, LOCAL_PORT, ROOT_PORT, BUFFER_SIZE, FORMAT

def validate_ip(s):
    a = s.split('.')
    if len(a) !=  4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i <  0 or i >  255:
            return False
    return True

def handle_query(data, addr, server):
    query = data.decode(FORMAT)
    print(f"Local Server received query: {query} from {addr}")
    packed_data = encode_dns_query(query, "None",  0)
    server.sendto(packed_data, (IP, ROOT_PORT))
    response, _ = server.recvfrom(BUFFER_SIZE)
    id, flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(response)
    print(f"Local Server received response: {answer}")
    i =  0
    while i <  3:
        if validate_ip(answer):
            server.sendto(answer.encode(FORMAT), addr)
            print(f"IP address sent to {addr}")
            break
        elif i ==  2:
            print("Local Server sending response: Not Found")
            server.sendto(answer.encode(FORMAT), addr)
            break
        else:
            next_server_port = int(answer)
            server.sendto(encode_dns_query(query, "None",  0), (IP, next_server_port))
            response, _ = server.recvfrom(BUFFER_SIZE)
            id, flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(response)
            print(f"Local Server received response: {answer} from {next_server_port}")
        i +=  1

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, LOCAL_PORT))
    print(f"Local Server listening on {IP}:{LOCAL_PORT}")
    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()
