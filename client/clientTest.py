
import socket
import threading
import pickle

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


currentOnlineFriendList = []
peopleInConversation = []
account = ""
password = ""
id = -1

def connectToServer():
    client.connect(('127.0.1.1',55555))

def sendLoginInfo(client):
    account = input("please input account") 
    string = f'ACC:{account}'
    client.send(string.encode('ascii'))
    password = input("please input password") 
    string = f'PAS:{password}'
    client.send(string.encode('ascii'))

def connectToPeople(client,peopleInConversation):
    for person in peopleInConversation:
        client.connect((person.IP,person.port))


def recieveObj(client):
    HEADERSIZE = 20
    returnObject={}
    # print("iam here")
    #online code
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
            print(d)
            returnObject=d
            new_msg = True
            full_msg = b''
            break
    #online code
    return returnObject



def talkToPeer():
    aSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)










# when online -> send user my IP and address
# get address of friend from user
# allow the user to input message, if message == INITIATE CONNECTION => choose people from friendlist

def receiveFromServer():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'REG OR LOG':
                response = input("Register(REG) or Login(LOG): ")                
                client.send(response.encode('ascii'))
            

            elif message == 'ACCOUNT: ':
                inputAccount = input("Please input account: ")                
                client.send(inputAccount.encode('ascii'))
            elif message == 'PASSWORD: ':
                inputPassword = input("Please input password: ")                
                client.send(inputPassword.encode('ascii'))
            
            
            elif message == 'REGISTER_ACCOUNT: ':
                registerAccount = input("Please input account for register: ")                
                client.send(registerAccount.encode('ascii'))
            elif message == 'REGISTER_PASSWORD: ':
                registerPassword = input("Please input password for register: ")                
                client.send(registerPassword.encode('ascii'))
            

            elif message == 'FRIEND_LIST_AND_ADDRESS: ':
                # recieve the list of friend
                objCurrentOnlineFriendList= recieveObj(client)
                currentOnlineFriendList = objCurrentOnlineFriendList["friendlist"]
                print("this is your friend online list",currentOnlineFriendList)
                userClientWantToTalkTo = int(input("which user you want to talk to"))
                talkToPeer(currentOnlineFriendList[userClientWantToTalkTo])









            else:
                print(message)




        except:
            print("error")
            client.close()
            break








def write():
    while True:
        message = input("Send message to server: ")
        client.send(message.encode('ascii'))















connectToServer()
# sendLoginInfo()
receive_thread = threading.Thread(target= receiveFromServer)
receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()