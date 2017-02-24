# python-socket-terminal-chat
*This is a simple real time chat application using python socket and Mysql. The application allow multiple users to chat as a group, and it stores chat history on Mysql database. When new user comes, the user can retrieve chat history from Mysql to know what is going on the group chat.*

## Installation
    $ pip install pymysql

## To get these codes run on your local machine
* setup Mysql database on your local machine
* Fill your info in this line db = **pymysql.connect("host","user","pass","db")** on your **chat_server.py**
* create "history" table on Mysql use this command **create table history (message VARCHAR(100));**

## A demo of chat_client_aws.py
![](https://github.com/shenghuayou/python-socket-terminal-chat/blob/master/chat.gif)
