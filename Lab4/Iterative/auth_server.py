import socket,time,struct

IP = 'localhost'
AUTH_PORT = 8003
BUFFER_SIZE = 1024
FORMAT = "utf-8"

auth_records = {
    'cse.du.ac.bd': '192.0.2.3',
    'google.com': '142.250.193.110',
    'ns1.cse.du.ac.bd':'192.0.2.1',
    'ns2.cse.du.ac.bd':'192.0.2.2',
    'mail.cse.du.ac.bd':'192.0.2.4'
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
    id , flag, q, a, auth_rr, add_rr, question, answer = decode_dns_query(data)
    print(f"Authoritative Server received query: {question} from {addr}")

    query = question

    if query in auth_records:
        print(f"Authoritative Server sending response: {auth_records[query]} to {addr}")
        server.sendto(encode_dns_query(query,auth_records[query],1), addr)
    else:
        print(f"Sending response: Not Found to {addr}")
        server.sendto(encode_dns_query(query,"Not Found",1),addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, AUTH_PORT))
    print(f"Authoritative Server listening on {IP}:{AUTH_PORT}")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()