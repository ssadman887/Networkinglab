import socket
import uuid

def generate_transaction_id():
    """Generate a unique transaction ID."""
    return str(uuid.uuid4())

def send_request(client_socket, request):
    """Send request to the server and wait for response."""
    client_socket.send(request.encode('utf-8'))
    return client_socket.recv(1024).decode('utf-8')

def main():
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to the bank server.")

        card_number = input("Enter your card number: ")
        password = input("Enter your password: ")
        transaction_id = generate_transaction_id()
        response = send_request(client_socket, f"AUTH:{card_number}:{password}:{transaction_id}")
        print(response)

        if "SUCCESS" in response:
            while True:
                operation = input("Enter operation (balance/withdraw/deposit/exit): ").lower()
                transaction_id = generate_transaction_id()

                if operation == "balance":
                    response = send_request(client_socket, f"BALANCE_QUERY:{card_number}:{transaction_id}")
                elif operation == "withdraw":
                    amount = input("Enter amount to withdraw: ")
                    response = send_request(client_socket, f"WITHDRAW:{card_number}:{amount}:{transaction_id}")
                elif operation == "deposit":
                    amount = input("Enter amount to deposit: ")
                    response = send_request(client_socket, f"DEPOSIT:{card_number}:{amount}:{transaction_id}")
                elif operation == "exit":
                    break
                else:
                    print("Invalid operation. Please try again.")
                    continue

                print(response)
        else:
            print("Authentication failed.")

if __name__ == '__main__':
    main()
