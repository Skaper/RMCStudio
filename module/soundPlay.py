# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
version = 1.0


class PlaySoundWidget(QtCore.QObject): #MoveWidget
    def __init__(self, sock):
        self.sock2 = sock
        self.Name = 'Play Sound'

    def getWidget(self):
            #elf.webCam = QtWebKit.QWebView()
            #self.webCam.setUrl(QtCore.QUrl('http://195.235.198.107:3344/axis-cgi/mjpg/video.cgi?resolution=320x240'))

            self.emptyLabel = QtGui.QLabel('Sound')
            self.emptyLabel.setMinimumHeight(40)
            self.emptyLabel.setMinimumWidth(40)

            self.up = QtGui.QPushButton('Play')
            self.up.setStyleSheet('''
                                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.67, stop: 0 #22c70d, stop: 1 #116a06);
                                    color:white;
                                    border-radius: 4px;

                                    border: 1px solid #199909;

                                    border-color: rgb(190, 190, 190);''')

            self.statPlay = 'Play'
            self.up.setMinimumHeight(40)
            #self.up.setMinimumWidth(20)
            #self.up.setMaximumHeight(55)
            #self.up.setMaximumWidth(55)
            self.up.clicked.connect(self.playSound)


            #self.delButton.setMaximumWidth(55)


            self.gridLayout = QtGui.QGridLayout()
            self.gridLayout.setSpacing(1)

            self.gridLayout.addWidget(self.emptyLabel, 0, 0)
            self.gridLayout.addWidget(self.up, 0, 1)
            #self.servoGrid.addWidget(self.pin, 3, 4)

            widget = QtGui.QWidget()
            widget.setLayout(self.gridLayout)

            return widget

    def playSound(self):
        if self.statPlay =='Play':
            self.statPlay = 'Stop'
            self.up.setText(self.statPlay)
            data = 'PLAYsound\n'
            print data
            #border-style: outset;
            #background-color: rgb(200, 70, 70);
            #border-width: 2px;

            self.up.setStyleSheet('''
                                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.67, stop: 0 #ff0000, stop: 1 #c84646);
                                    color:white;
                                    border-radius: 4px;

                                    border: 1px solid #199909;

                                    border-color: rgb(190, 190, 190);''')
            if self.sock2 != '':
                self.sock2.send(data)
        else:
            self.statPlay = 'Play'
            self.up.setText(self.statPlay)
            data = 'STOPsound\n'
            print data
            if self.sock2 != '':
                self.sock2.send(data)
            self.up.setStyleSheet('''
                                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.67, stop: 0 #22c70d, stop: 1 #116a06);
                                    color:white;
                                    border-radius: 4px;

                                    border: 1px solid #199909;

                                    border-color: rgb(190, 190, 190);''')





    def getName(self):
        return self.Name