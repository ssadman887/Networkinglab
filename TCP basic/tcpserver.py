from socket import *
servername ='localhost'
serverport = 12000
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(('',serverport))
serversocket.listen(1)
print("The server is ready to receive:")
while True:
    connectionsocket, addr = serversocket.accept()
    messege = connectionsocket.recv(1024).decode()
    capitalizedsentence = messege.upper()
    connectionsocket.send(capitalizedsentence.encode())
    connectionsocket.close()
