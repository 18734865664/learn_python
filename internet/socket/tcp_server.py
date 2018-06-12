#! /usr/local/python3/bin/python3
# encoding: utf8

import subprocess
import socket


host = subprocess.getoutput("ip addr|grep global|grep brd|awk '{match($0, /(([0-9]{1,3}\.){3}[0-9]{1,3})/, S); print S[0]}'")
# import pdb; pdb.set_trace()
port = 8888
bufsize = 3

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((host, port))
tcp_server_socket.listen(1)

while True:
    print("wait for connection....")
    tcp_client_obj, addr = tcp_server_socket.accept()
    print("connect from: ", addr)
    while True:
        data = tcp_client_obj.recv(bufsize)
        print(data)
        if data.decode("utf-8") == "EOF":
            break
        #data = "recive your message: " + data.decode("utf-8")
        tcp_client_obj.sendall(data)
    tcp_client_obj.send("EOF".encode("utf-8"))
    tcp_client_obj.close()
tcp_server_socket.close()
