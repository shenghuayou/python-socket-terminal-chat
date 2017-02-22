#!/usr/bin/env python

import select
import socket
import sys
import pymysql

def store_message(info):
    #connect to database and perform query
    db = pymysql.connect("host","user","pass","db" )
    cursor = db.cursor()
    cursor.execute("insert into history(message) values (%s);", info)
    db.commit()
    db.close()

def read_message():
    return_list=[]
    db = pymysql.connect("host","user","pass","db" )
    cursor = db.cursor()
    cursor.execute("select * from history")
    result = cursor.fetchall()
    for i in result:
      return_list.append(i)
    db.close()
    print ('result:%s' % result)
    return (i)

def broadcast (server_socket, sock, message):
    for socket in input:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try :
                socket.send(message)
            except :
                socket.close()
                if socket in input:
                    input.remove(socket)
    

#basic socket setup for server
host = 'localhost' 
backlog = 5 
BUFFER_SIZE = 1024 
port = 6666
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(backlog) 
input = [server,] #list of connection

print ('server is up, waiting for connections')
running = 1 #set running to zero to close the server
while running: 
  inputready,outputready,exceptready = select.select(input,[],[]) 

  for s in inputready: #check each socket that select() said has available data
    if s == server: #if select returns our server socket, there is a new 
                    #remote socket trying to connect
      client, address = server.accept() 
      input.append(client) #add it to the socket list so we can check it now
      print ('New client added - id is %s'%str(address))
      #message_from_DB="history"
      #s.send(message_from_DB.encode('utf-8'))

    else: 
      # select has indicated that these sockets have data available to recv
      data = s.recv(BUFFER_SIZE) 
      if data:
        print ('%s received from %s'%(data,s.getsockname()))
        #decode_data = str(data.decode('utf-8'))
        #store_message(decode_data)
        broadcast(server, s, data)
      else: 
        s.close() 
        input.remove(s) 

server.close()