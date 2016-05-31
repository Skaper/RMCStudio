#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, serial, random

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
sock.bind(('', 6666))
sock.listen(1)
conn, addr = sock.accept()
#sock.settimeout(.01)

def reStart():
    global conn, addr
    #port.write("S\n")
    conn.close()
    conn, addr = sock.accept()


while True:
    data = conn.recv(16384)
    print data
    if data == u'end':
        break
    if not data:
        print '> RESTART'
        reStart()
    if data == 'PLAYsound' and play == 0:
        print "> Play sound"
        file = random.randint(0, 10)
        play=1                       #On playing

    if data == 'STOPsound':
        print "> Stop sound"
        play = 0

    if 'SAY|' in data:
        print '--------------------------------------------'
        tts = data.split('|')[-1]
        print '--------------------------------------------' + tts
        ttsFunction(tts)

    if data != ('PLAYsound' and 'STOPsound') and 'SAY|' not in data:
        port.write(data + "\n")
