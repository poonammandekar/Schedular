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
port = 2295
lineCount=1
lineStart=1

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
# Create a TCP/IP socket                                              
upperSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
upperSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
upperSocket.bind((IP,port))
#upperLog.write("101  Binding success : Binding Done to scheduler port for upper case...\n")                                                  
#upperLog.flush()                                                                                                                            
#upperLog.write("102  Listening for upper case socket...\n")                                                                                  
#upperLog.flush()   
# if upperSocket == -1:
#         upperLog.write("501 socket creation failed : socket error in uppercase\n")
#         upperLog.flush()
upperSocket.listen(3)
(connection,(IP,port))=upperSocket.accept()
inputData=connection.recv(10024)
print "data in upper=",inputData
if inputData:
        arglist = inputData.split(" ")
        length=len(arglist)
        upperLog= open(arglist[0],"a")
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
        for line in arglist[2:length]:
                name_list = []
                for i in line:
                        if i.islower():
                                name_list.append(i.upper())
                        else:
                                name_list.append(i)

                data=''.join(name_list)
                
                time.sleep(delay)
                connection.send(data)
                upperLog.write(str(lineCount)+' : executing sucessFully : '+data)
                upperLog.flush()
        
finally:
        upperLog.write("505 connection close : Connection close from uppercase to scheduler\n")
        upperLog.flush()
        upperLog.close()
        upperSocket.close()
