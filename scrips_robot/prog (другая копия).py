#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from pygame import mixer
import serial, threading, random
import subprocess
import sys, os
child = os.path.join(os.path.dirname(__file__), "/home/pi/r2d2/sound.py")
word  = 'word'
file = ['/home/pi/r2d2/prog.py','/home/pi/r2d2/sound.py']

pipes = []

arduinoBodyName =  '/dev/ttyACM0' #'/dev/ardBody'
aBNbaudrate = 115200
play = 0
file = 0
try:
    port = serial.Serial(arduinoBodyName, baudrate=aBNbaudrate, dsrdtr = 1,  timeout=3.0)
except:
    print "> Not found " + arduinoBodyName
    port = ""
    exit()


#sock = socket.socket()
#sock.bind(('', 6518))
#sock.listen(1)
#conn, addr = sock.accept()
#sock.settimeout(.01)

def soundPlayer(arg3, soundPlayer_stop):
    mixer.init(16000, -16, 1, 2048)
    file = random.randint(0, 10)
    mixer.music.load("/home/pi/r2d2/sound/"+str(file)+".MP3")
    mixer.music.play()
    while mixer.music.get_busy() == True and not soundPlayer_stop.is_set():
        if play==0:
            mixer.music.stop()
        continue


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

#print '> Connected:', addr
def sendDataRobot(data):
    pass
def dataHandler(data):
    pass
def reStart():
    #global conn, addr
    port.write("S\n")
    #conn.close()
    #conn, addr = sock.accept()
def ttsFunction(text):
    cmd =  'espeak -vru -s120 "%s" 2>>/dev/null' % text
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
data = ''

command = [sys.executable, child]
#pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
#pipes.append(pipe)
while True:
    #data = conn.recv(512)
    line = readlineCR(port)
    #line = port.read()
    #line = ""
    print line
    if  "V" in line:
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
	pipe.stdin.write(u"play\n")

    elif "S" in line:
        pipe.kill()             #Stop playing

    '''
    if dataIn != '\n':
        data += dataIn
    else:
        data = ''
    '''
    if data == u'end':
        break
    if not data:
        print '> RESTART'
        reStart()
    print data
    

    if 'SAY|' in data:
        print '--------------------------------------------'
        tts = data.split('|')[-1]
        print '--------------------------------------------' + tts
        ttsFunction(tts)

    if data != ('PLAYsound' and 'STOPsound') and 'SAY|' not in data:
        port.write(data + "\n")

port.write("S\n")
#conn.close()
