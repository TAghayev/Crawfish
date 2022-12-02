import threading 
import socket

host = '127.0.0.1' # Local Host
port = 55555 # Port

IDs = [[],[],[]] 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Start the server
server.bind((host, port)) #Server is bound to the local host on our port
server.listen() #Port starts listening