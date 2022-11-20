# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.connect((HOST, PORT))
    while True :
        user_input = input("what u wan say? :")
        s.sendall(bytes(user_input, 'utf-8'))
        data = s.recv(1024)

