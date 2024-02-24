import socket, time, struct

AUTH_IP = 'localhost'
AUTH_PORT =   8003
BUFFER_SIZE =   1024
ENCODING_FORMAT = "utf-8"

auth_dns_records = {
    'cse.du.ac.bd': '192.0.2.3',
    'google.com': '142.250.193.110',
    'ns1.cse.du.ac.bd':'192.0.2.1',
    'ns2.cse.du.ac.bd':'192.0.2.2',
    'mail.cse.du.ac.bd':'192.0.2.4'
}

def pack_dns_query(question, answer, flag):
    query_id = int(time.time())
    query_count =   1
    answer_count =   1
    auth_rr =   0
    add_rr =   0
    encoded_question = question.encode(ENCODING_FORMAT)
    encoded_answer = answer.encode(ENCODING_FORMAT)
    packed_data = struct.pack(f'!7i{len(encoded_question)}s{len(encoded_answer)}s', query_id, flag, query_count, answer_count, auth_rr, add_rr, len(encoded_question), encoded_question, encoded_answer)
    return packed_data

def unpack_dns_query(data):
    query_id, flag, query_count, answer_count, auth_rr, add_rr, question_length = struct.unpack('!7i', data[:28])
    question = data[28:28+question_length].decode(ENCODING_FORMAT)
    answer = data[28+question_length:].decode(ENCODING_FORMAT)
    return query_id, flag, query_count, answer_count, auth_rr, add_rr, question, answer

def process_query(data, client_address, server_socket):
    query_id, flag, query_count, answer_count, auth_rr, add_rr, question, answer = unpack_dns_query(data)
    query = question
    print(f"Authoritative Server received query: {query} from {client_address}")

    if query in auth_dns_records:
        server_socket.sendto(pack_dns_query(query, auth_dns_records[query],   1), client_address)
        print(f"Authoritative Server sent response: {auth_dns_records[query]} to TLD Server {client_address}")
    else:
        server_socket.sendto(pack_dns_query(query, "Not Found",   1), client_address)
        print(f"Authoritative Server sent response: Not Found to TLD Server {client_address}")

def start_auth_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((AUTH_IP, AUTH_PORT))
    print(f"Authoritative Server listening on {AUTH_IP}:{AUTH_PORT}")

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        process_query(data, addr, server_socket)

if __name__ == "__main__":
    start_auth_server()
