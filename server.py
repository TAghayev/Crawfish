import threading 
import socket
import transmission_construction as tc

enc_standard = 'utf8'
msg_len = 1028
host = '127.0.0.1' # Local Host
port = 55555 # Port



if __name__ == "__main__" :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start the server
    server.bind((host, port)) #Server is bound to the local host on our port
    server.listen() #Port starts listening
