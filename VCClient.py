from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from time import sleep
import sys

def receive():
    #Handles receiving of messages
    while 1:
        try:
            if flag == True:
                msg = client.recv(BUFSIZ).decode("utf8")
                print (msg)
            
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  #Event is passed by binders.
    """Handles sending of messages."""
    client.send(bytes(my_msg, "utf8"))
    if my_msg == "/quit":
        client.close()

def on_closing(event=None):
    my_msg = "/quit"
    send()
    
#----Now comes the sockets part----
HOST = str(sys.argv[3])
PORT = int(sys.argv[2])
NAME = str(sys.argv[1])

print (sys.argv)
if not PORT:
    PORT = 2000
BUFSIZ = 4096
ADDR = (HOST, PORT)
client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)
flag = True
receive_thread = Thread(target=receive)
receive_thread.start()
sleep(0.2)
my_msg = NAME

send()
sleep(0.2)
while 1:
    my_msg = input("\n")
    # For the messages to be sent.
    if my_msg == '/quit':
        on_closing()
        break
    elif my_msg == '/sleep':
        flag = False
    elif my_msg == '/wake':
        flag = True
    else:
        send()
        sleep(0.2)
