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

monitorLog=open("monitor.log","a")
configFile=open("config","r")
print 'I am in moniter'

i=0 
processList = ['lowercase.py','uppercase.py','togglecase.py','scheduler.py']
noOfProcess=len(processList) #no of process to launch
def processLaunch(processName):
    process=subprocess.Popen(["python",processName])
    processId=process.pid
    print processName + ' created'
    try:
        while True:
            p = process.poll()
            if p != None:
               #processLaunch()
               break
    except Exception:
        import traceback
        print traceback.format_exc()
    finally:
        print processName+' terminated'

while i < noOfProcess:
    if(os.fork()==0):
        processLaunch(processList[i])
        exit(0);
    time.sleep(1)
    i=i+1

time.sleep(3)
for port in configFile:
    if(os.fork()==0):
        process=subprocess.Popen(["python","webServer.py",port])
        processId=process.pid
        print 'WebServer created'
        try:
            while True:
                p = process.poll()
                if p != None:
                    #processLaunch()
                    break
        except Exception:
            import traceback
            print traceback.format_exc()
        finally:
            print 'Webserver terminated'
        exit(0)
