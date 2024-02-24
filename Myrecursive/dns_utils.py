import socket
import struct
import time

FORMAT = "utf-8"

def encode_dns_query(question, answer, flag):
    id = int(time.time())
    q =  1
    a =  1
    auth_rr =  0
    add_rr =  0
    question = question.encode(FORMAT)
    answer = answer.encode(FORMAT)
    packed_data = struct.pack(f'!7i{len(question)}s{len(answer)}s', id, flag, q, a, auth_rr, add_rr, len(question), question, answer)
    return packed_data

def decode_dns_query(data):
    id, flag, q, a, auth_rr, add_rr, len_question = struct.unpack('!7i', data[:28])
    question = data[28:28+len_question].decode(FORMAT)
    answer = data[28+len_question:].decode(FORMAT)
    return id, flag, q, a, auth_rr, add_rr, question, answer

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
