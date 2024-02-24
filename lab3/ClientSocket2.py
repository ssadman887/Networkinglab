import socket

host = 'localhost'
port = 1744

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

operation = input("Do you want to download or upload a file? (download/upload): ").strip().lower()
file_name = input("Enter the file name: ")

if operation == 'download':
    client_socket.send(f"download:{file_name}".encode())
    file_data = client_socket.recv(1024)
    if file_data == b"File not found":
        print("File not found on the server.")
    else:
        with open(file_name, 'wb') as file:
            file.write(file_data)
        print(f"File {file_name} downloaded successfully.")
elif operation == 'upload':
    try:
        with open(file_name, 'rb') as file:
            file_data = file.read()
        client_socket.send(f"upload:{file_name}".encode())
        client_socket.send(file_data)
        print(f"File {file_name} uploaded successfully.")
    except FileNotFoundError:
        print("File not found.")
else:
    print("Invalid operation.")

client_socket.close()