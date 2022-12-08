
from cProfile import label
from tkinter import messagebox
import socket
import threading
import pickle
from tkinter import *
import random




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
userId = "-1"
HEADERSIZE = 20



initYforAnotherPeer = 40
initYforAllPeer=10
# initYforMyMessage=40

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
# print("IP: ",IPAddr)
port = random.randint(4000,6000)
# print("port: ",port)

peerWelcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerWelcomeSocket.bind((IPAddr,port))
peerWelcomeSocket.listen()




connectionCreatingSocket={}


userAccount = ''
friendlistOfUser = []
inComingPeer= []
currentPersonInTalk = []




button_list = []
currentPerson_name_label = []
message_sending_label_list = []
message_receiving_label_list = []
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
# PEER FUNCTION##############################################################################
def responseToChosenPeer(oneSocket,messageToGetName):
    global connectionCreatingSocket 
    name = ''
    for i in messageToGetName:
        if i == ":":
            break
        else:
            name += i
    global currentPersonInTalk
    currentPersonInTalk = oneSocket
    connectionCreatingSocket = oneSocket
    reRenderPersonNameTag(name)
    reRenderMyMessageLabel()
    reRenderAnotherPeerMessageLabel()

def receiveFromCurrentPeer(aSocket):
    if (aSocket):
        print("is waitng in current peer")
        while True:
            try:
                message = aSocket.recv(1024).decode('ascii')
                
                
                messageToTake = ''
                canTake = False
                for i in message:
                    if canTake:
                        messageToTake +=i
                    if i == ":":
                        canTake = True
                print(messageToTake)
                
                
                global initYforAnotherPeer
                global message_receiving_label_list
                page2_messageFromAnotherPeer = Label(page_2,text=messageToTake, font=(10))
                page2_messageFromAnotherPeer.place(x=120,y=initYforAnotherPeer)
                initYforAnotherPeer += 30
                message_receiving_label_list.append(page2_messageFromAnotherPeer)

                print("Your friend said: ",message)
            except:
                print("error")
                aSocket.close()
                break
    else:
        print("asocket not defined")

def receiveAllMessage(client,address):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            userAccount = ""
            userPassword = ""
            print(f"{address} said: {message}")   
            # print("this is current person")    
            global currentPersonInTalk
            # global currentPersonName
            if (currentPersonInTalk != client):
                # currentPersonName
                page2_messageFromAllPeer_button = Button(page_2,text=f'{message}', wraplength=100,font=(10), command=lambda: responseToChosenPeer(client,message))
                print("before")
                global initYforAllPeer
                page2_messageFromAllPeer_button.place(x=420,y=initYforAllPeer)
                print("after")
                initYforAllPeer += 50
                
            else:
                # render on chatbox
                global initYforAnotherPeer
                messageToTake = ''
                canTake = False
                for i in message:
                    if canTake:
                        messageToTake +=i
                    if i == ":":
                        canTake = True
                    
                print(messageToTake)


                page2_messageFromAllPeer_label = Label(page_2,text=messageToTake, wraplength=100,font=(10))
                page2_messageFromAllPeer_label.place(x=200,y=initYforAnotherPeer)
                initYforAnotherPeer += 50
                print("")



        except:
            print("hic")
            client.close()
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
            

            receive_thread = threading.Thread(target= receiveFromCurrentPeer, args=(connectionCreatingSocket,))
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

        rec_message_thread = threading.Thread(target=receiveAllMessage, args=(client,address) )
        rec_message_thread.start()


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
###########BETWEEN UI AND USER#######################

def reRenderPersonNameTag(name): 
    global currentPerson_name_label
    # global currentPerson_name_value

    for label in currentPerson_name_label:
        label.place(width=0,height=0)
    currentPerson_name_label= []
    page2_person_label = Label(page_2,text=name, font=('Bold',15))
    page2_person_label.place(x=200,y=5)
    currentPerson_name_label.append(page2_person_label)   
    
def reRenderMyMessageLabel():
    global message_sending_label_list
    for label in message_sending_label_list:
        label.place(width=0,height=0)
    message_sending_label_list= []
def reRenderAnotherPeerMessageLabel():
    global message_receiving_label_list
    for label in message_receiving_label_list:
        label.place(width=0,height=0)
    message_receiving_label_list= []



####################################################################################################

def connectToAnotherPeer(ip,port):
    global connectionCreatingSocket
    connectionCreatingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectionCreatingSocket.connect((ip,port))

   

    receive_thread = threading.Thread(target= receiveFromCurrentPeer, args=(connectionCreatingSocket,))
    receive_thread.start()

def sendMessageToCurrentPeer(message):
    global connectionCreatingSocket
    global userAccount
    if connectionCreatingSocket != {}:
        connectionCreatingSocket.send(f'{userAccount}:{message}'.encode('ascii'))
        print("You said: ",message)


        global initYforAnotherPeer
        global message_sending_label_list
        my_sending_message_label = Label(page_2, text=f'{message}', wraplength=100,font=(10), bg="blue")
        my_sending_message_label.place(x=300,y=initYforAnotherPeer,height=50, width=100)
        message_sending_label_list.append(my_sending_message_label)
        initYforAnotherPeer += 50


    else:
        print("connectionCreatingSocket is not yet defined")



def stopTalkingWithCurrentPeer():
    global connectionCreatingSocket
    connectionCreatingSocket.close()
    connectionCreatingSocket = {}
    reRenderPersonNameTag('')

def talkToPeer(ip,port,name): 
    # print("is talking to",name)
    connectToAnotherPeer(ip,port)
    reRenderPersonNameTag(name)
   
########################################################################
########################################################################
########################################################################
########################################################################







def sendLoginInfoToServer(account,password):
    global userAccount
    userAccount = account
    message = client.recv(1024).decode('ascii')
    print(message)
    client.send("LOG".encode('ascii'))
    message = client.recv(1024).decode('ascii')
    print(message)
    if message == 'ACCOUNT: ':
        client.send(account.encode('ascii'))
    message = client.recv(1024).decode('ascii')
    print(message)
    if message == 'PASSWORD: ':
        client.send(password.encode('ascii'))
    message = client.recv(1024).decode('ascii')
    print(message)
    if message == 'OKAY':
        idMessageFromServer = client.recv(1024).decode('ascii')
        global userId 
        userId =  idMessageFromServer
        print("Id is ",userId)

        client.send(IPAddr.encode('ascii'))
        client.send(f'{port}'.encode('ascii'))

        return True
    else:
        return False



def updateStatusToOffline():
    if userId != "-1":
        client.send("OFFLINE".encode('ascii'))
        client.send(userId.encode('ascii'))


def getOnlineFriendlist():
    print(userId)
    client.send("FRIENDLIST".encode('ascii'))
    message = client.recv(1024).decode('ascii')
    if message=="CONTINUE":

        client.send(f'{userId}'.encode('ascii'))  
    
        global friendlistOfUser
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
               
                friendlistOfUser = d["friendlist"]
                new_msg = True
                full_msg = b''
                break
        print("friendlistOfUser",friendlistOfUser)

        global button_list

        for butt in button_list:
            print("here")
            butt.place(width=0, height=0)


        initY=10
        for data in friendlistOfUser:
            print(data)
            name_button = Button(page_2, text=f'{data["account"]}', command=lambda: talkToPeer(data["IP"],data["port"],data["account"]))
            name_button.place(x=10,y=initY,width=100,height=50)
            button_list.append(name_button)
            initY += 70



########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
#####################################################





window = Tk()
window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)
# window.state('normal')
window.geometry('500x500')
window.title('Chat App')


page_1 = Frame(window)
page_2 = Frame(window)
 

for frame in (page_1,page_2):
    frame.grid(row=0,column=0,sticky='nsew')


def show_frame(frame):
    frame.tkraise()

show_frame(page_1)


def login(account,password,next_frame,old_frame):
    response = sendLoginInfoToServer(account,password)
    # if a+b==2:
    # print("hello")
    
    if response == True:
        # print("hello again")
        show_frame(next_frame)
    else:
        show_frame(old_frame)



# PAGE LOGIN####################################
page1_label1 = Label(page_1,text='User Account', font=('Bold',15))
page1_label1.place(x=70,y=100)

page1_entry1 = Entry(page_1)
page1_entry1.place(x=220,y=106)


page1_label2 = Label(page_1,text='User Password', font=('Bold',15))
page1_label2.place(x=70,y=150)

page_1_entry2 = Entry(page_1)
page_1_entry2.place(x=220,y=156)

page1_button = Button(page_1, text='LOGIN', font=('Bold',15) , command=lambda: login(page1_entry1.get(),page_1_entry2.get(),page_2,page_1))
page1_button.place(x = 220, y= 300)
########################################################################



# PAGE CHATTING####################################
page_2.grid(row=0,column=0,padx=20,pady=20,ipadx=20,ipady=20)

# page2_label1 = Label(page_2,text='Chat Page', font=('Bold',15))
# page2_label1.place(x=70,y=100)


page2_button = Button(page_2, text='Get Friendlist', wraplength=100,font=('Bold',15) , command=lambda: getOnlineFriendlist())
page2_button.place(x = 10, y= 300, width=100, height=100)

chatBox = Entry(page_2, width=50)
chatBox.place(x=150,y=300,height=50)

sendMessageButton = Button(page_2, text='SEND', font=('Bold',15) , command=lambda: sendMessageToCurrentPeer(chatBox.get()))
sendMessageButton.place(x = 200, y= 350,height=50)

stopTalkingButton = Button(page_2, text='STOP', font=('Bold',15) , command=lambda: stopTalkingWithCurrentPeer())
stopTalkingButton.place(x = 280, y= 350,height=50)

my_row,my_col=0,0
# print("friendlist of user",friendlistOfUser)


# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################
# #############################################################################################


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        updateStatusToOffline()
        global connectionCreatingSocket
        if connectionCreatingSocket!={}:
            connectionCreatingSocket.close()
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
###########BETWEEN UI AND USER#######################




















































########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
# CLIENT FUNCTION#################################################################################

def connectToServer():
    client.connect(('127.0.1.1',55555))

def sendLoginInfo(client):
    account = input("please input account") 
    string = f'ACC:{account}'
    client.send(string.encode('ascii'))
    password = input("please input password") 
    string = f'PAS:{password}'
    client.send(string.encode('ascii'))

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
            

            # elif message == 'FRIEND_LIST_AND_ADDRESS: ':
            #     # recieve the list of friend
            #     objCurrentOnlineFriendList= recieveObj(client)
            #     currentOnlineFriendList = objCurrentOnlineFriendList["friendlist"]
            #     print("this is your friend online list",currentOnlineFriendList)
            #     userClientWantToTalkTo = int(input("which user you want to talk to"))
            #     # talkToPeer(currentOnlineFriendList[userClientWantToTalkTo])

            elif message == 'OKAY':
                show_frame(page_2)

            else:
                print(message)

        except:
            print("error")
            client.close()
            break








connectToServer()


receive_connection_thread = threading.Thread(target=receiveConnection)
receive_connection_thread.start()


window.mainloop()




