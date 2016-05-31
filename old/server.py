#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from pygame import mixer
import serial, threading, random, time

arduinoBodyName = '/dev/ardBody2'
aBNbaudrate = 115200
play = 0
file = 0
try:
    port = serial.Serial(arduinoBodyName, baudrate=aBNbaudrate, dsrdtr = 1,  timeout=3.0)
except:
    print "> Not found " + arduinoBodyName
    port = ""
    exit()


sock = socket.socket()
sock.bind(('', 6526))
sock.listen(1)
conn, addr = sock.accept()
sock.settimeout(2)

def soundPlayer(arg3, soundPlayer_stop):
    global file
    while 1:
        global play
        mixer.init(16000, -16, 1, 2048)

        if play == 1:
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
soundPlayer=threading.Thread(target=soundPlayer, args=(2, soundPlayer_stop))
if port != "":
    soundPlayer.start()

def simplePlay(file):
    mixer.init(16000, -16, 1, 2048)
    mixer.music.load("/home/pi/r2d2/sound/"+file+".MP3")
    mixer.music.play()
    while mixer.music.get_busy() == True:
            continue
simplePlay("ready")
print "> OK. Start!"

print '> Connected:', addr
def sendDataRobot(data):
    pass
def dataHandler(data):
    pass
def reStart():
    global conn, addr
    port.write("S\n")
    conn.close()
    conn, addr = sock.accept()

while True:
    data = conn.recv(1024)
    if data == u'end':
        break
    if not data:
        print '> RESTART'
        reStart()
    print data

    if data == 'PLAYsound' and play == 0:
        print "> Play sound"
        file = random.randint(0, 10)
        play=1                       #On playing

    if data == 'STOPsound':
        print "> Stop sound"
        play = 0

    if data != 'PLAYsound' and data != 'STOPsound':
        port.write(data + "\n")

port.write("S\n")
conn.close()
