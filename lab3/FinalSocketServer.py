import socket
import threading
import os

host = 'localhost'
port = 1744

def handle_client(client_socket, client_address):
    try:
        # Read the command (upload/download) from the client
        command = client_socket.recv(1024).decode()
        
        if command.startswith('download:'):
            file_name = command.split(':')[1]
            # Handle file download
            if os.path.isfile(file_name):
                with open(file_name, 'rb') as file:
                    client_socket.sendall(file.read())
                print(f"Sent {file_name} to {client_address}")
            else:
                client_socket.sendall(b"File not found")
        elif command.startswith('upload:'):
            file_name = command.split(':')[1]
            file_data = client_socket.recv(1024)
            with open(file_name, 'wb') as file:
                file.write(file_data)
            print(f"Received {file_name} from {client_address}")
        else:
            client_socket.sendall(b"Invalid command")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,client_address))
        client_handler.start()

start_server()