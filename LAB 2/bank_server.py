import socket
import threading

# Simulate a simple database for accounts and transaction history
accounts = {
    "1234567890": {"password": "password123", "balance": 1000}
}
transaction_history = {}

def handle_client_connection(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            response = process_request(data)
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def process_request(request):
    parts = request.split(':')
    request_type, card_number = parts[0], parts[1]
    transaction_id = parts[-1]

    if transaction_id in transaction_history:
        return transaction_history[transaction_id]

    if request_type == "AUTH":
        response = authenticate_user(card_number, parts[2], transaction_id)
    elif request_type == "BALANCE_QUERY":
        response = get_balance(card_number, transaction_id)
    elif request_type == "WITHDRAW":
        response = process_withdrawal(card_number, float(parts[2]), transaction_id)
    elif request_type == "DEPOSIT":
        response = process_deposit(card_number, float(parts[2]), transaction_id)
    else:
        response = "ERROR:Invalid request"

    transaction_history[transaction_id] = response
    return response

def authenticate_user(card_number, password, transaction_id):
    account = accounts.get(card_number)
    if account and account['password'] == password:
        return f"AUTH_RESPONSE:SUCCESS:Authenticated:{transaction_id}"
    return f"AUTH_RESPONSE:FAILURE:Authentication Failed:{transaction_id}"

def get_balance(card_number, transaction_id):
    account = accounts.get(card_number)
    if account:
        return f"BALANCE_RESPONSE:SUCCESS:{account['balance']}:{transaction_id}"
    return f"BALANCE_RESPONSE:FAILURE:Account not found:{transaction_id}"

# def process_withdrawal(card_number, amount, transaction_id):
#     account = accounts.get(card_number)
#     if account:
#         if account['balance'] >= amount:
#             account['balance'] -= amount
#             return f"WITHDRAW_RESPONSE:SUCCESS:Withdrawal Complete:{transaction_id} "
#         return f"WITHDRAW_RESPONSE:FAILURE:Insufficient Funds:{transaction_id}"
#     return f"WITHDRAW_RESPONSE:FAILURE:Account not found:{transaction_id}"

# def process_deposit(card_number, amount, transaction_id):
#     account = accounts.get(card_number)
#     if account:
#         account['balance'] += amount
#         return f"DEPOSIT_RESPONSE:SUCCESS:Deposit Complete:{transaction_id} "
#     return f"DEPOSIT_RESPONSE:FAILURE:Account not found:{transaction_id}"

def process_withdrawal(card_number, amount, transaction_id):
    account = accounts.get(card_number)
    if account:
        if account['balance'] >= amount:
            account['balance'] -= amount
            return f"WITHDRAW_RESPONSE:SUCCESS:Withdrawal Complete. New Balance: {account['balance']}. Transaction ID: {transaction_id}"
        return f"WITHDRAW_RESPONSE:FAILURE:Insufficient Funds. Current Balance: {account['balance']}. Transaction ID: {transaction_id}"
    return f"WITHDRAW_RESPONSE:FAILURE:Account not found. Transaction ID: {transaction_id}"

def process_deposit(card_number, amount, transaction_id):
    account = accounts.get(card_number)
    if account:
        account['balance'] += amount
        return f"DEPOSIT_RESPONSE:SUCCESS:Deposit Complete. New Balance: {account['balance']}. Transaction ID: {transaction_id}"
    return f"DEPOSIT_RESPONSE:FAILURE:Account not found. Transaction ID: {transaction_id}"


def main():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on {}:{}".format(host, port))

    try:
        while True:
            client_sock, _ = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(client_sock,))
            client_thread.start()
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
