#!/usr/bin/env python

import select
import socket
import sys
import pymysql
import time

def store_message(info):
    #connect to database and perform query
    db = pymysql.connect("<host>","<user>","<pass>","<db>")
    cursor = db.cursor()
    cursor.execute("insert into history(message) values (%s);", info)
    db.commit()
    db.close()

def read_message():
    return_list=[]
    db = pymysql.connect("<host>","<user>","<pass>","<db>")
    cursor = db.cursor()
    cursor.execute("select * from history")
    result = cursor.fetchall()
    for i in result:
      return_list.append(i[0])
    db.close()
    return (return_list)

def broadcast (server_socket, sock, message):
    for socket in input:
        # send message to all clients exceot itself
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
      print ('New client: %s'%str(address))
      enter_data = "A client enter the room"
      encode_enter_data = enter_data.encode('utf-8')
      broadcast(server,client,encode_enter_data)
      history_list = read_message()
      for i in history_list:
        client.send(i.encode('utf-8'))
        time.sleep(0.01)
      #broadcast(server,client,message_from_DB.encode('utf-8'))

    else: 
      # select has indicated that these sockets have data available to recv
      data = s.recv(BUFFER_SIZE) 
      if data:
        decode_data = str(data.decode('utf-8'))
        store_message(decode_data)
        broadcast(server, s, data)
      else: 
        left_data = "A client left the room"
        broadcast(server,s,left_data.encode('utf-8'))
        s.close() 
        input.remove(s) 

server.close()