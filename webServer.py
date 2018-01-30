#!/usr/bin/env python
import socket
import select
import sys
import os
import signal
import subprocess
from multiprocessing import Process
import random
import time, re
import thread

webServerLog=open("webServer.log","a")
print 'I am in webserver'
class WebServer:
    def __init__(self):
#        self.port = 8222
        self.port1 = 2595
        self.host = (socket.gethostname())
        self.IP = socket.gethostbyname(self.host)
        self.size = 1025 #size for revieve data through socket
               
    def newProcess(self,connection,schedulerSock):
        data = connection.recv(self.size)
        webServerLog.write("Rreceived from UI "+ data +'\n')
        webServerLog.flush()
        print "data in web= ",data
        try:
            schedulerSock.send(data)
            webServerLog.write("Data send to scheduler "+ data +'\n')
            webServerLog.flush()
            while True:
                dataRecv=schedulerSock.recv(self.size)
                webServerLog.write("Received from scheduler "+ dataRecv +'\n')
                webServerLog.flush()
                if not dataRecv:
                    return
                connection.send(dataRecv)            
        finally:
            print 'WebServer terminated'

    def run(self):
        #Create a TCP/IP socket
        port=int(sys.argv[1])
        print 'Port=',port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.sock == -1:
            webServerLog.write("501  socket creation failed : socket error in webServer for UI...\n")
            webServerLog.flush()
            self.sock.close()
            sys.exit(1)
        # Bind the socket to the port
        serverAddress = (self.IP, port)
        self.sock.bind(serverAddress)
        webServerLog.write("101  Binding success : Binding Done to webServer port for UI...\n")
        webServerLog.flush()
        # Listen for incoming connections
        self.sock.listen(3)
        webServerLog.write("102  Listening for UI...\n")
        webServerLog.flush()

        self.schedulerSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if self.schedulerSock == -1:
            webServerLog.write("501  socket creation failed : socket error in webServer for scheduler...\n")
            webServerLog.flush()

        serverAddress = (self.IP, self.port1)
        self.schedulerSock.connect(serverAddress)

        webServerLog.write("101  Socket Created Successfully : Binding Done to webServer port for scheduler...\n")
        webServerLog.flush()

        while True:
            (connection,(IP,port))=self.sock.accept()
            try:
                thread.start_new_thread( self.newProcess,( connection , self.schedulerSock ) )
            except:
                webServerLog.write("404  Error: unable to start thread... \n")
                webServerLog.flush()

if __name__ == "__main__":
    s = WebServer()
    s.run()
