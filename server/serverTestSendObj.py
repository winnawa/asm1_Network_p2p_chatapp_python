import pickle
import threading
import socket
import json



hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print(IPAddr)
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IPAddr,port))
server.listen()

currentClientAddress = []
currentClientInfo= []
currentClientId= []

currentNickname = []



def receiveConnection(): 
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")        
        print(f'{address} joined the chat')
        
        
        d = {1: "Hey",2: "There", "hi":[{"one":1},{"two":2},{"three":3}]}
        msg = pickle.dumps(d)
        msg = bytes(f'{len(msg):<{20}}', "utf-8") + msg
        client.send(msg)


receiveConnection()