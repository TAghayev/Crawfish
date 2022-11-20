# echo-client.py

import socket
import threading

nickname = input ("Choose a nickname")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Define a client
client.connect(('127.0.0.1', 12345)) # Server triggers the accept method and sets up the connection



def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii') # Receive messages from the server
            if message == 'NICK': # If we get the NICK key word, then we send the nickname
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close() # Close the connection
            break # Break out of the loop


def write():
    while True:
        message = f'{nickname}: {input("")}' # Constantly wait for the new message
        client.send(message.encode('ascii')) # Send the message
        # Run receive and run threads at the same time

receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()
