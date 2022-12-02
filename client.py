import threading
import socket
import transmission_construction as tc

# definitions
enc_standard = 'utf8'
msg_len = 1028
host = '127.0.0.1' # Local Host
port = 55555 # Port

def send_transmission() :
    # call construct_transmission to build the message
    # send said message
    return

def process_recieved_transmission() :
    # call deconstruct_transmission to verify the message, post  process and print... something?
    return

def write_engine(client, pub, verif) :
    # startup
    # send keys to server, 
    
    client.send()

    while True :
        return

def read_engine(client) :
    # startup
    # recieves current public key array (the server should send this to the
    # new client first, hence no checks are necessary for )

    # main process engine
    while True :
        return 
        try:
            inbound_tr = client.recv(msg_len)
            input = process_recieved_transmission(inbound_tr)
            if input is None :
                continue # None occurs on error in deconstructing the transmission (faulty transmission or tampering detected)
            
            

        except :
            print("ERROR")
            client.close()
            break

    
    
if __name__ == "__main__" :
    # main function

    # establish connection (standard socket stuff)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # generate keys before even bothering with anything else
    pub, priv, sign, verif = tc.generate_keys()

    # write thread
    wt = threading.Thread(target = write_engine(client, pub, verif))
    wt.start()

    # read thread
    rt = threading.Thread(target = read_engine(client))
    rt.start()