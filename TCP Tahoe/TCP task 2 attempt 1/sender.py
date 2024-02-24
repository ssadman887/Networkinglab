import socket
import time
import os

SOURCE_PORT =  8500

packet_queue = {}

def packet_decode(packet):
    """Decode the packet header and payload."""
    transport_header = packet[:30].decode('utf-8')
    payload = packet[30:]

    source_port = int(transport_header[:4])
    destination_port = int(transport_header[4:8])
    seq = int(transport_header[8:14])
    ack = int(transport_header[14:20])
    flag = int(transport_header[20:21])
    window = int(transport_header[21:26])
    payloadlen = int(transport_header[26:30])

    return source_port, destination_port, seq, ack, flag, window, payloadlen, payload

def packet_encode(seq, ack, window, flag, payloadlen, payload, destination_port):
    """Encode the packet header and payload."""
    seq = int(seq)
    ack = int(ack)
    window = int(window)
    transport_header = f'{SOURCE_PORT:04d}{destination_port:04d}{seq:06d}{ack:06d}{flag:01d}{window:05}{payloadlen:04d}'.encode('utf-8')[:30].ljust(30)
    
    packet = transport_header + payload
    return packet

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', SOURCE_PORT))
server_socket.listen(1)

print('Server is listening for incoming connections')

client_socket, address = server_socket.accept()
destination_port = address[1]
client_socket.settimeout(5)

print(f'Accepted connection from {address}')

# Open file to be sent
file = open('file_to_send.txt', 'rb')
file_size = os.path.getsize('file_to_send.txt')

# Open CSV files for RTT measurements
file1 = open('samplertt.csv', 'w')
f2 = open('estimatedrtt.csv', 'w')
file1.write("no,sampleRTT\n")
f2.write("no,estimatedRTT\n")

sequence_number =  0
last_ack =  0    
dup_count =  0
ack_number =  0
starting_time = time.time()
alpha =  0.125
beta =  0.25  
prevestimatedRTT =  0
prevdevRTT =  0

def get_estimated_rtt(sample_rtt, prev_estimated_rtt):
    """Calculate the estimated RTT."""
    estimated_rtt = (1 - alpha) * prev_estimated_rtt + alpha * sample_rtt
    return estimated_rtt

def get_dev_rtt(sample_rtt, estimated_rtt, prev_dev_rtt):
    """Calculate the deviation of RTT."""
    dev_rtt = (1 - beta) * prev_dev_rtt + beta * abs(sample_rtt - estimated_rtt)
    return dev_rtt

def get_timeout(estimated_rtt, dev_rtt):
    """Calculate the timeout value."""
    return estimated_rtt +  4 * dev_rtt

packet = client_socket.recv(1500)
source_port, destination_port, seq, ack, flag, window, payloadlen, payload = packet_decode(packet)
last_ack = ack
i =  1

# Initialize prev_estimated_rtt before the loop
prev_estimated_rtt =  0
prev_dev_rtt=0
while True:
    stime = time.time()
    if sequence_number + window == last_ack:
        payload = file.read(window)
        if not payload:
            break
        payload_size = len(payload)
        print("Size: ", payload_size)
        
        sequence_number += payload_size
        packet_queue[sequence_number] = payload
        packet = packet_encode(sequence_number, ack_number, window,  0, payload_size, payload, destination_port)

        client_socket.send(packet)
        print(f'Sent packet {sequence_number}')

    # Wait for acknowledgment from client
    try:
        acknowledgment = client_socket.recv(1500)
    except socket.timeout:
        print('No acknowledgment received within  5 seconds')
        break
    if acknowledgment:
        acknowledgment_source, acknowledgment_destination, acknowledgment_sequence_number, acknowledgment_ack_number, ack_flag, acknowledgment_window, acknowledgment_payloadlen, acknowledgment_payload = packet_decode(acknowledgment)
    
        if acknowledgment_ack_number == sequence_number + acknowledgment_window:
            print(f'Received acknowledgment for packet {sequence_number}')
            packet_queue.pop(sequence_number)
            window = acknowledgment_window
            last_ack = acknowledgment_ack_number
            dup_count =  0
        elif dup_count ==  3:
            payload = packet_queue[acknowledgment_ack_number]
            packet = packet_encode(acknowledgment_ack_number, ack_number, window,  0, len(payload), payload, destination_port)
            client_socket.send(packet)
            print(f'Fast retransmitted {acknowledgment_ack_number}')
            window = acknowledgment_window
            dup_count =  0
        elif acknowledgment_ack_number == last_ack:
            print(f'Received duplicate acknowledgment for packet {acknowledgment_ack_number}')
            dup_count +=  1
            payload = packet_queue[acknowledgment_ack_number]
            packet = packet_encode(acknowledgment_ack_number, ack_number, window,  0, len(payload), payload, destination_port)
            client_socket.send(packet)
            print(f'Retransmitted {acknowledgment_ack_number}')
        else:
            expected_ack = acknowledgment_ack_number - window
            print(f'Received acknowledgment for packet {acknowledgment_ack_number}, but expected {sequence_number}')
            payload = packet_queue[acknowledgment_ack_number]
            packet = packet_encode(acknowledgment_ack_number, ack_number, window,  0, len(payload), payload, destination_port)
            client_socket.send(packet)
            print(f'Retransmitted {acknowledgment_ack_number}')
            window = acknowledgment_window
            last_ack = acknowledgment_ack_number
    elif payload_size < window:
        print("File sent")
        break
    else:
        print('Did not receive acknowledgment')
    etime = time.time()
    sample_rtt = etime - stime
    file1.write(f'{i},{round(sample_rtt *  1000,  4)}\n')
    estimated_rtt = get_estimated_rtt(sample_rtt, prev_estimated_rtt)
    f2.write(f'{i},{round(estimated_rtt *  1000,  4)}\n')
    dev_rtt = get_dev_rtt(sample_rtt, estimated_rtt, prev_dev_rtt)
    timeout = get_timeout(estimated_rtt, dev_rtt)
    prev_estimated_rtt = estimated_rtt
    prev_dev_rtt = dev_rtt
    print("Sample RTT: ", round(sample_rtt *  1000,  4), "ms")
    print("Estimated RTT: ", round(estimated_rtt *  1000,  4), "ms")
    print("Dev RTT: ", round(dev_rtt *  1000,  4), "ms")
    print("Timeout: ", round(timeout *  1000,  4), "ms")
    client_socket.settimeout(timeout)
    i +=  1

# Close file
file.close()

print(f'Throughput: {(file_size / (time.time() - starting_time)) /  1000.0} B/s')
    
# Close sockets
client_socket.close()
server_socket.close()
print('Done')
