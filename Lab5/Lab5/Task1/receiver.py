import socket
import time
import os 
import random

destination_port = 8500
source_port = 0


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
    
def packet_encode(seq, ack, window, flag, payloadlen, payload):
    seq = int(seq)
    ack = int(ack)
    window = int(window)
    transport_header = f'{source_port:04d}{destination_port:04d}{seq:06d}{ack:06d}{flag:01d}{window:05}{payloadlen:04d}'.encode('utf-8')[:30].ljust(30)
    packet = transport_header + payload
    return packet

# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
source_port = int(client_socket.getsockname()[1])
client_socket.connect(('localhost', 8500))

client_socket.settimeout(5)

print('Connected to server')

#buffer
window=1470
rec_ack=1470
rec_seq =0
packet = packet_encode(0,rec_ack,window,1,0,"".encode('utf-8'))
client_socket.send(packet)

start_time = time.time()

# Receive packets and write to file
with open('received_file.txt', 'wb') as file:
    while True:
        try:
            packet = client_socket.recv(1500)

            if not packet:
                print("No packet received.")
                break
            r_source_port, r_destination_port, seq, ack, flag, r_window, payloadlen, payload = packet_decode(packet)
            # print("received")
            # print(source_port, destination_port, seq, ack, flag, window, payloadlen, payload)

            print(f"Received packet with seq {seq}")

            if rec_ack==seq:
                file.write(payload)
                print(f"Received {seq} and wrote to file")
                rec_ack+=window
                packet = packet_encode(rec_seq, rec_ack, window, 1, 0, "".encode('utf-8'))
                client_socket.send(packet)
            elif payloadlen<window:
                file.write(payload)
                print(f"file receive complete")
                break
            else:
                print(f"Packet with seq {seq} dropped")
                packet = packet_encode(rec_seq, rec_ack, window, 1, 0, "".encode('utf-8'))
                client_socket.send(packet)
        except socket.timeout:
            print("Timeout")
            break
endtime = time.time()
print("file received in", round(endtime - start_time,2), "seconds")
file_size = os.path.getsize('received_file.txt')
print(f'Throughput: {(file_size/ (endtime-start_time))/1000.0} B/s')

client_socket.close()
print("Connection closed")





            