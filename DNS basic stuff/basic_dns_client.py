import socket
import struct

ADDR = ('localhost', 9000) # can change
SIZE = 1024
FORMAT = 'utf-8'

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP socket
    
    while True:
        try:
            domain = input("Enter a domain to send to the server (or 'exit' to quit): ")
            if domain.lower() == 'exit':
                break
            
            while True:
                query_type = input("Enter a type to send to the server: ")

                final_msg = f"{domain} {query_type}" #get the domain and type binded
                client.sendto(final_msg.encode(FORMAT), ADDR) #send to server

                msg, addr = client.recvfrom(SIZE) #receive the response from the server
                id, flag, q, a, auth_rr, add_rr, question_len = struct.unpack('!7i', msg[:28]) #unpack stuff

                question = msg[28:28+question_len].decode(FORMAT)
                answer = msg[28+question_len:].decode(FORMAT)

                print("\nAfter decoding:")
                print(f"id: {id}")
                print(f"Question: {question}")

                if answer == "NOT FOUND":
                    print("Type not found. Please try again.")
                else:
                    print(f"Answer: {answer}")
                    print(f"IP Address: {answer}")
                    break  # Exit the loop if answer is found

        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
