# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
version = 1.0

class CamBuff(QtCore.QThread):
    #arrayImg = QtCore.pyqtSignal(QtCore.QImage)#np.ndarray)
    def __init__(self, sock):
        QtCore.QThread.__init__(self)
        self.sock = sock

    def __del__(self):
        self.wait()

    def run(self, sendData):
        while True:
            self.sock.send(sendData)

class MoveWidget(QtCore.QObject): #MoveWidget
    def __init__(self, sock):
        self.sock = sock
        self.Name = 'Move'

    def getWidget(self):
            #elf.webCam = QtWebKit.QWebView()
            #self.webCam.setUrl(QtCore.QUrl('http://195.235.198.107:3344/axis-cgi/mjpg/video.cgi?resolution=320x240'))

            self.emptyLabel = QtGui.QLabel()
            self.emptyLabel.setMinimumHeight(40)
            self.emptyLabel.setMinimumWidth(40)

            self.up = QtGui.QPushButton('UP')
            self.up.setMinimumHeight(40)
            self.up.setMinimumWidth(40)
            self.up.setMaximumHeight(55)
            self.up.setMaximumWidth(55)
            self.up.pressed.connect(self.upMove)
            self.up.released.connect(self.stopMove)


            self.left = QtGui.QPushButton('L')
            self.left.setMinimumHeight(40)
            self.left.setMinimumWidth(40)
            self.left.setMaximumHeight(55)
            self.left.setMaximumWidth(55)
            self.left.pressed.connect(self.leftMove)
            self.left.released.connect(self.stopMove)


            self.down = QtGui.QPushButton('DW')
            self.down.setMinimumHeight(40)
            self.down.setMinimumWidth(40)
            self.down.setMaximumHeight(55)
            self.down.setMaximumWidth(55)
            self.down.pressed.connect(self.dwMove)
            self.down.released.connect(self.stopMove)


            self.right = QtGui.QPushButton('R')
            self.right.setMinimumHeight(40)
            self.right.setMinimumWidth(40)
            self.right.setMaximumHeight(55)
            self.right.setMaximumWidth(55)
            self.right.pressed.connect(self.rightMove)
            self.right.released.connect(self.stopMove)

            #self.right.installEventFilter(self.parent)


            self.speed = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.speed.setMaximum(255)
            self.speed.setMinimumWidth(150)

            #self.delButton.setMaximumWidth(55)


            self.gridLayout = QtGui.QGridLayout()
            self.gridLayout.setSpacing(1)

            self.gridLayout.addWidget(self.emptyLabel, 0, 0)
            self.gridLayout.addWidget(self.up, 0, 1)
            #self.gridLayout.addWidget(self.emptyLabel, 0, )
            self.gridLayout.addWidget(self.left, 1, 0)
            self.gridLayout.addWidget(self.down, 1, 1)
            self.gridLayout.addWidget(self.right, 1, 2)
            self.gridLayout.addWidget(self.speed, 2,0, 2,3)
            #self.servoGrid.addWidget(self.pin, 3, 4)

            widget = QtGui.QWidget()
            widget.setLayout(self.gridLayout)
            #self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_W), self), QtCore.SIGNAL('activated()'), self.tx)

            return widget




    def tx(self):
        print 'asd'

    def upMove(self):

        data = 'F\n'
        if self.sock != '':
            self.sock.send(data)



    def dwMove(self):
        data = 'B\n'
        if self.sock != '':
            self.sock.send(data)
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def leftMove(self):
        data = 'R\n' #L
        if self.sock != '':
            self.sock.send(data)

    def rightMove(self):
        data = 'L\n' #R
        if self.sock != '':
            self.sock.send(data)

    def stopMove(self):
        data = 'S\n'
        if self.sock != '':
            self.sock.send(data)




    def getName(self):
        return self.Name