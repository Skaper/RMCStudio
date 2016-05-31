# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, QtWebKit
import cv2
import urllib
import numpy as np
from time import strftime
import gst

version = 1.0
class CamBuff(QtCore.QThread):
    #arrayImg = QtCore.pyqtSignal(QtCore.QImage)#np.ndarray)
    def __init__(self, url):
        QtCore.QThread.__init__(self)
        self.url = url

    def __del__(self):
        self.wait()

    def run(self):
        stream=urllib.urlopen(self.url)
        bytes=''
        while True:
            bytes+=stream.read(1024)#12288)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB) #Convert image to RGB

                height, width, bytesPerComponent = i.shape
                bytesPerLine = bytesPerComponent * width

                image = QtGui.QImage(i.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888) #Convert image to QImage

                self.emit(QtCore.SIGNAL('addImage(QImage)'), image)

class CamWidget(QtCore.QObject): #CamWidget
    def __init__(self, parend):
        self.lastServoNamber = 1
        self.Name = 'IP CAM'
        self.type = '<ipcam>'
        self.parend = parend
        self.videoCompression = 'MJPEG'
        self.resolution = '640x480'
        self.frameRate = 15
        #http://192.168.42.1:8080/?action=stream
        self.url = ''#'http://192.168.0.106:8080/video' #http://192.168.42.1:8080/?action=stream'
        if self.url != '':
            try:
                self.get_thread = CamBuff(self.url)
                self.connect(self.get_thread, QtCore.SIGNAL("addImage(QImage)"), self.addImage)
                #self.get_thread.arrayImg.connect(self.addImage)
                self.get_thread.start()
                #self.connect(self.get_thread, QtCore.SIGNAL("finished()"), self.done)
            except:
                print 'Error URL' #TODO
        #self.setURL('http://192.168.0.105:8080/video')
        self.player = gst.element_factory_make("playbin", "player")
        #sself.player.event_new_buffer_size(1024)

    def on_tag(bus, msg):
        taglist = msg.parse_tag()
        print 'on_tag:'
        for key in taglist.keys():
            print '\t%s = %s' % (key, taglist[key])


    def getWidget(self, quantity=1, load=0, file=None):

        if self.lastServoNamber <= 53:
            #elf.webCam = QtWebKit.QWebView()
            #self.webCam.setUrl(QtCore.QUrl('http://195.235.198.107:3344/axis-cgi/mjpg/video.cgi?resolution=320x240'))
            self.webCamLabel = QtGui.QLabel()
            self.screenButton = QtGui.QPushButton('Screen')
            self.screenButton.clicked.connect(self.screenshot)
            self.screenButton.setMaximumHeight(50)
            self.screenButton.setMaximumWidth(50)
            self.screenButton.setMinimumHeight(50)
            self.screenButton.setMinimumWidth(50)

            self.urlText = QtGui.QLineEdit('http://192.168.42.1:8080/?action=stream')
            self.urlText.setMinimumWidth(100)

            self.urlAudioText = QtGui.QLineEdit('http://192.168.0.105:8080/audio.wav')
            self.urlAudioText.setMinimumWidth(100)

            self.connectButton = QtGui.QPushButton('Connect')
            self.connectButton.clicked.connect(self.connect2Url)

            self.connectAudioButton = QtGui.QPushButton('Connect')
            self.connectAudioButton.clicked.connect(self.connect2UrlAudio)

            self.gridLayout = QtGui.QGridLayout()
            self.gridLayout.setSpacing(1)


            self.gridLayout.addWidget(self.webCamLabel, 0, 0, 0, 2)
            self.gridLayout.addWidget(self.urlText, 1, 0)
            self.gridLayout.addWidget(self.connectButton, 1, 1)
            self.gridLayout.addWidget(self.urlAudioText, 2, 0)
            self.gridLayout.addWidget(self.connectAudioButton, 2, 1)
            self.screenButton.hide()

            self.gridLayout.addWidget(self.screenButton, 0, 1, QtCore.Qt.AlignTop)

            widget = QtGui.QWidget()
            widget.setLayout(self.gridLayout)

            #self.updateData()
            print 'OK'

        return widget

    def screenshot(self):
        try:
            #img = Image.fromarray(image, 'RGB')
            name = strftime("%Y-%m-%d %H:%M:%S")

            self.image.save('screenshots/Screenshot ' + name, "jpeg", -1)
            self.webCamLabel.setText('SCREEN')
        except:
            print 'Error'

    def setURL(self, url):
        self.url = url
        if url != '':
            self.screenButton.show()
            self.get_thread.quit()
            self.get_thread = CamBuff(self.url)
            self.connect(self.get_thread, QtCore.SIGNAL("addImage(QImage)"), self.addImage)
            self.get_thread.start()

    def connect2UrlAudio(self):
        music_stream_uri = self.urlAudioText.text()
        self.player.set_property('uri', music_stream_uri)
        self.player.set_state(gst.STATE_PLAYING)


    def connect2Url(self):
        url = self.urlText.text()
        print url
        self.url = str(url)
        if url != '':
            try:
                self.get_thread.quit()
            except:
                pass
            self.screenButton.show()
            self.get_thread = CamBuff(self.url)
            self.connect(self.get_thread, QtCore.SIGNAL("addImage(QImage)"), self.addImage)
            self.get_thread.start()


    def addImage(self, image):
        self.image = image
        #img = Image.fromarray(image, 'RGB')
        #img.save('test.png')
        #pixmap = QtGui.QPixmap()
        #pixmap.load(img)
        #print type(img)

        self.webCamLabel.setPixmap(QtGui.QPixmap(self.image))

    def getData(self):
        data = (['Name', self.Name], ['Type', self.type], ['Url', self.url], ['Video compression', self.videoCompression], ['Resolution',self.resolution], ['Frame Rate', self.frameRate])
        return data

    def getName(self):
        return self.Name

    def hideConsole(self):
        self.urlText.hide()
        self.connectButton.hide()

    def updateData(self):
        self.parend.tableProperties.setColumnCount(2)
        data = self.getData()
        self.parend.tableProperties.setRowCount(len(data))

        for i, obj in enumerate(data):
            item = QtGui.QTableWidgetItem()
            print obj[0]
            item.setText(obj[0])
            self.parend.tableProperties.setItem(i, 0, item)

            print obj[1]
            item = QtGui.QTableWidgetItem()
            item.setText(str(obj[1]))
            self.parend.tableProperties.setItem(i, 1, item)


