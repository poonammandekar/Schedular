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

schedulerLog=open("scheduler.log","a")
print 'I am in scheduler'
class Scheduler:
    def __init__(self):
        self.port = 2595
        self.port1 = 2495
        self.port2 = 2395
        self.port3 = 2295
        self.host = (socket.gethostname())
        self.IP = socket.gethostbyname(self.host)
        self.size = 1025 #size for revieve data through socket
        self.count = 0 #to create distinct Logfile name

    def newProcess(self,connection,toggleSock,lowerSock,upperSock,count):
        while True:
            data = connection.recv(self.size)
            schedulerLog.write(" Received from webserver "+ data +'\n')
            schedulerLog.flush()
            if data:
                arglist = data.split(" ")
                #print 'arglist=',arglist
                length=len(arglist)
                #print 'length=',length
                username= arglist[0]
                case= arglist[1]
                delay = arglist[2]
                print "case = ",case
                inputData=" ".join(str(x) for x in arglist[2:length])
                print "d=",inputData
            filename=case+str(count)+'.log'
            inputData=filename+inputData
            print 'inputData in scheduler='+inputData
            def relaunch(case):
                if(case == 'toggle'):
                    toggleSock.connect((self.IP,self.port1))
                    try:
                        # handle the server socket
                        #                    (conn,(self.IP,self.port1)) = toggleSock.accept()
                        #                    schedulerLog.write("102  Connection Accepted from toggle...\n")
                        #                    schedulerLog.flush()
                        toggleSock.send(inputData)
                        schedulerLog.write(" Sending to the toggle process... "+inputData +'\n')
                        schedulerLog.flush()
                        # Receive the data
                        while True:
                            procData = toggleSock.recv(self.size)
                            schedulerLog.write("Data get from toggle... "+procData)
                            schedulerLog.flush()
                            if not procData:
                                return
                            connection.send(procData)
                    except Exception:
                        import traceback
                        print traceback.format_exc()
                    finally:
                        print 'Toggle Case User work completed'

                if(case == 'lower'):
                    lowerSock.connect((self.IP,self.port2))
                    try:
                        # handle the server socket
                        # (conn1,(self.IP,self.port2)) = lowerSock.accept()
                        # schedulerLog.write("102  Connection Accepted from lower...\n")
                        # schedulerLog.flush()
                        lowerSock.send(inputData)
                        schedulerLog.write(" Sending to the lower process... "+inputData + '\n')
                        schedulerLog.flush()
                        # Receive the data
                        while True:
                            procData1 = lowerSock.recv(self.size)
                            schedulerLog.write("Data get from lower...\n"+procData1)
                            schedulerLog.flush()
                            if not procData1:
                                return
                            connection.send(procData1)
                    except Exception:
                        import traceback
                        print traceback.format_exc()
                    finally:
                        print 'Lower Case User work completed'

                if(case == 'upper'):
                    upperSock.connect((self.IP,self.port3))
                    try:
                        # handle the server socket
                        # (conn2,(self.IP,self.port3)) = upperSock.accept()
                        # schedulerLog.write("102  Connection Accepted from lower...\n")
                        # schedulerLog.flush()
                        upperSock.send(inputData)
                        schedulerLog.write(" sending to the upper process... "+inputData+'\n' )
                        schedulerLog.flush()
                        # Receive the data
                        while True:
                            procData2 = upperSock.recv(self.size)
                            schedulerLog.write("Data get from upper...\n"+procData2)
                            schedulerLog.flush()
                            if not procData2:
                                return
                            connection.send(procData2)
                    except Exception:
                        import traceback
                        print traceback.format_exc()
                    finally:
                        print 'Upper Case User work completed'
                        
            relaunch(case)
    
    def run(self):
        #Create a TCP/IP socket
        self.webServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.webServerSock == -1:
            schedulerLog.write("501  socket creation failed : socket error in scheduler for webSever...\n")
            schedulerLog.flush()
            self.webServerSock.close()
            sys.exit(1)
        # Bind the socket to the port
        serverAddress = (self.IP, self.port)
        self.webServerSock.bind(serverAddress)
        schedulerLog.write("101  Binding success : Binding Done to sheduler port for webServer...\n")
        schedulerLog.flush()
        # Listen for incoming connections
        self.webServerSock.listen(3)
        schedulerLog.write("102  Listening for webServer...\n")
        schedulerLog.flush()


        self.toggleSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if self.toggleSock == -1:
            schedulerLog.write("501  socket creation failed : socket error in scheduler for toggle...\n")
            schedulerLog.flush()
        # self.toggleSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.toggleSock.bind((self.IP,self.port1))
        # schedulerLog.write("101  Binding success : Binding Done to scheduler port for toggle...\n")
        # schedulerLog.flush()
        # schedulerLog.write("102  Listening for toggle case socket...\n")
        # schedulerLog.flush()

        self.lowerSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if self.lowerSock == -1:
            schedulerLog.write("501  socket creation failed : socket error in scheduler for lower case...\n")
            schedulerLog.flush()
        # self.lowerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.lowerSock.bind((self.IP,self.port2))
        # schedulerLog.write("101  Binding success : Binding Done to scheduler port for upper case...\n")
        # schedulerLog.flush()
        # schedulerLog.write("102  Listening for upper case socket...\n")
        # schedulerLog.flush()

        self.upperSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if self.upperSock == -1:
            schedulerLog.write("501  socket creation failed : socket error in scheduler for upper case...\n")
            schedulerLog.flush()
        # self.upperSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.upperSock.bind((self.IP,self.port3))
        # schedulerLog.write("101  Binding success : Binding Done to scheduler port for uppercase...\n")
        # schedulerLog.flush()
        # schedulerLog.write("102  Listening for lower case socket...\n")
        # schedulerLog.flush()


        while True:
            (connection,(IP,port))=self.webServerSock.accept()
            self.count = self.count + 1
            try:
                thread.start_new_thread(self.newProcess,(connection,self.toggleSock,self.lowerSock,self.upperSock,self.count))
            except:
                schedulerLog.write("404  Error: unable to start thread... \n")
                schedulerLog.flush()



if __name__ == "__main__":
    s = Scheduler()
    s.run()
