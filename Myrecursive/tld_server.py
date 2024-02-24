import socket, time, struct, threading

TLD_IP = 'localhost'
TLD_PORT =  8002
AUTH_SERVER_PORT =  8003
BUFFER_SIZE =  1024
ENCODING_FORMAT = "utf-8"
TTL_VALUE =  3
tld_dns_records = {}

def check_record_expiry(record, ttl):
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > ttl:
            tld_dns_records.pop(            record)
            print(f"Record {record} expired after {ttl} seconds. Removed from TLD records.")
            break

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
    print(f"TLD Server received query: {query}")

    if query in tld_dns_records:
        print("Record found in TLD records. Sending response to Root Server")
        server_socket.sendto(pack_dns_query(query, str(tld_dns_records[query]),   1), client_address)
    else:
        print(f"Record not found redirecting to Authoritative Server {AUTH_SERVER_PORT}")
        server_socket.sendto(pack_dns_query(query, str(AUTH_SERVER_PORT),   0), (TLD_IP, AUTH_SERVER_PORT))

        response, _ = server_socket.recvfrom(BUFFER_SIZE)
        print(f"TLD Server received response from Authoritative Server {AUTH_SERVER_PORT}")

        query_id, flag, query_count, answer_count, auth_rr, add_rr, question, answer = unpack_dns_query(response)

        if validate_ip_address(answer):
            print("Record added to TLD records")
            tld_dns_records.update({query: answer})
            threading.Thread(target=check_record_expiry, args=(query, TTL_VALUE)).start()
        server_socket.sendto(pack_dns_query(query, answer,   1), client_address)
        print(f"TLD Server sent response to Root Server")

def validate_ip_address(s):
    parts = s.split('.')
    if len(parts) !=   4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        value = int(part)
        if value <   0 or value >   255:
            return False
    return True

def start_tld_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((TLD_IP, TLD_PORT))
    print(f"TLD Server listening on {TLD_IP}:{TLD_PORT}")

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        process_query(data, addr, server_socket)

if __name__ == "__main__":
    start_tld_server()

