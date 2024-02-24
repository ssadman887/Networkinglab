import socket
import threading

def handle_client_connection(client_socket):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break  # No data, client closed connection

            # Split the data to command and message/number
            command, message = data.split(':', 1)

            if command == 'text':
                # Convert text to lowercase
                response = message.lower()
            elif command == 'check':
                number, operation = message.split(',')
                number = int(number)
                if operation == 'prime':
                    response = str(is_prime(number))
                elif operation == 'palindrome':
                    response = str(is_palindrome(number))
                else:
                    response = 'Invalid operation'
            else:
                response = 'Invalid command'

            client_socket.send(response.encode('utf-8'))
    finally:
        client_socket.close()

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_palindrome(n):
    """Check if a number is a palindrome."""
    return str(n) == str(n)[::-1]

def main():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Server listening on {host}:{port}...')

    try:
        while True:
            client_sock, address = server_socket.accept()
            print(f'Accepted connection from {address}')
            client_thread = threading.Thread(target=handle_client_connection, args=(client_sock,))
            client_thread.start()
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
