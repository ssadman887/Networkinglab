import socket

def send_text(text):
    return f"text:{text}"

def send_number_check(number, operation):
    return f"check:{number},{operation}"

def main():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to the server. Type 'exit' to quit.")

        while True:
            operation = input("Enter operation (text/check): ").strip()
            if operation.lower() == 'exit':
                break

            if operation == 'text':
                text = input("Enter text to convert: ")
                message = send_text(text)
            elif operation == 'check':
                number = input("Enter a number: ")
                op_name = input("Enter operation name (prime/palindrome): ")
                message = send_number_check(number, op_name)
            else:
                print("Invalid operation. Please try again.")
                continue

            client_socket.sendall(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Response from server: {response}")

if __name__ == '__main__':
    main()
