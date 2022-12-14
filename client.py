import threading
import socket
import transmission_construction as tc
import pickle
import time

# definitions
enc_standard = 'utf8' 
msg_len = 1024
host = '127.0.0.1'  # Local Host
port = 55555  # Port
END_TRANSMISSION = b"break"

# globals
keys = {}
keys_live = False

def print_online() :
    print("\nOnline Users")
    print(  "------------")
    for key in keys.keys() :
        nick, _, _ = keys[key]
        print(nick + " | id: " + str(key))
    print("\n")

def send_transmission(message, target_id, target_pubkey, signing_key):

    # call construct_transmission to build the message
    # send said message
    transmission = tc.construct_transmission(message, target_id, target_pubkey, signing_key)
    if len(transmission) > 0: return transmission #If the transmission is not empty, return
    else: pass # else nothing


def process_recieved_transmission(transmission, private_key):
    global keys, keys_live
    tr = pickle.loads(transmission)
    if type(tr) is dict :
        keys = tr
        # print("Keys transferred, ready to message!")
        keys_live = True
    else :
        # print("message recieved!")
        out = tc.deconstruct_transmission(transmission, private_key, keys)
        if out is None :
            return
        received_message, nick = tc.deconstruct_transmission(transmission, private_key, keys)
        print("\n" + nick + ": " + received_message)
        print("Enter a command:", end=" ")


def get_target_ID(input) :
    if input.isnumeric() :
        if int(input) in keys.keys() :
            return int(input)
    else :
        for user_id in keys.keys() : 
            nick, _, _ = keys[user_id] 
            if nick == input :
                return user_id
    return None

def process_command(input, client, sign) :

    if len(input) < 1 :
        print("Invalid command")
        return

    if input[0] != '/' :
        print("Input must begin with a slash '/'.")
        return

    if input[1] == 'w' :
        whisper = input[3:].split(" ", 1)
        if len(whisper) < 2 :
            print("No message entered!")
            return

        message = whisper[1]
        target_ID = get_target_ID(whisper[0])

        if target_ID is None :
            print("No such user :", whisper[0])
            return
        
        nick, pub, _ = keys[target_ID]
        transmission = tc.construct_transmission(message, target_ID, pub, sign)
        client.send(transmission)
        time.sleep(.2)
        client.send(b"break")
        print("sent :", message, "| to :", nick)
    if input[1] == "o" :
        print_online()

    return



def write_engine(client, pub, verif, nickname, sign):
    # THREAD: all outward messages from client
    print("write thread started.")
    # initialize - send keys to server with time delay
    client.send(pickle.dumps((nickname, pub, verif)))
    time.sleep(.2)
    client.send(b"break")
    time.sleep(3)

    # take command input from user and process accordingly
    while not keys_live :
        print("waiting...")
        time.sleep(1)
    while True:
        user_in = input("Enter a command: ")
        process_command(user_in, client, sign)
        


def read_engine(client, priv):
    # startup
    # recieves current public key array (the server should send this to the
    # new client first, hence no checks are necessary for )

    # main process engine
    while True:
        try:
            tr = b""
            while True :
                packet = client.recv(msg_len)
                # print(len(packet), "client read") DEBUG
                if packet == END_TRANSMISSION or len(packet) == 0:
                    break
                tr += packet
            
            input = process_recieved_transmission(tr, priv)
            if input is None:
                continue    #None occurs on error in deconstructing the transmission 
                            #(faulty transmission or tampering detected)

        except Exception as e:
            print(e)
            print("ERROR")
            client.close()
            break



if __name__ == "__main__":
    # main function

    # establish connection (standard socket stuff)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    nick = input("Connected to server, enter nickname: ")
    print("Hello ", nick, ", generating keys now.")
    # generate keys before even bothering with anything else
    pub, priv, sign, verif = tc.generate_keys()

    # read thread
    rt = threading.Thread(target=read_engine, args=(client, priv))
    rt.start()

    # write thread
    wt = threading.Thread(target=write_engine, args=(client, pub, verif, nick, sign))
    wt.start()

