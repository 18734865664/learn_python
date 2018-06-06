#! /usr/local/python3/bin/python3
# encoding: utf-8

import subprocess
import socket
import time


host = subprocess.getoutput("ip addr|grep global|grep brd|awk '{match($0, /(([0-9]{1,3}\.){3}[0-9]{1,3})/, S); print S[0]}'")
ip = 8888
bufsize = 1024
addr = (host, ip)

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(addr)
#tcp_client_socket.setblocking(0)
#tcp_client_socket.settimeout(4)

while True:
    data = input(">>  ")
    if not data:
        break
    tcp_client_socket.send(data.encode("utf-8"))
    tcp_client_socket.send("EOF".encode("utf-8"))

    while True:
        data = tcp_client_socket.recv(bufsize)
        #import pdb; pdb.set_trace()
        if data.decode("utf-8") == "EOF":
            break
        print(data.decode("utf-8"))
tcp_client_socket.close()
    
