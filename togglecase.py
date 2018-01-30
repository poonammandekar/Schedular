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
port = 2495
lineCount=1
lineStart=1

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
# Create a TCP/IP socket                                              
toggleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

toggleSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
toggleSocket.bind((IP,port))
#toggleLog.write("101  Binding success : Binding Done to scheduler port for upper case...\n")                                                  
#toggleLog.flush()                                                                                                                    
#toggleLog.write("102  Listening for upper case socket...\n")                                            
#toggleLog.flush()
# if toggleSocket == -1:
#         toggleLog.write("501 socket creation failed : socket error in nextNo\n")
#         toggleLog.flush()
toggleSocket.listen(3)
(connection,(IP,port))=toggleSocket.accept()
inputData=connection.recv(10024)
print "data in toggle=",inputData
if inputData:
        arglist = inputData.split(" ")
        length=len(arglist)
        toggleLog= open(arglist[0],"a")
        delay1= arglist[1]
        delay=int(delay1)

lastLine = subprocess.check_output(['tail', '-1', arglist[0]])
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
                        if i.isupper():
                                name_list.append(i.lower())
                        elif i.islower():
                                name_list.append(i.upper())
                        else:
                                name_list.append(i)

                data=''.join(name_list)
                time.sleep(delay)
                connection.send(data)
                toggleLog.write(str(lineCount)+' : executing sucessFully : '+data)
                toggleLog.flush()
        
finally:
        toggleLog.write("505 connection close : Connection close from toggle to scheduler\n")
        toggleLog.flush()
        toggleLog.close()
        toggleSocket.close()
