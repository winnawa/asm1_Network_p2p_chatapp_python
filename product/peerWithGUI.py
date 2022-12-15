
from tkinter import filedialog, messagebox
import socket
import threading
import pickle
from tkinter import *
import random
import os
import tqdm


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
userId = "-1"
HEADERSIZE = 20

server_hostname=socket.gethostname()
server_IPAddr=socket.gethostbyname(server_hostname)

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
def receiveFile(asocket):
    file_name = recv_to_newline(asocket).decode("utf-8")
    print('at the receive file side: ',file_name)
    file_size = int(recv_to_newline(asocket).decode("utf-8"))
    print('at the receive file side: ',file_size)

    error = False

    file_name_without_path =''
    for i in file_name:
        if i == "/":
            file_name_without_path=''
        else:
            file_name_without_path +=i
    print("file name without path",file_name_without_path)

    with open(file_name_without_path, "wb") as file:
        progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))
        while file_size:
            data = asocket.recv(min(1024, file_size))
            if not data:
                print("Error: Truncated recieve")
                error = True
                break
            file.write(data)    
            progress.update(len(data))
            file_size -= len(data)
    if error:
        print('error happend in receiving ')
        os.remove(file_name_without_path)

    # print("end of writing  file")
    return file_name_without_path
    



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
    global initYforAnotherPeer
    initYforAnotherPeer = 40

def receiveFromCurrentPeer(aSocket):
    if (aSocket):
        print("is waitng in current peer")
        while True:
            try:
                message = aSocket.recv(1024).decode('ascii')
                
                global initYforAnotherPeer
                global message_receiving_label_list

                if message == 'SENDFILE':
                    print("in message == SENDFILE of current peer message")
                    file_name = receiveFile(aSocket)

                    if file_name != "":
                        page2_fileReceiving_label = Label(page_2,text=file_name,bg='white' ,wraplength=100,font=(10))
                        page2_fileReceiving_label.place(x=120,y=initYforAnotherPeer)
                        initYforAnotherPeer += 60
                        message_receiving_label_list.append(page2_fileReceiving_label)

                else:
                    messageToTake = ''
                    canTake = False
                    for i in message:
                        if canTake:
                            messageToTake +=i
                        if i == ":":
                            canTake = True
                    print(messageToTake)
                
                    if messageToTake == '':
                        messageToTake = message
                
                   
                    page2_messageFromAnotherPeer = Label(page_2,text=messageToTake, bg='white',font=(10))
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
                page2_messageFromAllPeer_button = Button(page_2,text=f'{message}', wraplength=200,font=(10), command=lambda: responseToChosenPeer(client,message))
                print("before")
                global initYforAllPeer
                page2_messageFromAllPeer_button.place(x=420,y=initYforAllPeer)
                print("after")
                initYforAllPeer += 50
                
            else:
                global initYforAnotherPeer
                global message_receiving_label_list
                if message == "SENDFILE":
                    print("in message == SENDFILE of all message")
                    file_name = receiveFile(client)
                    # receiveFile(client)
                    
                    

                    page2_fileReceiving_label = Label(page_2,text=file_name,bg='white' ,wraplength=100,font=(10))
                    page2_fileReceiving_label.place(x=120,y=initYforAnotherPeer)
                    initYforAnotherPeer += 60
                    message_receiving_label_list.append(page2_fileReceiving_label)

                else:
                # render on chatbox
                    
                    messageToTake = ''
                    canTake = False
                    for i in message:
                        if canTake:
                            messageToTake +=i
                        if i == ":":
                            canTake = True
                    
                    print(messageToTake)

                    

                    page2_messageFromAllPeer_label = Label(page_2,text=messageToTake,bg='white' ,wraplength=100,font=(10))
                    page2_messageFromAllPeer_label.place(x=120,y=initYforAnotherPeer)
                    initYforAnotherPeer += 60
                    message_receiving_label_list.append(page2_messageFromAllPeer_label)



        except:
            print("hic")
            client.close()
            break



# def userAction():
#     while True:
#         message = input("What you want to do: ")
#         if message == "CONNECT TO ANOTHER PEER":
#             IP = input("input IP address: ")
#             port = int(input("input port address: "))
#             connectionCreatingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             connectionCreatingSocket.connect((IP,port))
#             stopTalking = False
            

#             receive_thread = threading.Thread(target= receiveFromCurrentPeer, args=(connectionCreatingSocket,))
#             receive_thread.start()

#             while True:
#                 message = input("Okat so now we connect, what you want to send to other peer: ")
#                 if  message == "QUIT":
#                     stopTalking = True
#                     break
#                 else:
#                     connectionCreatingSocket.send(message.encode('ascii'))
#                     print("You said: ",message)
#             connectionCreatingSocket.close()




#         elif message == "ANSWER MESSAGE FROM PEER":
#             IP = input("input IP address: ")
#             port = int(input("input port address: "))
#             socketConnection={}
#             found = False
#             for element in inComingPeer:
#                 print("this is in inComingPeer list",element)
#                 if element["IP"] == IP and element["port"]==port :
#                     socketConnection = element["socket"]
#                     found = True
#                     break
#             if found:
#                 print(socketConnection)
#                 while True:
#                     message = input("what do you want to say: ")
#                     socketConnection.send(message.encode('ascii'))


#             else:
#                 print("address not found")
#         else:
#             print("Sorry we dont understand this command")    



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
    reRenderMyMessageLabel()
    reRenderAnotherPeerMessageLabel()
    global initYforAnotherPeer
    initYforAnotherPeer = 40


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
    # message = client.recv(1024).decode('ascii')
    # print(message)
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
            name_button = Button(page_2, text=f'{data["account"]}', command=lambda   ip=data["IP"],port=data["port"],name=data["account"]  : talkToPeer(ip,port,name))
            name_button.place(x=10,y=initY,width=100,height=50)
            button_list.append(name_button)
            initY += 70


def send_file():

    global connectionCreatingSocket
  
    if connectionCreatingSocket != {}:
        filename = filedialog.askopenfilename()
        # print('this is file name in send_file',filename)

        # connectionCreatingSocket.send("SENDFILE".encode('ascii'))
        if filename != "":

            with open(filename, "rb") as file:
                connectionCreatingSocket.send("SENDFILE".encode('ascii'))

                file_size = os.path.getsize(filename)
                # protocol <filename>\n<size>\n<data>
                connectionCreatingSocket.sendall(filename.encode("utf-8"))
                connectionCreatingSocket.sendall(b"\n")
                connectionCreatingSocket.sendall(str(file_size).encode("utf-8"))
                connectionCreatingSocket.sendall(b"\n")
                data = file.read()
                connectionCreatingSocket.sendall(data)
        

            file_name_without_path =''
            for i in filename:
                if i == "/":
                    file_name_without_path=''
                else:
                    file_name_without_path +=i
            print("file name without path in sending",file_name_without_path)
            global initYforAnotherPeer
            global message_sending_label_list
            my_sending_file_label = Label(page_2, text= file_name_without_path, wraplength=100,font=(10), bg="blue")
            my_sending_file_label.place(x=300,y=initYforAnotherPeer,height=50, width=100)
            message_sending_label_list.append(my_sending_file_label)
            initYforAnotherPeer += 50

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
sendMessageButton.place(x = 180, y= 350,height=50)

stopTalkingButton = Button(page_2, text='STOP', font=('Bold',15) , command=lambda: stopTalkingWithCurrentPeer())
stopTalkingButton.place(x = 260, y= 350,height=50)

upFileButton = Button(page_2, text='UPFILE', font=('Bold',15) , command=lambda: send_file())
upFileButton.place(x = 330, y= 350,height=50)



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
    global server_IPAddr
    client.connect((server_IPAddr,55555))

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




