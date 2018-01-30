#!/usr/bin/env python
import socket
import sys
import os
import subprocess
from multiprocessing import Process
import random
import time, re

host = (socket.gethostname())
IP = socket.gethostbyname(host)
port = 2395
lineCount=1
lineStart=1

# Create a TCP/IP socket                                              
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

lowerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lowerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                                                  
lowerSocket.bind((IP,port))                                                                                             
#lowerLog.write("101  Binding success : Binding Done to scheduler port for upper case...\n")                                       
        # lowlerLog.flush()                                                                                                                 
        # lowlerLog.write("102  Listening for upper case socket...\n")                                                                      
        # lowlerLog.flush()  
    
# if lowerSocket == -1:
#         lowerLog.write("501 socket creation failed : socket error in lowerCase\n")
#         lowerLog.flush()
lowerSocket.listen(3)
(connection,(IP,port))=lowerSocket.accept()
inputData=connection.recv(10024)
print "data in lower=",inputData
if inputData:
        arglist = inputData.split(" ")
        length=len(arglist)
        lowerLog= open(arglist[0],"a")
        delay1= arglist[1]
        delay=int(delay1)

lastLine = subprocess.check_output(['tail', '-1',arglist[0]])
print lastLine
if lastLine:
        token = lastLine.split(" ")
        if(token[2] == 'executing'):
                if(token[3] == 'sucessFully'):
                        lineCount = int(token[0])+1
try:
        #while(lineStart<lineCount):
        for line in arglist[2:length]:
                name_list = []
                for i in line:
                        if i.isupper():
                                name_list.append(i.lower())
                        else:
                                name_list.append(i)

                data=''.join(name_list)
                time.sleep(delay)
                connection.send(data)
                lowerLog.write(str(lineCount)+' : executing sucessFully : '+data)
                lowerLog.flush()
                #lineCount=lineCount+1
        
finally:
        lowerLog.write("505 connection close : Connection close from lowerCase to scheduler\n")
        lowerLog.flush()
        lowerLog.close()
        lowerSocket.close()
