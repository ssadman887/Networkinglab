import socket
import time
import os

source_port = 8500

def packet_decode(packet):
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
    seq = int(seq)
    ack = int(ack)
    window = int(window)
    transport_header = f'{source_port:04d}{destination_port:04d}{seq:06d}{ack:06d}{flag:01d}{window:05}{payloadlen:04d}'.encode('utf-8')[:30].ljust(30)
    
    packet = transport_header + payload
    return packet

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8500))
server_socket.listen(1)

print('Server is listening for incoming connections')

client_socket, address = server_socket.accept()
destination_port = address[1]
client_socket.settimeout(5)

print(f'Accepted connection from {address}')

# Open file to be sent
file = open('file_to_send.txt', 'rb')

sequence_number = 0
ack_number=0
starting_time=time.time()
file_size= os.path.getsize('file_to_send.txt')

packet = client_socket.recv(1500)
source_port, destination_port, seq, ack, flag, window, payloadlen, payload = packet_decode(packet)

while True:
    payload = file.read(window)
    if not payload:
        break
    payload_size=len(payload)
    print("size: ",payload_size)
    
    sequence_number+=payload_size
    packet=packet_encode(sequence_number,ack_number,window,0,payload_size,payload,destination_port)

    # print(sequence_number,ack_number,window,0,payload_size)
    client_socket.send(packet)
    print(f'Sent packet {sequence_number}')

    # Wait for acknowledgment from client
    try:
        acknowledgment = client_socket.recv(1500)
    except socket.timeout:
        print('No acknowledgment received within 5 seconds')
        break
    if acknowledgment:
        acknowledgment_source,acknowledgment_destination,acknowledgment_sequence_number,acknowledgment_ack_number,aack_flag,acknowledgment_window,acknowledgment_payloadlen,acknowledgment_payload = packet_decode(acknowledgment)
    
        # print("acknowledgment:")
        # print(acknowledgment_sequence_number,acknowledgment_ack_number,acknowledgment_window,acknowledgment_flag,acknowledgment_payloadlen,acknowledgment_payload)

        if acknowledgment_ack_number == sequence_number+acknowledgment_window:
            print(f'Received acknowledgment for packet {sequence_number}')
            window = acknowledgment_window
        else:
            acknowledgment_ack_number = acknowledgment_ack_number - window
            print(f'Received acknowledgment for packet {acknowledgment_ack_number}, but expected {sequence_number}')
            window = acknowledgment_window
    elif payload_size<window:
        print("file sent")
        break
    else:
        print('Did not receive acknowledgment')

    

# Close file
file.close()

endtime = time.time()

print(f'Throughput: {(file_size/ (endtime-starting_time))/1000.0} B/s')
    
# Close sockets
client_socket.close()
server_socket.close()
print('Done')