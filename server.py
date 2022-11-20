# Import the libraries

import threading
import socket

#Define a host address and port
host = '127.0.0.1' # Local Host
port = 12345 # Port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start the server
server.bind((host, port)) #Server is bound to the local host on our port
server.listen() #Port starts listening

clients = [] # List of all clients
nicknames = [] # List of clients' nicknames

#Function that sends the message to clients that are currently connected

def broadcast(message):
    for client in clients: # For every client that is online
        client.send(message) # Send the message to a client

def handle(client):
    while True: # Endless loop
        try:
            message = client.recv(1024) # If message is received succeessfully
            broadcast(message) # Broadcast the message to all
        except:
            index = clients.index(client) # Index of the client who's message failed
            clients.remove(client) # Remove this client
            client.close() # Close the connection to the client
            nickname = nicknames[index] # Get the nickname of the client
            broadcast(f'{nickname} left the chat!'.encode('ascii')) # Broadcast that the user has left the server
            nicknames.remove(nickname) # Remove the nickname of the deleted client
            break # Break the loop to terminate the thread


def receive():
    while True:
        client, address = server.accept() # Accept all the connections, if the connection is received, client and the adress are returned
        print(f"Connected with {str(address)}") # Print that the connection was successfull

        client.send('NICK'.encode('ascii')) # Send a client the ketword NICK
        nickname = client.recv(1024).decode('ascii') # Receive the nickname from the client
        nicknames.append(nickname) # Append the nickname to nickname list
        clients.append(client) # Append the client to the clients list

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('arcii'))

        thread = threading.Thread(target = handle, args = (client, )) # One thread per each client, because we need to process messages at the same time
        thread.start()

# Main method
print("Server is listening...")
receive()