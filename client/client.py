from concurrent.futures import thread
from email import message
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.1.1',55555))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                nickname = input("Enter a nickname")
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("error")
            client.close()
            break
def write():
    while True:
        message = input("Send message to server")
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target= receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()