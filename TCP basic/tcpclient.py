from socket import *
servername ='localhost'
serverport = 12000
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((servername,serverport))

messege = input('input lowercase sentence:')

clientsocket.send(messege.encode()) #convert from string to byte type
modifiedmessege, _ = clientsocket.recvfrom(1024) # Extract data from tuple
print('from server', modifiedmessege.decode())
clientsocket.close()
