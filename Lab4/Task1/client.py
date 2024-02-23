import socket
import struct

ADDR = ('localhost', 9000)
SIZE = 1024
FORMAT = 'utf-8'

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    domain = input("Enter a domain to send to the server: ")
    type = input("Enter a type to send to the server: ")
    final_msg = domain + ' ' + type
    client.sendto(final_msg.encode(FORMAT), ADDR)

    msg, addr = client.recvfrom(SIZE)
    # print('In bytes: ')
    # print(msg)

    # Unpack the first 7 integers
    id, flag, q, a, auth_rr, add_rr, question_len = struct.unpack('!7i', msg[:28])

    question = struct.unpack(f'!{question_len}s', msg[28:28+question_len])[0].decode(FORMAT)

    answer_start = 28 + question_len

    answer_len = len(msg) - answer_start
    answer = struct.unpack(f'!{answer_len}s', msg[answer_start:])[0].decode(FORMAT)
    
    print("After decoding:")
    print(f"id: {id}, flag: {flag}, q: {q}, a: {a}, auth_rr: {auth_rr}, add_rr: {add_rr}, question: {question}, answer: {answer}")
    print(f"IP Address: {answer}")

        

if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break