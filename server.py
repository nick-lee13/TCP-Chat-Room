import socket
import threading

#Connection (Host used on local network for testing)
host = '127.0.0.1'
port = 55555

#Start server(Internet socket, TCP Connection)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Clients and their chosen chat names
clients = []
chatnames = []

#Sends message to all clinmets currently connected
def broadcast(message):
    for client in clients:
        client.send(message)

#Handle messaging from clients
def handle(client):
    while True:
        try:
            #Send message from client
            message = client.recv(1024)
            broadcast(message)
        except:
            #Cut connection from client and announce leaving
            index = clients.index(client)
            clients.remove(client)
            client.close()
            chatname = chatnames[index]
            broadcast('{} has left the chat!'.format(chatname).encode('ascii'))
            chatnames.remove(chatname)
            break

#Function for receiving and listening
def receive():
    while True:
        #Accept connections
        client, address = server.accept()
        print("{} Connected!".format(str(address)))

        #Ask client for chatname and store
        client.send('NICK'.encode('ascii'))
        chatname = client.recv(1024).decode('ascii')
        chatnames.append(chatname)
        clients.append(client)

        #Print and broadcast chatname
        print("chatname is {}".format(chatname))
        broadcast("{} has joined!".format(chatname).encode('ascii'))
        client.send('You are connected to the server!'.encode('ascii'))

        #Handle thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server listening...")
receive()