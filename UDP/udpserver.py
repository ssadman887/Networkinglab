from socket import *
servername ='localhost'
serverport = 12000
serversocket = socket(AF_INET, SOCK_DGRAM)
serversocket.bind(('',serverport))
print("The server is ready to receive:")
while True:
    messege,clientAddresss= serversocket.recvfrom(2048)
    modifiedmessege = messege.decode().upper()
    serversocket.sendto(modifiedmessege.encode(), clientAddresss)
