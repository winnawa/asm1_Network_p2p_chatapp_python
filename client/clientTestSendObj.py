import pickle
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.1.1',55555))
peopleInConversation = []
account = ""
password = ""
id = -1

HEADERSIZE = 20
while True:

    full_msg = b''
    new_msg = True
    while True:
        msg = client.recv(1024)
        print("new message recieve")

        if new_msg:
            print(f'new message length: {msg[:HEADERSIZE]}')
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
            print("full message received")

            d = pickle.loads(full_msg[HEADERSIZE:])
                    
            # print(d)
            new_msg = True
            full_msg = b''
    