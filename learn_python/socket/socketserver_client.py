#! /usr/local/python3/bin/python3
# encoding: utf-8

import socket
import time

host = "127.0.0.1"
port = 9999
bufsize = 1024
addr = (host, port)

while True:
    socketserver_client_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketserver_client_object.connect(addr)
    data = input(">>   ")
    socketserver_client_object.send(data.encode())
    data = socketserver_client_object.recv(bufsize)
    print(data.decode())
    time.sleep(3)
    data = socketserver_client_object.recv(bufsize)
    print(data.decode())
    
    if not len(data):
        break
    print(data.decode())
    socketserver_client_object.close()
    
