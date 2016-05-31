#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame import mixer
import threading, random, socket
import serial

play = 0
file = 0
arduinoBodyName = '/dev/ardBody'
aBNbaudrate = 9600
try:
    port = serial.Serial(arduinoBodyName, baudrate=aBNbaudrate, dsrdtr = 1,  timeout=3.0)
except:
    print "Not found " + arduinoBodyName
    port = ""
    exit()

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

sock = socket.socket()
sock.bind(('', 6003))
sock.listen(1)
conn, addr = sock.accept()
#sock.settimeout(.01)

def soundPlayer(arg3, soundPlayer_stop):
    global file
    global play
    while 1:
        if play == 1:

            mixer.init(16000, -16, 1, 2048)
            mixer.music.load("/home/pi/r2d2/sound/"+str(file)+".MP3")
            print file
            mixer.music.play()
            while mixer.music.get_busy() == True:
                if play==0:
                    mixer.music.stop()
                continue
            file = random.randint(0, 10) #Random sound
            #play = 0



soundPlayer_stop = threading.Event()
#soundPlayer=threading.Thread(target=soundPlayer)
soundPlayer=threading.Thread(target=soundPlayer, args=(2, soundPlayer_stop))
soundPlayer.start()

def simplePlay(file):
    mixer.init(16000, -16, 1, 2048)
    mixer.music.load("/home/pi/r2d2/sound/"+file+".MP3")
    mixer.music.play()
    while mixer.music.get_busy() == True:
            continue
#simplePlay("ready")
print "> OK. Start!"

print '> Connected:', addr
def reStart():
    global conn, addr
    conn.close()
    conn, addr = sock.accept()

while True:
    data = conn.recv(16384)
    #data = raw_input()
                     #Stop playing

    if not data:
        print '> RESTART'
        reStart()
    print data
    if data == 'PLAYsound' and play == 0:
        print "> Play sound"
        file = str(random.randint(0, 10))
        play=1                       #On playing

    if data == 'STOPsound':
        print "> Stop sound"
        play = 0


conn.close()
