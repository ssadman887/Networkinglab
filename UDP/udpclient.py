from socket import *
servername ='localhost'
serverport = 12000
clientsocket = socket(AF_INET, SOCK_DGRAM)
messege = input('input lowercase sentence:')
clientsocket.sendto(messege.encode(), (servername,serverport)) #convert from string to byte type
modifiedmessege, serveraddress = clientsocket.recvfrom(2048) #2MB buffer
print(modifiedmessege.decode())
clientsocket.close()
