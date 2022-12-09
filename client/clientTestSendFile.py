# import pickle
# import socket
# import threading
# import os

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('127.0.1.1',55555))
# peopleInConversation = []
# account = ""
# password = ""
# id = -1



# file = open("image.png","rb")
# file_size = os.path.getsize("image.png")


# client.send("received_image.png".encode())
# client.send(str(file_size).encode())

# data = file.read()
# client.sendall(data)
# client.send(b"<END>")


# file.close()
# client.close()



import os, socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

filename = "image.png"

with open(filename, "rb") as file:
    file_size = os.path.getsize(filename)
    # protocol <filename>\n<size>\n<data>
    client.sendall(filename.encode("utf-8"))
    client.sendall(b"\n")
    client.sendall(str(file_size).encode("utf-8"))
    client.sendall(b"\n")
    data = file.read()
    client.sendall(data)
    client.close()