# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, QtWebKit

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

version = 1.0
class TTSWidget(QtCore.QObject): #MoveSimpleWidget
    def __init__(self, sock):
        self.Name = 'TTS'
        self.sock = sock

    def getWidget(self):
        #elf.webCam = QtWebKit.QWebView()
        #self.webCam.setUrl(QtCore.QUrl('http://195.235.198.107:3344/axis-cgi/mjpg/video.cgi?resolution=320x240'))

        self.emptyLabel = QtGui.QLabel()
        self.emptyLabel.setMinimumHeight(40)
        self.emptyLabel.setMinimumWidth(40)



        self.text = QtGui.QLineEdit(_fromUtf8("Привет"))
        #self.text.setMinimumHeight(100)
        self.text.setMinimumWidth(100)


        self.say = QtGui.QPushButton('Say')
        self.say.setMinimumHeight(27)
        #self.say.setMinimumWidth(40)
        self.say.setMaximumHeight(27)
        self.say.clicked.connect(self.sayText)

        self.words = [line.rstrip('\n') for line in open('textTTS')]
        self.list = QtGui.QComboBox()
        self.list.setMinimumWidth(100)
        for i in self.words:
            self.list.addItem(i.decode('utf-8'))

        self.list.activated[str].connect(self.sayWords)

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(1)

        #self.gridLayout.addWidget(self.emptyLabel, 0, 0)
        #self.gridLayout.addWidget(self.up, 0, 1)
        #self.gridLayout.addWidget(self.emptyLabel, 0, )
        self.gridLayout.addWidget(self.text, 0, 0)
        #self.gridLayout.addWidget(self.down, 1, 1)
        self.gridLayout.addWidget(self.say, 0, 1)
        self.gridLayout.addWidget(self.list, 1, 0, 1, 1)

        widget = QtGui.QWidget()
        widget.setLayout(self.gridLayout)

        return widget
    def sayWords(self, text):
        data =  'SAY|RU|' + unicode(text).encode('utf_8')
        print data
        print type(data)
        if self.sock != '':
            self.sock.send(data+'\n')

    def sayText(self):
        text = self.text.text()
        #print self.sock.accept()[-1]
        #print unicode(text.toUtf8(), encoding="UTF-8")
        data =  'SAY|RU|' + unicode(text).encode('utf_8')
        print data
        print type(data)
        if self.sock != '':
            self.sock.send(data+'\n')

    def getName(self):
        return self.Name

