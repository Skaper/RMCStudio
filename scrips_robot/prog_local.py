#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from pygame import mixer
import serial, threading, random
import subprocess
import sys, os
PORTaddres = 6576
BUFF = 1024
child = os.path.join(os.path.dirname(__file__), "/home/pi/r2d2/sound.py")
word  = 'word'
file = ['/home/pi/r2d2/prog.py','/home/pi/r2d2/sound.py']

pipes = []


arduinoBodyName =  '/dev/ttyACM1' #'/dev/ardBody'
aBNbaudrate = 115200
play = 0
file = 0
try:
    port = serial.Serial(arduinoBodyName, baudrate=aBNbaudrate, dsrdtr = 1,  timeout=0.1, writeTimeout=0.3)
except:
    print "> Not found " + arduinoBodyName
    port = ""
    exit()




def soundPlayer(arg3, soundPlayer_stop):
    mixer.init(16000, -16, 1, 2048)
    file = random.randint(0, 10)
    mixer.music.load("/home/pi/r2d2/sound/"+str(file)+".MP3")
    mixer.music.play()
    while mixer.music.get_busy() == True and not soundPlayer_stop.is_set():
        if play==0:
            mixer.music.stop()
        continue





#soundPlayer_stop = threading.Event()
#soundPlayer=threading.Thread(target=soundPlayer)
#soundPlayer_stop = threading.Event()
#soundPlayer=threading.Thread(target=soundPlayer, args=(2, soundPlayer_stop))

def simplePlay(file):
    mixer.init(16000, -16, 1, 2048)
    mixer.music.load("/home/pi/r2d2/sound/"+file+".MP3")
    mixer.music.play()
    while mixer.music.get_busy() == True:
            continue
#simplePlay("ready")
print "> OK. Start!"

#
def sendDataRobot(data):
    pass
def dataHandler(data):
    pass

def ttsFunction(text):
    cmd =  'espeak -vru -s120 "%s" 2>>/dev/null' % text
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
data = ''

command = [sys.executable, child]
#pipe = subprocess.Popen(command, stdin=subprocess.1024PIPE)
#pipes.append(pipe)
def readlineCR(port):
    if port !="":
        rv = ""
        while True:
            ch = port.read()
            if ch=='\r' or ch=='' or ch=='\n':
                return rv
            else:
                rv += ch
    else:
        return ""

def handlerSock(arduino):
    #global data
    sock = socket.socket()
    #sock.setblocking(False)
    sock.bind(('', PORTaddres))
    sock.listen(1)

    conn, addr = sock.accept()
    print '> Connected:', addr
    #sock.settimeout(.1)
    while 1:
        #print 1
        try:
            dataIN = conn.recv(BUFF)
            #print 1
            if '\n' in dataIN and dataIN !='':
                print dataIN
                #data = dataIN
                if len(dataIN)<3:
                    arduino.write(dataIN)
                    print dataIN
                if 'SAY|' in dataIN:
                    print '--------------------------------------------'
                    tts = dataIN.split('|')[-1]
                    print '--------------------------------------------' + tts
                    ttsFunction(tts)
                elif  "PLAYsound" in dataIN:
                    #pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
                    #pipe.stdin.write(u"play\n")
                    print "Start PLAY"
                elif "STOPsound" in dataIN:
                    #pipe.kill()             #Stop playing
                    print "Stop PLAY"

            elif not dataIN:
                print "Restart"
                arduino.write("S\n")
                conn.close()
                conn, addr = sock.accept()
        except:
            print "sock Error"
            pass


def handle_usb_DATA(data):
    #print data
    if data !='':
            print "Data from ARDUINP: " + data
            if  "V" in data:
                #pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
                #pipe.stdin.write(u"play\n")
                print "Start PLAY"
            elif "S" in data:
                #pipe.kill()             #Stop playing
                print "Stop PLAY"
def handlerUsb(arduino):

    #line = port.read()
    #line = ""
    while 1:
        #print 2
        try:
            #line = arduino.readline().decode()
            line = arduino.readline()#.decode()
            #print line
            handle_usb_DATA(line)

        except:
            print "error "
stdout_lck = threading.Lock()

#thread.start_new_thread(handler)
#thread.start_new(handler())
ad = ''
bluetooth_stop = threading.Event()
bluetoothThread=threading.Thread(target=handlerSock, args=(port,))
bluetoothThread.start()

sockThread_stop = threading.Event()
sockThread=threading.Thread(target=handlerUsb, args=(port,))
sockThread.start()




print 'OK Threads run!'
#sockThread_stop = threading.Event()
#soundPlayer=threading.Thread(target=soundPlayer, args=(2, soundPlayer_stop))

    



port.write("S\n")
#conn.close()
