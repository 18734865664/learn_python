#! /usr/local/python3/bin/python3
# encoding: utf8

import subprocess
import socket

# 定义变量
HOST = subprocess.getoutput("ip addr |grep globa|grep brd|awk   '{match($0, /(([0-9]{1,3}\.){3}[0-9]{1,3})/, S); print S[1]}'")
PORT = 9999
BUFSIZE = 5

# 绑定socket
UDP_SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_SERVER_SOCKET.bind((HOST, PORT)) 


# 循环接收信息

while True:
    print("waiting for message...")
    DATA, ADDR = UDP_SERVER_SOCKET.recvfrom(BUFSIZE)
    DATA = "接收到信息是：{}".format(DATA)
    print(DATA)
    if not DATA:
        break
    DATA = "接收到信息: {} \n来自：{}".format(DATA, ADDR)
    UDP_SERVER_SOCKET.sendto(DATA.encode("utf-8"), ADDR)
    print("...received from and returned to :", ADDR)
UDP_SERVER_SOCKET.close()
