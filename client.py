import socket
import threading

chatname = input("Chatname: ")

#Connect internet socket by TCP (localhost)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(chatname.encode('ascii'))
            else:
                print(message)
        except:
            print("INTERNAL ERROR!")
            client.close()
            break

def write():
    while True:
        message = "{}: {}".format(chatname,input(' '))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()