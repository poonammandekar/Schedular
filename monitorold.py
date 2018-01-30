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
print 'I am in moniter'

def schedulerRelaunch():
    schedulerProc=subprocess.Popen(["python","scheduler.py"])
    schedulerId=schedulerProc.pid
    try:
        while True:
            p = schedulerProc.poll()
            if p != None:
#                schedulerRelaunch()
                break
    except Exception:
        import traceback
        print traceback.format_exc()
    finally:
        print 'Scheduler terminated'

def webServerRelaunch():
    webServerProc=subprocess.Popen(["python","webServer1.py"])
    procId=webServerProc.pid
    try:
        while True:
            p = webServerProc.poll()
            if p != None:
#                webServerRelaunch()
                break
    except Exception:
        import traceback
        print traceback.format_exc()
    finally:
        print 'WebServer terminated'

def toggleLaunch():
    toggleProc=subprocess.Popen(["python","togglecase.py"])
    toggleProcId=toggleProc.pid
    try:
        while True:
            p = toggleProc.poll()
            if p != None:
                toggleLaunch()
    except Exception:
        import traceback
        print traceback.format_exc()
    finally:
        print 'toggle process terminated'

def lowerLaunch():
    lowerProc=subprocess.Popen(["python","lowercase.py"])
    lowerProcId=schedulerProc.pid
    try:
        while True:
            p = lowerProc.poll()
            if p != None:
                lowerLaunch()
    except Exception:
        import traceback
        print traceback.format_exc()
    finally:
        print 'lower process terminated'

def upperLaunch():
    upperProc=subprocess.Popen(["python","lowercase.py"])
    upperProcId=schedulerProc.pid
    try:
        while True:
            p = upperProc.poll()
            if p != None:
                upperLaunch()
    except Exception:
        import traceback
        print traceback.format_exc()
    finally:
        print 'upper process terminated'


if(os.fork()==0):
    schedulerRelaunch()
    exit(0);
time.sleep(2)

if(os.fork()==0):
    webServerRelaunch()
    exit(0);
time.sleep(2)

if(os.fork()==0):
    toggleLaunch()
    exit(0);
time.sleep(2)

if(os.fork()==0):
    lowerLaunch()
    exit(0);
time.sleep(2)

if(os.fork()==0):
    upperLaunch()
    exit(0);


