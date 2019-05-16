"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys


def accept_incoming_connections():
    #Sets up handling for incoming clients.
    while True:
        client, client_address = SERVER.accept() #Client and his info gets here.
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address #address dictionary
        Thread(target=handle_client, args=(client,)).start() #Every client have his/her own thread.


def handle_client(client):  # Takes client socket as argument.
    #Handles a single client connection.
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = ('Welcome %s! If you ever want to quit, type /quit to exit.' % name)
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    clients[name] = client #client dictionary: name - socket
    for sock in clients:
        t = clients[sock]
        t.send(bytes(str(msg), "utf8"))
    
    while True:
        msg = client.recv(BUFSIZ)
        print(name,': ',msg.decode())

        if msg == bytes("/name", "utf8"):
            msg = client.recv(BUFSIZ)
            oldname=msg.decode()
            msg = client.recv(BUFSIZ)
            newname=msg.decode()
            clients[newname] = clients.pop(oldname)
            name = newname
            continue

        elif msg == bytes("/file", "utf8"):
            print('in file function.')       
            with open('test.txt', "wb") as fw:
              while True:
                  msg = client.recv(BUFSIZ)
                  fw.write(msg)
                  break
              fw.close()
              
        elif msg == bytes("/quit", "utf8"): #Quit fuctionality
           print ('%s: has left the chat.' % name )
           client.close()
           #close the specific client from server side.
           del clients[name]
           for sock in clients:
                t = clients[sock]
                t.send(bytes("%s: has left the chat." % name, "utf8"))
           break
        else:
            msg = name+": "+(msg.decode())
            for sock in clients:
                t = clients[sock]
                t.send(bytes(str(msg), "utf8"))
                continue
        
clients = {}
addresses = {}

HOST = ''
PORT = 2000
if not PORT: #Default port set to 2000
    PORT = 2000

BUFSIZ = 64000
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) #Binder which binds with the incoming host.

if __name__ == "__main__":
   SERVER.listen(10)
   print("Waiting for connection...")
   ACCEPT_THREAD = Thread(target=accept_incoming_connections)
   ACCEPT_THREAD.start()
   ACCEPT_THREAD.join()
SERVER.close()
