#!/usr/bin/env python

import select
import socket
import sys
import pymysql
import time

def store_message(info):
    # connect to database and store data
    db = pymysql.connect("host","user","pass","db" )
    cursor = db.cursor()
    cursor.execute("insert into history(message) values (%s);", info)
    db.commit()
    db.close()

def read_message():
    # connect to database and retrieve data
    return_list=[]
    db = pymysql.connect("host","user","pass","db" )
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
    

# basic socket setup for server
host = 'localhost' 
backlog = 5 
BUFFER_SIZE = 1024 
port = 6666
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(backlog) 
input = [server,] # list of connection

# dict for client and username
client_username_dict = {}

print ('server is up, waiting for connections')
while 1: 
  inputready,outputready,exceptready = select.select(input,[],[]) 

  for s in inputready: #check each socket that select() said has available data
    if s == server: #if select returns our server socket, there is a new 
                    #remote socket trying to connect
      client, address = server.accept() 
      input.append(client) #add it to the socket list 
      print ('New client: %s'%str(address))

      #decode username from client, and add it to dictionary
      username_data = client.recv(BUFFER_SIZE)
      decoded_username_data = username_data.decode('utf-8')
      client_username_dict[client] = decoded_username_data

      # tell connected client that a new client connects to server
      enter_data ="---------------" + str(decoded_username_data) + " enter the room" + "---------------"
      encode_enter_data = enter_data.encode('utf-8')
      broadcast(server,client,encode_enter_data)

      # send chat history to a new client
      history_list = read_message()
      for i in history_list:
        client.send(i.encode('utf-8'))
        time.sleep(0.01)

    else: 
      # select has indicated that these sockets have data available to recv
      data = s.recv(BUFFER_SIZE) 
      if data:
        decode_data = str(data.decode('utf-8'))
        store_message(decode_data)
        broadcast(server, s, data)
      else:
        #send out message when a client left 
        left_user = client_username_dict[s]
        left_data = "---------------" + str(left_user) + " left the room" + "---------------" 
        broadcast(server,s,left_data.encode('utf-8'))

        # remove this client from dictionary and socket list
        del client_username_dict[s]
        s.close() 
        input.remove(s) 

server.close()