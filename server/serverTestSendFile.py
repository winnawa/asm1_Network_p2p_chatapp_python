import pickle
import threading
import socket
import os
import tqdm


# hostname=socket.gethostname()
# IPAddr=socket.gethostbyname(hostname)
# print(IPAddr)
# port = 55555

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((IPAddr,port))
# server.listen()



# client,addr = server.accept()
# file_name = client.recv(1024).decode()
# print(file_name)
# file_size = client.recv(1024).decode()
# print(file_size)



# file = open(file_name, "wb")
# file_bytes = b""
# done = False

# progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor= 1000, total= int(file_size))

# while not done:
#     data = client.recv(1024)
#     if file_bytes[-5:] == b"<END>":
#         done = True
#     else: 
#         file_bytes += data
#     progress.update(1024)


# file.write(file_bytes)

# file.close()
# client.close()

def recv_to_newline(s):
    buf = []
    while True:
        c = s.recv(1)
        if not len(c):
            # socket closed
            return None
        if c == b"\n":
            return b"".join(buf)
        buf.append(c)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

file_name = recv_to_newline(client).decode("utf-8")
print(file_name)
# file_size = int(client.recv(1024).decode("utf-8"))
file_size = int(recv_to_newline(client).decode("utf-8"))
print(file_size)

error = False
with open(file_name, "wb") as file:
    progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))
    while file_size:
        data = client.recv(min(1024, file_size))
        if not data:
            print("Error: Truncated recieve")
            error = True
            break
        file.write(data)    
        progress.update(len(data))
        file_size -= len(data)

if error:
    os.remove(file_name)
    
client.close()
server.close()