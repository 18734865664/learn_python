#!/usr/bin/python
# coding: utf8
import  socket

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind(('10.100.146.178',12345))
s.listen(5)
while True:
    c, addr = s.accept()
    print '连接地址：',addr
    c.send('欢迎欢迎')
    c.close()
