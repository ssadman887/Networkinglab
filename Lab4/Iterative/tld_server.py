import socket,time,struct

IP = 'localhost'
TLD_PORT = 8002
AUTH_PORT = 8003
BUFFER_SIZE = 1024
FORMAT = "utf-8"

tld_records = {
    'cse.du.ac.bd': AUTH_PORT,
    'google.com': AUTH_PORT,
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
    print(f"TLD Server received query: {question}")

    query = question

    if query in tld_records:
        print(f"TLD Server sending response: {tld_records[query]} to {addr}")
        server.sendto(encode_dns_query(query,str(tld_records[query]),1), addr)
    else:
        print(f"Record is not found redirecting to Authoritative Server {AUTH_PORT}")
        server.sendto(encode_dns_query(query,str(AUTH_PORT),1), addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, TLD_PORT))
    print(f"TLD Server listening on {IP}:{TLD_PORT}")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()