#!/usr/bin/python3

import socket
import subprocess

s = socket.socket()
host = '172.20.10.7'
port = 50020

s.connect((host,port))

s.sendall(b'Thanks for the connection')
print (s.recv(1024))

while True:
    command = s.recv(1024)
    
    if command == b'ShutOffNow':
        motors.terminate()
    
    
    if command == b'Shoot':
        print('Shooting')
        #commandShoot = s.recv(1024)
        xdist = str(xdist)
        motors = subprocess.Popen(['/home/pi/Desktop/Phoenix-Linux-SocketCAN-Example-master/bin/example', xdist])
        
    if command == b'manParam':
        xdist = s.recv(1024)
        xdist = xdist.decode('utf8')
        xdist = float(xdist)
        print(xdist)
        print(type(xdist))

    if command == b'Calculate':
        print('Calculating')

    if command == b'Shutoff':
        print('Shutting off')
        s.close()
        
    if command == b'NCAABB':
        print('Configuring BSMfor NCAA Basetkball')

    if command == b'FoamBall':
        print('Configuring BSM for Foam Ball')
