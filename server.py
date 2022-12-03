import threading 
import socket
import transmission_construction as tc
import random
import pickle
enc_standard = 'utf8'
msg_len = 1028
host = '127.0.0.1' # Local Host
port = 55555 # Port

clients = {} # dictionary of clients
             # key: user_ID
             # value: client (object??)
keys = {} # dictionary of keys
          # key: user_ID
          # value: tuple(nickname, public_key, verification_key)

def broadcast(transmission) :
    for client in clients.values():
        client.send(transmission)
    return

def unicast(target_ID, transmission) :
    client = clients[target_ID]
    client.send(transmission)
    return

def process_connection(client) :
    return

def create_ID() :
    while True :
        user_ID = random.randint(1,100000)
        if user_ID not in clients.keys() :
            return user_ID

def wait_for_connections(server) :
    while True :
        client, address = server.accept()
        print("Connected with address", str(address))

        # recieve client input of tuple (nickname, public_key, verification_key)
        tr_in = client.recv(msg_len)
        new_ID = create_ID()
        keys[new_ID] = pickle.loads(tr_in)
        
        # call for broadcast of keys
        broadcast(pickle.dumps(keys))
        return


def distribute_keys():
    #on new user join, distribute new key dictionary
    pass


def push_transmission(transmission):
    target_id = tc.pull_target_id(transmission) #Pull the target id to figure out the destination.
    #TO-DO: send to appropriate user
    return True #REVIEW: returns True if pushed successfully?

if __name__ == "__main__" :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start the server
    server.bind((host, port)) #Server is bound to the local host on our port
    server.listen() #Port starts listening

    wait_for_connections(server)


