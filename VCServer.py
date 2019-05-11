"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept() #Client and his info gets here.
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = ('Welcome %s! If you ever want to quit, type /quit to exit.' % name)
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    clients[client] = name
    
    for sock in clients:
        sock.send(bytes(str(msg), "utf8"))
    
    while True:
        msg = client.recv(BUFSIZ)
        print(name,' : ',msg.decode())
        
        if msg != bytes("/quit", "utf8"):
            msg = name+": "+str(msg)
            for sock in clients:
                sock.send(bytes(str(msg), "utf8"))
        else:
            
           #client.send(bytes("/quit", "utf8"))
           print ('%s has left the chat.' % name )
           client.close()
           del clients[client]
           for sock in clients:
                sock.send(bytes("%s has left the chat." % name, "utf8"))
           break    

        
clients = {}
addresses = {}

HOST = ''
PORT = 2000
if not PORT:
    PORT = 2000

BUFSIZ = 64000
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
   SERVER.listen(10)
   print("Waiting for connection...")
   ACCEPT_THREAD = Thread(target=accept_incoming_connections)
   ACCEPT_THREAD.start()
   ACCEPT_THREAD.join()
SERVER.close()
