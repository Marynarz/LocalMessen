import socket
import threading

#tworzenie socketa
servsoc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#bindowanie socketa
servsoc.bind((socket.gethostname(),80))
#listening
servsoc.listen(5)

while True:
    (clientsocket, address) = serversocket.accept()
    clientThr = client_thread(clientsocket)
    clientThr.run()