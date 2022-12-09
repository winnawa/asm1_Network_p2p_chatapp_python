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



def updateOfflineStatus(id):
    f = open('users.json', 'r')
    data = f.read()
    f.close()
    object = json.loads(data)

    for element in object["users"]:
        # print(element)
        if element["id"] == id:
            element["active"] = False
            
    # print(arrayofInfo)

    arrayInJSON = json.dumps(object)
    f = open('users.json', 'w')
    f.write(arrayInJSON)
    f.close()


def retrieveOnlineFriendlist(id):
    f = open('users.json', 'r')
    data = f.read()
    f.close()
    obj = json.loads(data)

    friendIdList = []
    for element in obj["friendship"]:
        if element["id"] == id:
            friendIdList = element["friendlist"]
            break
    
    # print(friendIdList)
    friendlist = []
    for element in obj["users"]:
        # print(element)
        for friendId in friendIdList:
            if element["id"] == friendId and element["active"]==True:
                friendlist.append(element)
                break
    # print(friendlist)
    return friendlist
    


def login(client):
    client.send("REG OR LOG".encode("ascii"))


def authenticate(account,password):
    f = open('users.json', 'r')
    data = f.read()
    f.close()
    obj = json.loads(data)

    id = -1
    for element in obj["users"]:
        # print(element)
        if element["account"] == account and element["password"] == password:
            id = element["id"]
            break
    return id


def updateAddress(id,IPaddress,port):
    print("iam in update")

    f = open('users.json', 'r')
    data = f.read()
    f.close()
    object = json.loads(data)

    for element in object["users"]:
        # print(element)
        if element["id"] == id:
            element["IP"] = IPaddress
            element["port"] = port
            element["active"] = True
            
    print(object["users"])

    arrayInJSON = json.dumps(object)
    f = open('users.json', 'w')
    f.write(arrayInJSON)
    f.close()
    
# updateAddress(0,"127.0.0.1",54048)


def registerNewAccount(account,password):
    f = open('users.json', 'r')
    data = f.read()
    f.close()
    object = json.loads(data)
    
    array = object["users"]
    newUser = {
        "id" : len(array),
        "account" : account,
        "password" : password,
        "IP" : "",
        "port" : -1,
    }
    array.append(newUser)
    # print(arrayofInfo)

    arrayInJSON = json.dumps(object)
    f = open('users.json', 'w')
    f.write(arrayInJSON)
    f.close()

    return newUser["id"]







def sendOnlineFriendlist(client,id):
    
    client.send("FRIEND_LIST_AND_ADDRESS: ".encode('ascii'))
    # print("i am here")
    friendlist = retrieveOnlineFriendlist(id)
    # print("this is friendlist")
    temporaryObj = {"friendlist":friendlist}

    msg = pickle.dumps(temporaryObj)
    msg = bytes(f'{len(msg):<{20}}', "utf-8") + msg
    client.send(msg)     




def recieveMessage(client,address):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            userAccount = ""
            userPassword = ""
            # if message == "REG":
            #     client.send("REGISTER_ACCOUNT: ".encode('ascii'))
            #     registerAccount = client.recv(1024).decode('ascii')
            #     # print(registerAccount)
            #     client.send("REGISTER_PASSWORD: ".encode('ascii'))
            #     registerPassword = client.recv(1024).decode('ascii')
            #     # print(registerPassword)
            #     id = registerNewAccount(registerAccount,registerPassword)
            #     updateAddress(id,address[0],address[1])
            #     currentClientId.append(id)
                # 


                # client.send("FRIEND_LIST_AND_ADDRESS: ".encode('ascii'))





            if message == "LOG": 
                client.send("ACCOUNT: ".encode('ascii'))
                userAccount = client.recv(1024).decode('ascii')
                # print(userAccount)
                client.send("PASSWORD: ".encode('ascii'))
                userPassword = client.recv(1024).decode('ascii')
                # print(userPassword)
                id = authenticate(userAccount, userPassword)
                # print(id)
                print(type(address[1]))
                if (id == -1):
                    client.send("user not found, please choose LOG or REG \n".encode('ascii'))
                    login(client)
                else:
                    client.send("OKAY".encode('ascii'))
                    client.send(f'{id}'.encode('ascii'))

                    tempIP = ''
                    tempPort = ''
                    tempIP = client.recv(1024).decode('ascii')        
                    tempPort = client.recv(1024).decode('ascii')
                    print(tempIP)
                    print(tempPort)

                    updateAddress(id,tempIP,int(tempPort))
                    currentClientId.append(id)
                    print("i am ok")
                    

                    # we send friendList

                    # sendOnlineFriendlist(client,id)

            elif message == "OFFLINE":
                idMessage = client.recv(1024).decode('ascii')
                updateOfflineStatus(int(idMessage))    
                print(address," left the chat")              
                break

            elif message == "FRIENDLIST":
                client.send("CONTINUE".encode('ascii'))
                idMessage = client.recv(1024).decode('ascii')
                friendlist = retrieveOnlineFriendlist(int(idMessage))
                d = {'friendlist': friendlist}
                msg = pickle.dumps(d)
                msg = bytes(f'{len(msg):<{20}}', "utf-8") + msg
                client.send(msg)

            else:
                print(f'client said: {message}')
                print('message not recognized')
                client.close()

        except:
            print("hic")
            client.close()
            break




def sendMessage(client):
    while True:
        message = input("enter message")
        client.send(message.encode('ascii'))
       

def receiveConnection(): 
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")        
        print(f'{address} joined the chat')
        
        currentClientAddress.append(address)


        

        currentClient = client
        #print(currentClient)

        rec_message_thread = threading.Thread(target=recieveMessage, args=(client,address) )
        rec_message_thread.start()
        # send_message_thread = threading.Thread(target=sendMessage, args= (currentClient,))
        # send_message_thread.start()


        login(client)
        # sendFriendList(client)
        client.send(str(address[1]).encode('ascii'))



receiveConnection()