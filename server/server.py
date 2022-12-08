
import threading
import socket
import sqlite3

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IPAddr,port))
server.listen()

currentClient = []
currentNickname = []























def recieveMessage(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(f'client said: {message}')
        except:
            break

def sendMessage(client):
    while True:
        message = input("enter message")
        client.send(message.encode('ascii'))
       
def receiveConnection(): 
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        print(f'{nickname} joined the chat')

        currentClient = client
        print(currentClient)
        currentNickname = nickname


        rec_message_thread = threading.Thread(target=recieveMessage, args=(client,) )
        rec_message_thread.start()
        send_message_thread = threading.Thread(target=sendMessage, args= (currentClient,))
        send_message_thread.start()

receiveConnection()