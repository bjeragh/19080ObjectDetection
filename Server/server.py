#!/usr/bin/python3

import socket #import the socket module

s = socket.socket() #Create a socket object
host = '192.168.0.244' #Get the local machine name
print(host)
port = 50002 # Reserve a port for your service
s.bind((host,port)) #Bind to the port

s.listen(5) #Wait for the client connection
while True:
    c,addr = s.accept() #Establish a connection with the client
    print ("Got connection from", addr)
    c.send(b"Connected")
    data = c.recv(1024)
    print (data)
    c.close()


