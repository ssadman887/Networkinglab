# import socket
# import uuid
# import time
# import random
# import matplotlib.pyplot as plt

# def generate_transaction_id():
#     """Generate a unique transaction ID."""
#     return str(uuid.uuid4())

# def simulate_message_with_error_rate(client_socket, error_rate, total_messages=100):
#     successful_time = 0
#     for _ in range(total_messages):
#         start_time = time.time()
#         # Simulate sending a message (e.g., balance query)
#         card_number = "1234567890"
#         transaction_id = generate_transaction_id()
#         message = f"BALANCE_QUERY:{card_number}:{transaction_id}"

#         # Simulate decision to either process or error based on error rate
#         if random.random() >= error_rate:
#             # Simulate sending and receiving a response (excluding actual send/receive for demonstration)
#             end_time = time.time()
#             successful_time += (end_time - start_time)*100000
#         else:
#             # Simulated error, do not add to successful_time
#             continue
#     return successful_time

# error_rates = [0.1, 0.2, 0.3, 0.4, 0.5]
# times_taken = []

# for error_rate in error_rates:
#     time_taken = simulate_message_with_error_rate(None, error_rate)  # Passing None for client_socket to simulate
#     times_taken.append(time_taken)

# # Plotting the graph
# plt.plot(error_rates, times_taken, marker='o')
# plt.title('Time Taken vs. Error Rate')
# plt.xlabel('Error Rate')
# plt.ylabel('Time Taken (s)')
# plt.grid(True)
# plt.show()

import socket
import uuid
import time
import random
import matplotlib.pyplot as plt

def generate_transaction_id():
    """Generate a unique transaction ID."""
    return str(uuid.uuid4())

def send_request_with_simulation(client_socket, request, simulate_error):
    """Send request to the server, simulate error based on flag."""
    start_time = time.time()
    if not simulate_error:
        client_socket.send(request.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        end_time = time.time()
        return end_time - start_time, response
    return 0, "SIMULATED_ERROR"

def simulate_operations_with_error_rate(host, port, error_rate, total_messages=100):
    successful_time = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        for _ in range(total_messages):
            transaction_id = generate_transaction_id()
            message = f"BALANCE_QUERY:1234567890:{transaction_id}"
            simulate_error = random.random() < error_rate
            time_taken, response = send_request_with_simulation(client_socket, message, simulate_error)
            successful_time += time_taken
    return successful_time

# Connect to the actual server and measure time excluding errors
host = 'localhost'
port = 12345
error_rates = [0.1, 0.2, 0.3, 0.4, 0.5]
times_taken = []

for error_rate in error_rates:
    time_taken = simulate_operations_with_error_rate(host, port, error_rate)
    times_taken.append(time_taken)

# Plotting the results
plt.plot(error_rates, times_taken, marker='o')
plt.title('Time Taken vs. Error Rate')
plt.xlabel('Error Rate')
plt.ylabel('Time Taken (seconds)')
plt.grid(True)
plt.show()
