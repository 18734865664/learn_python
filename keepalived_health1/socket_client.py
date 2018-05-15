#!/usr/bin/python
# coding: utf8


import socket
s = socket.socket()
host = '10.100.146.178'
port =  12345

s.connect((host,port))

print s.recv(1024)
s.close()
