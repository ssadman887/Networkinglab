import socket
import time
import os

source_port = 9500


fr = False
cwnd = 1
ssthresh = 400

def slow_start():
    global cwnd
    cwnd *= 2


def congestion_avoidance():
    global cwnd
    cwnd += 1
    

def fast_recovery():
    global ssthresh, cwnd
    ssthresh = cwnd // 2
    cwnd = ssthresh + 3

packet_queue = {

}

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
server_socket.bind(('localhost', source_port))
server_socket.listen(10)

print('Server is listening for incoming connections')

client_socket, address = server_socket.accept()
destination_port = address[1]


print(f'Accepted connection from {address}')

# Open file to be sent
file = open('file_to_send.txt', 'rb')
file_size = os.path.getsize('file_to_send.txt')


sequence_number = 0
recovery_sequence_number = 0
last_ack = 0    
dup_count = 0
ack_number=0
starting_time=time.time()

packet = client_socket.recv(1500)
source_port, destination_port, seq, ack, flag, rwnd, payloadlen, payload = packet_decode(packet)
last_ack = ack
print(f'Initial rwnd: {rwnd}')

while True:

    if fr:
        print("Fast Recovery mode")
        for seq_recovery in packet_queue:
            if seq_recovery>recovery_sequence_number:
                payload = packet_queue[seq_recovery]
                recovery_sequence_number=seq_recovery
                payloadlen = len(payload)
                packet = packet_encode(seq_recovery, ack_number, rwnd, 1, payloadlen, payload, destination_port)
                client_socket.send(packet)
                break

        if recovery_sequence_number==sequence_number:
            fr = False

    else:
        print("General mode")
        max_cut = min(cwnd,rwnd)
        payload = file.read(max_cut)
        if not payload:
            print("File sent Successfully")
            packet = packet_encode(-1, -1, rwnd, 1, 0, "".encode('utf-8'), destination_port)
            client_socket.send(packet)
            break
        payloadlen = len(payload)
        sequence_number+=payloadlen
        packet_queue[sequence_number] = payload
        ack_number+=1
        packet = packet_encode(sequence_number, ack_number, rwnd, 1, payloadlen, payload, destination_port)
        client_socket.send(packet)
        print(f'send seq:{sequence_number}')
    
    

    try:
         print("Waiting for ack")
         acknowledgement = client_socket.recv(1500)
         cli_source_port, cli_destination_port, cli_seq, cli_ack, cli_flag, cli_rwnd, cli_payloadlen, cli_payload = packet_decode(acknowledgement)

         if cli_ack == sequence_number:
            print("Received ack:", cli_ack)

            if cwnd < ssthresh:
                slow_start()
            else:
                congestion_avoidance()
         elif dup_count == 3:
            print("Triple duplicate ack. Fast Recovery mode activated")
            fast_recovery()
            fr = True
            recovery_sequence_number = last_ack
            print("Fast recovery")
            dup_count = 0
        
         elif cli_ack == last_ack:
            dup_count += 1
         else:
            dup_count = 0
            last_ack = cli_ack

    except socket.timeout:
        print("Timeout")   
        ssthresh = cwnd // 2
        cwnd = 1           

# Close file
file.close()

print(f'Throughput: {(file_size/ (time.time()-starting_time))} B/s')
    
# Close sockets
client_socket.close()
server_socket.close()
print('Done')