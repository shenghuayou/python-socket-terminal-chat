#!/usr/bin/env python
 
import socket
from threading import Thread
import sys
 
 #basic socket setup for client
TCP_IP = 'localhost'
TCP_PORT = 6666
BUFFER_SIZE = 1024
username = input('username:')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def recv():
    while 1:
        data = s.recv(BUFFER_SIZE)
        if data:
        	print (data.decode('utf-8'))

Thread(target=recv).start()

while 1:
	input_message = input('')
	MESSAGE = ('%s:%s' % (username,input_message))
	s.send(MESSAGE.encode('utf-8'))
	

s.close()