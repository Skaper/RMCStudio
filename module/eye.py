__author__ = 'skaper'
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import os
version = 1.0

class Data(QtCore.QThread):
    #arrayImg = QtCore.pyqtSignal(QtCore.QImage)#np.ndarray)
    def __init__(self, sock):
        QtCore.QThread.__init__(self)
        self.sock = sock

    def __del__(self):
        self.wait()

    def run(self, sendData):
        while True:
            self.sock.send(sendData)

class EyeWidget(QtCore.QObject): #MoveWidget
    def __init__(self, sock):
        self.sock = sock
        self.Name = 'Eye'

    def getWidget(self):
            self.gridLayout = QtGui.QGridLayout()
            self.gridLayout.setSpacing(1)
            f = QtGui.QPushButton()
            #f.text
            size = 0
            allFiles = os.listdir('emotion')
            files1 = filter(lambda x: x.endswith('.gif'), allFiles)
            print files1
            files = sorted(files1, key = lambda x: os.path.getctime('emotion'))
            self.labels = []
            print files
            self.buttons = []
            labelsButton = 0
            couter = 0

            for i, fileName in enumerate(files1):
                if labelsButton < 7:
                    self.labels.append(QtGui.QLabel())

                    self.gridLayout.addWidget(self.labels[i], 0, couter)
                    self.buttons.append(QtGui.QPushButton(fileName.rstrip('.gif')))
                    self.gridLayout.addWidget(self.buttons[i], 1, couter)
                else:

                    self.labels.append(QtGui.QLabel('1'))
                    self.gridLayout.addWidget(self.labels[i], 2, couter)
                    self.buttons.append(QtGui.QPushButton(fileName.rstrip('.gif')))
                    self.gridLayout.addWidget(self.buttons[i], 3, couter)
                labelsButton +=1
                self.buttons[i].clicked.connect(self.eyeEmotion)
                #self.connect(self.buttons[i], QtCore.SIGNAL('clicked()'), QtCore.SLOT('QString()')) #+fileName.rstrip('.gif')+"')"))
                couter +=1
                if couter == 7:
                    couter = 0

                #QtCore.QString('')




            widget = QtGui.QWidget()
            widget.setLayout(self.gridLayout)

            return widget


    def eyeEmotion(self, sd):

        #print self.sender()
        print sd

