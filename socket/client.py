#! /usr/local/python3/bin/python3
# encoding:utf-8

import subprocess
import socket

# defind variate
host = subprocess.getoutput("ip a |grep globa|grep brd|awk '{match($0, /([0-9]{1,3}\.){3}[0-9]{1,3}/, S); print S[0]}'")
port = 9999
bufsize = 1024

# import pdb; pdb.set_trace()

# bind socket 
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client_socket.connect((host,port))

while True:
    data = input(">>  ").encode("utf-8")
    if not data:
        break
    udp_client_socket.sendto(data, (host, port))
    data, addr = udp_client_socket.recvfrom(bufsize)
    if not data:
        break
    print(data.decode("utf-8"))
udp_client_socket.close()      
   




