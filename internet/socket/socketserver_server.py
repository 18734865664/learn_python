#! /usr/local/python3/bin/python3
# encoding:utf-8

#from socketserver import TCPServer as TCP
#from socketserver import StreamRequestHandler as SRH
#
# import subprocess
# 
# host = ""
# port = 9999
# addr = (host, port)
# 
# class my_request_handler(SRH):
#     def handle(self):
#         print("connected from : {}".format(self.client_address))
#         data = "recevied all {}".format(self.rfile.readline())
#         data1 = "helloworld"
#         self.wfile.write(data1.encode())
#         print(33333)
#    
# 
# tcpServ = TCP(addr, my_request_handler)
# print("wating for connection....")
# tcpServ.serve_forever()

import socketserver  
from socketserver import StreamRequestHandler as SRH  
from time import ctime  
  
host = ''  
port = 9999  
addr = (host,port)  
  
class Servers(SRH):  
    def handle(self):  
        print('got connection from ',self.client_address)
        data = 'connection %s:%s at %s succeed!' % (host,port,ctime())
        self.wfile.write(data.encode())  
        while True:  
            data1 = self.rfile.readline()
            #import pdb; pdb.set_trace()
            data = self.request.recv(1024)  
            if not data1:   
                break  
            print(data1)
            print("RECV from ", self.client_address[0])
            #import pdb; pdb.set_trace()
            self.request.send(data1)  
            self.wfile.write(data1)
print('server is running....'  )
server = socketserver.ThreadingTCPServer(addr,Servers)  
server.serve_forever() 
