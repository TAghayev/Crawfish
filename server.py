import threading 
import socket
import transmission_construction as tc
import random
import pickle
import time

# definitions
enc_standard = 'utf8'
msg_len = 1024
host = '127.0.0.1' # Local Host
port = 55555 # Port
END_TRANSMISSION = b"break"

# globals
clients = {} # dictionary of clients
             # key: user_ID
             # value: client (object??)
keys = {} # dictionary of keys
          # key: user_ID
          # value: tuple(nickname, public_key, verification_key)

def broadcast(transmission) :
    for client in clients.values() :
        client.send(transmission)
        time.sleep(.2)
        client.send(END_TRANSMISSION)
    return

def unicast(target_ID, transmission) :
    client = clients[target_ID]
    client.send(transmission)
    time.sleep(.5)
    client.send(END_TRANSMISSION)
    return

def process_connection(id) :
    # THREAD: constant passing of user messages
    client = clients[id]
    nick, _, _ = keys[id]
    while True :
        try :
            tr = b""
            
            print("waiting for input from client:", nick)
            while True :
                
                packet = client.recv(msg_len)
                print(len(packet))
                if packet == END_TRANSMISSION:
                    break
                tr += packet
            print("recieved transmission")
            target_ID, mod_tr = tc.server_pass_mod(tr, id)
            unicast(target_ID, mod_tr)

        except Exception as e:
            print(e)

            # remove user on disconnect
            nick, _, _ = keys[id]
            clients.pop(id)
            keys.pop(id)
            print(nick, " disconnected!")
            client.close()

            # redistribute keys
            broadcast(pickle.dumps(keys))
            break
            

        
        

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
        tr = b""
        while True :
            packet = client.recv(msg_len)
            print(len(packet))
            if packet == b"break":
                break
            tr += packet
        new_ID = create_ID()
        keys[new_ID] = pickle.loads(tr)
        clients[new_ID] = client

        print("Recieved key info as ", pickle.loads(tr))
        
        # call for broadcast of keys
        broadcast(pickle.dumps(keys))
        print("keys broadcasted on connection from user: ", keys[new_ID][0])

        ct = threading.Thread(target = process_connection, args = (new_ID))
        ct.start()

if __name__ == "__main__" :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start the server
    server.bind((host, port)) #Server is bound to the local host on our port
    server.listen() #Port starts listening

    wait_for_connections(server)


