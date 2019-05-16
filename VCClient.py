from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from time import sleep
import sys

def receive():
    #Handles receiving of messages
    while 1:
        try:
            #flag for sleep and wake functions 
            if flag == True:
                msg = client.recv(BUFSIZ).decode("utf8")
                naming = msg.split(':')
                if naming[0] not in blocked: 
                    print (msg)
        except:
            pass

def send(event=None):
    #Event is passed by binders.
    #Handles sending of messages.
    client.send(bytes(my_msg, "utf8"))
    if my_msg == "/quit":
        client.close() #client is disconnected from server

def on_closing(event=None): #Termination Message
    my_msg = "/quit"
    send()
    
#----Now comes the sockets part----
HOST = str(sys.argv[3])
PORT = int(sys.argv[2])
NAME = str(sys.argv[1])

print (sys.argv)
if not PORT: #default port is set to 2000
    PORT = 2000
BUFSIZ = 4096
ADDR = (HOST, PORT) 
client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR) 
flag = True #True for waked client.
receive_thread = Thread(target=receive) #receive thread
receive_thread.start() 
sleep(0.2)
my_msg = NAME
blocked = []
send()
sleep(0.2)
while 1:
    my_msg = input("\n")
    # For the messages to be sent.
    if my_msg == '/quit':
        on_closing()
        break
    elif my_msg == '/sleep': #Sleep functionality
        flag = False
    elif my_msg == '/wake': #Wake functionality
        flag = True
    elif my_msg == '/block': #Block functionality
        bn = input('enter blocking name: ')
        blocked.append(bn)
    elif my_msg == '/unblock': #Unblock functionality
        un = input('enter unblocking name: ')
        blocked.remove(un)

    elif my_msg == '/file':#FTP
        send()
        with open('test.txt', 'rb') as fs:
            my_msg = fs.read(BUFSIZ)
            client.send(my_msg)
            
    elif my_msg == '/name': #Name Changing functinality
        send() #sends /name
        sleep(0.2)
        my_msg = NAME 
        send() #sends oldname
        name=input("Enter new name: ")
        my_msg = name
        sleep(0.2)
        send() #sends newname
        NAME = name
        sleep(0.4)
        my_msg = name
        send()
        continue
    else:
        send()
        sleep(0.2)
