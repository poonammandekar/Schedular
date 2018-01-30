#!/usr/bin/env python
import socket
import sys
import os
import subprocess
from multiprocessing import Process
import random
import time, re


host= (socket.gethostname())
IP = socket.gethostbyname(host)
port=int(sys.argv[5])
print 'Port in Ui=',port
# Create a TCP/IP socket
UISocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
serverAddress = (IP, port)
print >>sys.stderr, 'connecting to %s port %s' % serverAddress
UISocket.connect(serverAddress)

try:
    if len(sys.argv) == 6:
        inputFile = sys.argv[1]
        username= sys.argv[2]
        case= sys.argv[3]
        delay = sys.argv[4]
        f= open(inputFile,"r") #opens file"
        arglist1=username+" "+case+" "+" "+delay
        arglist=""
        for line in f:
            arglist=arglist+line
        data=arglist1+" "+arglist
        print 'data ',data
        UISocket.send(data)        
        while True:
            outputData = UISocket.recv(1024)
            print outputData
    
    else:
        print >>sys.stderr,'Invalid arguments count'
      
finally:
    print >>sys.stderr,'UI socket close...'
    UISocket.close()
