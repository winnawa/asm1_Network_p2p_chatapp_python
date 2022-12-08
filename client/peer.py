import pickle
import random
import threading
import socket
import json



hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
# print("IP: ",IPAddr)
port = random.randint(4000,6000)
# print("port: ",port)

peerWelcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerWelcomeSocket.bind((IPAddr,port))
peerWelcomeSocket.listen()


inComingPeer= []

def recieveMessage(client,address):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            userAccount = ""
            userPassword = ""
            print(f"{address} said: {message}")            
        except:
            print("hic")
            break


# def sendMessage():
#     while True:
#         message = input("Send message to server")
#         client.send(message.encode('ascii'))

def receive(aSocket):
    while True:
        try:
            message = aSocket.recv(1024).decode('ascii')
            print("Your friend said: ",message)
        except:
            print("error")
            aSocket.close()
            break


def userAction():
    while True:
        message = input("What you want to do: ")
        if message == "CONNECT TO ANOTHER PEER":
            IP = input("input IP address: ")
            port = int(input("input port address: "))
            connectionCreatingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connectionCreatingSocket.connect((IP,port))
            stopTalking = False
            

            receive_thread = threading.Thread(target= receive, args=(connectionCreatingSocket,))
            receive_thread.start()

            while True:
                message = input("Okat so now we connect, what you want to send to other peer: ")
                if  message == "QUIT":
                    stopTalking = True
                    break
                else:
                    connectionCreatingSocket.send(message.encode('ascii'))
                    print("You said: ",message)
            connectionCreatingSocket.close()




        elif message == "ANSWER MESSAGE FROM PEER":
            IP = input("input IP address: ")
            port = int(input("input port address: "))
            socketConnection={}
            found = False
            for element in inComingPeer:
                print("this is in inComingPeer list",element)
                if element["IP"] == IP and element["port"]==port :
                    socketConnection = element["socket"]
                    found = True
                    break
            if found:
                print(socketConnection)
                while True:
                    message = input("what do you want to say: ")
                    socketConnection.send(message.encode('ascii'))


            else:
                print("address not found")
        else:
            print("Sorry we dont understand this command")    



def receiveConnection(): 
    while True:
        print(f"i am listening on IP {IPAddr}, port {port}")
        client, address = peerWelcomeSocket.accept()
        print(f"{str(address)} connects to you")        
        
        peerObj = {"socket": client, "IP": address[0], "port":address[1]}
        inComingPeer.append(peerObj)



        currentClient = client
        #print(currentClient)

        rec_message_thread = threading.Thread(target=recieveMessage, args=(client,address) )
        rec_message_thread.start()

       
        
        # send_message_thread = threading.Thread(target=sendMessage, args= (currentClient,))
        # send_message_thread.start()


       
        # sendFriendList(client)
# receiveConnection()




def startProgram():
    receive_connection_thread = threading.Thread(target=receiveConnection)
    receive_connection_thread.start()
    
    user_action_thread = threading.Thread(target=userAction)
    user_action_thread.start()


startProgram()