import socket
import time
import struct
import threading

ROOT_IP = 'localhost'
ROOT_PORT =  8001
TLD_SERVER_PORT =  8002
BUFFER_SIZE =  1024
ENCODING_FORMAT = "utf-8"
TTL_VALUE =  6
root_dns_records = {
    'bd': TLD_SERVER_PORT,
    'com': TLD_SERVER_PORT,
}

def check_record_expiry(record, ttl):
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > ttl:
            root_dns_records.pop(record)
            print(f"Record {record} expired after {ttl} seconds. Removed from Root records.")
            break

def pack_dns_query(question, answer, flag):
    query_id = int(time.time())
    query_count =  1
    answer_count =  1
    auth_rr =  0
    add_rr =  0
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
    print(f"Root Server received query: {query}")

    if query in root_dns_records:
        print("Record found in root records. Sending response to Local Server")
        server_socket.sendto(pack_dns_query(question, str(root_dns_records[query]),  1), client_address)
    else:
        print(f"Record not found redirecting to TLD Server {TLD_SERVER_PORT}")
        server_socket.sendto(pack_dns_query(question, str(TLD_SERVER_PORT),  0), (ROOT_IP, TLD_SERVER_PORT))

        response, _ = server_socket.recvfrom(BUFFER_SIZE)
        print(f"Root Server received response from TLD Server {TLD_SERVER_PORT}")

        query_id, flag, query_count, answer_count, auth_rr, add_rr, question, answer = unpack_dns_query(response)

        if validate_ip_address(answer):
            print("Record added to root records")
            root_dns_records.update({question: answer})
            threading.Thread(target=check_record_expiry, args=(question, TTL_VALUE)).start()
        server_socket.sendto(pack_dns_query(question, answer,  1), client_address)
        print(f"Root Server sent response to Local Server")

def validate_ip_address(s):
    parts = s.split('.')
    if len(parts) !=  4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        value = int(part)
        if value <  0 or value >  255:
            return False
    return True

def start_root_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ROOT_IP, ROOT_PORT))
    print(f"Root Server listening on {ROOT_IP}:{ROOT_PORT}")

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        process_query(data, addr, server_socket)

if __name__ == "__main__":
    start_root_server()
