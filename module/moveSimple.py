# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

version = 1.0
class MoveSimpleWidget(QtCore.QObject): #MoveSimpleWidget
    def __init__(self, sock):
        self.sock = sock
        self.Name = 'Move Simple'

    def getWidget(self):
            #elf.webCam = QtWebKit.QWebView()
            #self.webCam.setUrl(QtCore.QUrl('http://195.235.198.107:3344/axis-cgi/mjpg/video.cgi?resolution=320x240'))

            self.emptyLabel = QtGui.QLabel()
            self.emptyLabel.setMinimumHeight(40)
            self.emptyLabel.setMinimumWidth(40)


            self.left = QtGui.QPushButton('L')
            self.left.setMinimumHeight(40)
            self.left.setMinimumWidth(40)
            self.left.setMaximumHeight(55)
            self.left.setMaximumWidth(55)
            self.left.pressed.connect(self.leftMove)
            self.left.released.connect(self.stopMove)


            self.right = QtGui.QPushButton('R')
            self.right.setMinimumHeight(40)
            self.right.setMinimumWidth(40)
            self.right.setMaximumHeight(55)
            self.right.setMaximumWidth(55)
            self.right.pressed.connect(self.rightMove)
            self.right.released.connect(self.stopMove)

            self.speed = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.speed.setMaximum(255)
            #self.speed.setMinimumWidth(150)

            #self.delButton.setMaximumWidth(55)


            self.gridLayout = QtGui.QGridLayout()
            self.gridLayout.setSpacing(1)

            #self.gridLayout.addWidget(self.emptyLabel, 0, 0)
            #self.gridLayout.addWidget(self.up, 0, 1)
            #self.gridLayout.addWidget(self.emptyLabel, 0, )
            self.gridLayout.addWidget(self.left, 0, 0)
            #self.gridLayout.addWidget(self.down, 1, 1)
            self.gridLayout.addWidget(self.right, 0, 1)
            self.gridLayout.addWidget(self.speed, 1,0, 1,2)
            #self.servoGrid.addWidget(self.pin, 3, 4)

            widget = QtGui.QWidget()
            widget.setLayout(self.gridLayout)

            return widget
    def stopMove(self):
        data = str(3)
        print data
        if self.sock != '':
            self.sock.send(data)

    def leftMove(self):
        data = str(0)
        if self.sock != '':
            self.sock.send(data)

    def rightMove(self):
        data = str(9)
        if self.sock != '':
            self.sock.send(data)


    def getName(self):
        return self.Name

