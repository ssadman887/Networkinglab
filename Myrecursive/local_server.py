import socket
import struct
import time
import threading

LOCAL_IP = 'localhost'
LOCAL_PORT =  8000
ROOT_SERVER_PORT =  8001
BUFFER_SIZE =  1024
ENCODING_FORMAT = "utf-8"
TTL_VALUE =  3

local_dns_records = {}

def check_record_expiry(record, ttl):
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > ttl:
            local_dns_records.pop(record)
            print(f"Record {record} expired after {ttl} seconds. Removed from Local records.")
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
    query = data.decode(ENCODING_FORMAT)
    print(f"Local Server received query: {query} from {client_address}")

    if query in local_dns_records:
        print(f"IP address found in local records")
        server_socket.sendto(local_dns_records[query].encode(ENCODING_FORMAT), client_address)
        print(f"IP address sent to {client_address}")
        return

    packed_query = pack_dns_query(query, "None",  0)
    print(f"Local Server sending query to Root Server {ROOT_SERVER_PORT}")
    server_socket.sendto(packed_query, (LOCAL_IP, ROOT_SERVER_PORT))

    response, server_address = server_socket.recvfrom(BUFFER_SIZE)
    query_id, flag, query_count, answer_count, auth_rr, add_rr, question, answer = unpack_dns_query(response)

    print("Local Server received response from Root Server")
    if validate_ip_address(answer):
        local_dns_records.update({query: answer})
        threading.Thread(target=check_record_expiry, args=(query, TTL_VALUE)).start()
        print(f"IP address added to local records")
        server_socket.sendto(answer.encode(ENCODING_FORMAT), client_address)
        print(f"IP address sent to {client_address}")
    else:
        server_socket.sendto(answer.encode(ENCODING_FORMAT), client_address)
        print(f"IP address Not Found")

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

def start_local_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((LOCAL_IP, LOCAL_PORT))
    print(f"Local Server listening on {LOCAL_IP}:{LOCAL_PORT}")

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        process_query(data, addr, server_socket)

if __name__ == "__main__":
    start_local_server()
