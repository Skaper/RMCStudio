# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui, QtCore
from configobj import ConfigObj
import glob
import serial
import socket
from module import editorView

print 'Run'
#sock = socket.socket()
#sock.connect(('192.168.42.1', 6518)) #6526
#sock.connect(('127.0.0.1', 6576)) #6526

#sock2 = socket.socket()
#sock2.connect(('192.168.42.1', 6003)) #6526

sock = ''
sock2 = ''

from module.servo import ServoWiget
print 'Run servo'
from module.mjpgsteamview import CamWidget
print 'Run mjpgsteamview'
from module.move import MoveWidget
print 'Run move'
from module.moveSimple import MoveSimpleWidget
print 'Run moveSimple'
from module.soundPlay import PlaySoundWidget
print 'Run soundPlay'
from module.tts import TTSWidget
print 'Run tts'
from module.battery import BattaryWidget





print 'Run'
version = 0.2

class USBcommunication():
    def __init__(self):
        self.baudrate = 115200
        self.port = ''
        self.portConnect = ''

    def setPort(self, port):
        self.port = port

    def getPortList(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def setBaudrate(self, baudrate):
        self.baudrate = baudrate

    def sendData(self, data):
        if self.portConnect:
            self.portConnect.write(data + "\n")

    def connect(self):
        if self.port:
            self.portConnect = serial.Serial(self.port, baudrate=self.baudrate, dsrdtr = 1,  timeout=1)

class ChoicePort(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ChoicePort, self).__init__(parent)
        #self.usbCom = USBcommunication()
        #self.devices = self.usbCom.getPortList()

    def setMainWindow(self, window):
        self.mainWindow = window
        self.setWindowTitle('Serial Port')



        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)


        self.devicesList = QtGui.QListWidget(self)
        self.speed = QtGui.QComboBox()
        speedList = ['300', '1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400', '57600', '115200']

        '''
        for i in speedList:
            self.speed.addItem(i)

        for i in self.devices:
            self.devicesList.addItem(i)
        '''


        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.update = QtGui.QPushButton('update')
        self.verticalLayout.addWidget(self.update)
        self.update.clicked.connect(self.updatePorts)
        self.verticalLayout.addWidget(self.devicesList)
        self.verticalLayout.addWidget(self.speed)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.returnPort)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(lambda : super(ChoicePort, self).accept())

    def returnPort(self):
        portItem = self.devicesList.currentItem()

        if portItem:
            portName = portItem.text()
            getSpeed = str(self.speed.currentText())
            self.mainWindow.choiceUsbPort(str(portName), str(getSpeed))
            super(ChoicePort, self).accept()

    def updatePorts(self):
        self.devicesList.clear()
        self.devices = self.usbCom.getPortList()
        for i in self.devices:
            self.devicesList.addItem(i)

class SubWindow(QtGui.QMdiSubWindow):

    def __init__(self, parent=None):
        self.parent = parent
        QtGui.QMdiSubWindow.__init__(self)
        #super(SubWindow, self).__init__(parent)

    def closeEvent(self, QCloseEvent):
        print '+++++++++++++++++++++++++++++++++++++++++++++++'
        self.parent.updateData()


    def focusOutEvent(self, event):

        print event

        self.parent.updateData()
        print self.widget()

class MainWindow(QtGui.QMainWindow):

    def __init__(self, portWindow):
        print 'Loading GUI'
        QtGui.QMainWindow.__init__(self)
        self.sock = sock
        self.setGeometry(100, 100, 900, 650)

        #self.usbCom = USBcommunication()
        self.port = ''
        self.statusBar()

        self.labelPort  = QtGui.QLabel(self.port)
        self.statusBar().addWidget( self.labelPort,2)

        self.mdi = QtGui.QMdiArea()
        self.mdi.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdi.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdi.setBackground(QtGui.QBrush(QtGui.QColor(240, 240, 240)))
        self.mdi.setBackground(QtGui.QBrush(QtGui.QPixmap('icons/logo.png')))
        #self.mdi.mousePressEvent(self, self.test2)
        self.setCentralWidget(self.mdi)

        self.docList = QtGui.QDockWidget('Objects')
        self.docList_Contents = QtGui.QWidget()
        self.docList.setWidget(self.docList_Contents)

        self.docList_Layout = QtGui.QGridLayout()
        self.listElements = QtGui.QListWidget()
        self.docList_Layout.addWidget(self.listElements)
        self.docList_Contents.setLayout(self.docList_Layout)

        self.docListServo2 = QtGui.QDockWidget('Properties editor')
        self.docListServo_Contents2 = QtGui.QWidget()
        self.docListServo2.setWidget(self.docListServo_Contents2)
        self.docListServo_Layout2 = QtGui.QGridLayout()
        self.tableProperties = QtGui.QTableWidget()
        self.docListServo_Layout2.addWidget(self.tableProperties)
        self.docListServo_Contents2.setLayout(self.docListServo_Layout2)
        self.tableProperties.verticalHeader().hide()
        self.tableProperties.horizontalHeader().hide()
        self.tableProperties.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)


        '''
         self.docTerminal = QtGui.QDockWidget('Terminal')
        self.docTerminal_Contents = QtGui.QWidget()
        self.docTerminal.setWidget(self.docTerminal_Contents)
        #self.docTerminal.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)

        self.docTerminal_Layout = QtGui.QGridLayout()
        self.terminal = QtGui.QTextEdit()
        self.docTerminal_Layout.addWidget(self.terminal)
        #self.docTerminal_Layout.setVerticalSpacing(1)
        #self.docTerminal.setTitleBarWidget(QtGui.QWidget(self.docTerminal))
        self.docTerminal_Contents.setLayout(self.docTerminal_Layout)
        '''
        self.view = editorView.editorViewClass()
        self.view2 = editorView.editorViewClass()
        self.docTerminal = QtGui.QDockWidget('Terminal')
        self.docTerminal_Contents = QtGui.QWidget()
        self.docTerminal.setWidget(self.docTerminal_Contents)
        #self.docTerminal.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)

        self.docTerminal_Layout = QtGui.QGridLayout()
        self.terminal = QtGui.QTextEdit()
        self.layato = QtGui.QGridLayout()
        scene1 = QtGui.QLineEdit("Nao 1")
        scene1.setMaximumHeight(100)
        scene1.setMaximumWidth(100)
        start1 = QtGui.QPushButton("Start >")
        start1.setMaximumHeight(200)
        start1.setMaximumWidth(200)
        close1 = QtGui.QPushButton("X")
        close1.setMaximumHeight(100)
        close1.setMaximumWidth(40)
        log1 = QtGui.QPushButton("Log")
        log1.setMaximumHeight(100)
        log1.setMaximumWidth(40)

        self.layato.addWidget(scene1, 0, 0)
        self.layato.addWidget(close1, 0, 1)
        self.layato.addWidget(start1, 1, 0)
        self.layato.addWidget(log1, 1, 1)
        self.wiglayayot = QtGui.QWidget()
        self.wiglayayot.setLayout(self.layato)

        startAll1 = QtGui.QPushButton("Start/Pause")
        startAll1.setMaximumHeight(100)
        startAll1.setMaximumWidth(100)
        stopAll1 = QtGui.QPushButton("Stop")
        stopAll1.setMaximumHeight(100)
        stopAll1.setMaximumWidth(60)
        battarryWd10 = BattaryWidget()
        battarryWd1 = battarryWd10.getWidget()
        self.docTerminal_Layout.addWidget(startAll1, 0, 0)
        self.docTerminal_Layout.addWidget(stopAll1, 0, 1)
        #self.docTerminal_Layout.addWidget(stopAll1, 0, 2)
        self.docTerminal_Layout.addWidget(self.wiglayayot, 1, 0, )
        self.docTerminal_Layout.addWidget(self.view, 1, 1)
        self.docTerminal_Layout.addWidget(battarryWd1, 1, 2)

        self.layato2 = QtGui.QGridLayout()
        scene2 = QtGui.QLineEdit("Nao 2")
        scene2.setMaximumHeight(100)
        scene2.setMaximumWidth(100)
        start2 = QtGui.QPushButton("Start >")
        start2.setMaximumHeight(100)
        start2.setMaximumWidth(100)
        close2 = QtGui.QPushButton("X")
        close2.setMaximumHeight(100)
        close2.setMaximumWidth(40)
        log2 = QtGui.QPushButton("Log")
        log2.setMaximumHeight(100)
        log2.setMaximumWidth(40)

        self.layato2.addWidget(scene2, 0, 0)
        self.layato2.addWidget(close2, 0, 1)
        self.layato2.addWidget(start2, 1, 0)
        self.layato2.addWidget(log2, 1, 1)
        self.wiglayayot2 = QtGui.QWidget()
        self.wiglayayot2.setLayout(self.layato2)
        battarryWd20 = BattaryWidget()
        battarryWd2 = battarryWd20.getWidget()
        self.docTerminal_Layout.addWidget(self.wiglayayot2, 2, 0)
        self.docTerminal_Layout.addWidget(self.view2, 2, 1)
        self.docTerminal_Layout.addWidget(battarryWd2, 2, 2)
        #self.docTerminal_Layout.setVerticalSpacing(1)
        #self.docTerminal.setTitleBarWidget(QtGui.QWidget(self.docTerminal))
        self.docTerminal_Contents.setLayout(self.docTerminal_Layout)


        self.docWidgets = QtGui.QDockWidget('Robots')
        self.docWidgets_Contents = QtGui.QWidget()
        self.docWidgets.setWidget(self.docWidgets_Contents)



        self.docWidgets_Layout = QtGui.QGridLayout()
        self.docWidgets_Layout.setSpacing(0)
        self.listWidgetsDoc = QtGui.QListWidget()
        self.docWidgets_Layout.addWidget(self.listWidgetsDoc)
        self.docWidgets_Contents.setLayout(self.docWidgets_Layout)
        #self.updateWitdgetList()
        self.listWidgetsDoc.addItem("Nao")
        self.listWidgetsDoc.itemDoubleClicked.connect(self.tx)

        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.docWidgets)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.docList)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.docListServo2)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.docTerminal)

        self.fileName = ''
        self.programIsSave = 0

        self.lastServoNamber = 0    #Последняя подключенная
        self.columnServo = 0
        self.rowServo = 0
        self.servoInColumn = 6
        self.servoInWindow = 0


        self.setWindowTitle('Robot Control ' + str(version))

        self.massServoGrid = QtGui.QGridLayout() #Хранилище блоков управления сервами
        self.massServoGrid.setSpacing(10)

        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        open = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open project ...', self)
        open.setShortcut('Ctrl+O')
        open.setStatusTip('Open project file')
        self.connect(open, QtCore.SIGNAL('triggered()'), self.openProject)

        save = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        save.setShortcut('Ctrl+S')
        save.setStatusTip('Save project')
        self.connect(save, QtCore.SIGNAL('triggered()'), self.saveThisFile)

        saveAs = QtGui.QAction('Save project As ...', self)
        saveAs.setStatusTip('Save project file')
        self.connect(saveAs, QtCore.SIGNAL('triggered()'), self.saveProject)

        newProject = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New Project...', self)
        newProject.setShortcut('Ctrl+N')
        newProject.setStatusTip('New Project')
        self.connect(newProject, QtCore.SIGNAL('triggered()'), self.newProject)

        add = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'Servo', self)
        add.setShortcut('Ctrl+N')
        add.setStatusTip('Add servo')
        self.connect(add, QtCore.SIGNAL('triggered()'), self.addServo)

        addImg = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'WebCam', self)
        addImg.setShortcut('Ctrl+N')
        addImg.setStatusTip('Add image')
        self.connect(addImg, QtCore.SIGNAL('triggered()'), self.addImage)

        addMove = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'Move', self)
        addMove.setShortcut('Ctrl+N')
        addMove.setStatusTip('Add move')
        self.connect(addMove, QtCore.SIGNAL('triggered()'), self.addMove)

        addMoveSimple = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'Move simple', self)
        addMoveSimple.setShortcut('Ctrl+N')
        addMoveSimple.setStatusTip('Add move simple')
        self.connect(addMoveSimple, QtCore.SIGNAL('triggered()'), self.addMoveSimple)

        addSoundPlay = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'Sound Play', self)
        addSoundPlay.setShortcut('Ctrl+N')
        addSoundPlay.setStatusTip('Add sound Play')
        self.connect(addSoundPlay, QtCore.SIGNAL('triggered()'), self.addSoundPlay)

        addTTS = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'TTS', self)
        addTTS.setShortcut('Ctrl+N')
        addTTS.setStatusTip('Add sound Play')
        self.connect(addTTS, QtCore.SIGNAL('triggered()'), self.addTTS)

        addBattery = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'Battery', self)
        addBattery.setShortcut('Ctrl+N')
        addBattery.setStatusTip('Battery')
        self.connect(addBattery, QtCore.SIGNAL('triggered()'), self.addBattary)

        #portLabel = QtGui.QLabel('Port: ')
        port = QtGui.QAction(QtGui.QIcon('icons/usb.png'), 'Connetcion...', self)
        port.setShortcut('Ctrl+C')
        port.setStatusTip('Connection to Arduino')
        self.connect(port, QtCore.SIGNAL('triggered()'), portWindow.show)

        hint =QtGui.QAction(QtGui.QIcon('icons/usb.png'), 'Hint', self)
        self.connect(hint, QtCore.SIGNAL('triggered()'), self.hintEvent)
        self.isHintSubWindows = False

        doc =QtGui.QAction(QtGui.QIcon('icons/usb.png'), 'Doc', self)
        self.connect(doc, QtCore.SIGNAL('triggered()'), self.docVisible)
        self.isHintDocWindows = False

        test = QtGui.QAction(QtGui.QIcon('icons/usb.png'), 'test...', self)
        test.setShortcut('Ctrl+C')
        test.setStatusTip('test to test')


        menubar = self.menuBar()
        #menubar.connect(serialPort, QtCore.SIGNAL('hovered()'), self.choiceUsbPort)

        file = menubar.addMenu('&File')
        file.addAction(newProject)
        file.addAction(open)
        file.addAction(save)
        file.addAction(saveAs)
        file.addAction(exit)

        #service = menubar.addMenu('&Service')
        #serialPort = service.addMenu('&Serial Port')
        #self.connect(serialPort, QtCore.SIGNAL('actionTriggered(int)'), self.choiceUsbPort)
        #serialPort.addAction(test)
        #serialPort.actionEvent(self.choiceUsbPort)
        #service.addAction(sp, self.choiceUsbPort)


        toolbar = self.addToolBar('Add')
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        toolbar.addAction(add)
        toolbar.addAction(addImg)
        toolbar.addAction(addMove)
        toolbar.addAction(addMoveSimple)
        toolbar.addAction(addSoundPlay)
        toolbar.addAction(addTTS)
        toolbar.addAction(addBattery)
        toolbar.addAction(port)
        toolbar.addAction(hint)
        toolbar.addAction(doc)

        self.servoW=[]
        self.webCam=[]
        self.move = []
        self.moveSimple = []
        self.soundPlay = []
        self.tts = []
        self.battary = []

        self.servoSub = []
        self.servoData =[]
        #self.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_W), self), QtCore.SIGNAL('activated()'), self.tx)

        print 'GUI >> OK'
    def tx(self, item):
        print 'asd' + str(item.text())
    def keyPressEvent(self, event):
        print str(event.key()), 'dfsfsdf'
        #if (event.key() == QtCore.Qt.Key_W): #and  (event.modifiers() == QtCore.Qt.ControlModifier):
        if event.nativeScanCode() == 83:
            print 'KKKKKKKKKKKK'


    def docVisible(self):
        if not self.isHintDocWindows:
            self.docWidgets.close()
            self.docList.close()
            self.docListServo2.close()
            self.docTerminal.close()
            self.isHintDocWindows = True
        else:
            self.docWidgets.show()
            self.docList.show()
            self.docListServo2.show()
            self.docTerminal.show()
            self.isHintDocWindows = False

    def hintEvent(self):
        print 1
        if not self.isHintSubWindows:
            for i in self.mdi.subWindowList():
                #i.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred).setHeightForWidth(True))
                i.setWindowFlags(QtCore.Qt.FramelessWindowHint)
                #i.setOption(QtGui.QMdiSubWindow.RubberBandMove, on=False)
                i.update()
            self.isHintSubWindows = True
        else:
            for i in self.mdi.subWindowList():
                #i.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred).setHeightForWidth(True))
                i.normalGeometry()
                #i.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
                #i.setWindowFlags(QtCore.Qt.Frame)
                #i.setOption(QtGui.QMdiSubWindow.RubberBandMove, on=False)
                i.update()
            self.isHintSubWindows = False

    def choiceUsbPort(self, port, br):
        if port:
            self.port = port
            self.usbCom.setPort(self.port)
            self.usbCom.setBaudrate(br)
            self.labelPort.setText('Arduino on '+self.port)
            self.usbCom.connect()

    def updateWitdgetList(self):
        allFiles = os.listdir('module')
        modules = filter(lambda x: x.endswith('.py'), allFiles)
        print modules
        #self.ui.tableScripts.setColumnCount(2)
        #self.ui.tableScripts.setRowCount(len(files))
        for widget in modules:
            if '__init__' not in widget:
                print widget
                foo = imp.load_source(widget, 'module/'+widget)
                name = foo.Widget()

                self.listWidgetsDoc.addItem(name.getName())
        print dict

    def addBattary(self):
        self.battary.append(BattaryWidget())


        self.lastServoNamber +=1

        sub = QtGui.QMdiSubWindow()
        #sub.normalGeometry()
        sub.setWidget(self.battary[-1].getWidget())


        sub.setWindowTitle("battary "+str(self.lastServoNamber))

        self.mdi.addSubWindow(sub)

        sub.show()
        #self.listElements.clear()
        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def addTTS(self):
        self.tts.append(TTSWidget(sock))


        self.lastServoNamber +=1

        sub = QtGui.QMdiSubWindow()

        sub.setWidget(self.tts[-1].getWidget())

        sub.setWindowTitle("Say "+str(self.lastServoNamber))
        self.mdi.addSubWindow(sub)

        sub.show()
        #self.listElements.clear()
        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def addSoundPlay(self):
        self.soundPlay.append(PlaySoundWidget(sock))


        self.lastServoNamber +=1

        sub = QtGui.QMdiSubWindow()

        sub.setWidget(self.soundPlay[-1].getWidget())

        sub.setWindowTitle("move "+str(self.lastServoNamber))
        self.mdi.addSubWindow(sub)

        sub.show()
        #self.listElements.clear()
        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def addMoveSimple(self):
        self.moveSimple.append(MoveSimpleWidget(sock))


        self.lastServoNamber +=1

        sub = QtGui.QMdiSubWindow()

        sub.setWidget(self.moveSimple[-1].getWidget())

        sub.setWindowTitle("move "+str(self.lastServoNamber))
        self.mdi.addSubWindow(sub)

        sub.show()
        #self.listElements.clear()
        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def addMove(self):
        self.move.append(MoveWidget(sock))


        self.lastServoNamber +=1

        sub = QtGui.QMdiSubWindow()

        sub.setWidget(self.move[-1].getWidget())

        sub.setWindowTitle("move "+str(self.lastServoNamber))
        self.mdi.addSubWindow(sub)

        sub.show()
        #self.listElements.clear()
        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def addImage(self):
        cam = CamWidget(self)
        self.webCam.append(cam)

        self.lastServoNamber +=1

        sub = SubWindow(cam)

        sub.setWidget(self.webCam[-1].getWidget())

        sub.setWindowTitle("ipCam "+str(self.lastServoNamber))
        self.mdi.addSubWindow(sub)
        #self.test(cam)


        sub.show()


        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def test2(self):
        print self.sender()

    def test(self, cam):
        self.tableProperties.setColumnCount(2)
        data = cam.getData()
        self.tableProperties.setRowCount(len(data))

        for i, name in enumerate(data.keys()):
            inf = data[name]
            item = QtGui.QTableWidgetItem()
            item.setText(name)
            self.tableProperties.setItem(i, 0, item)

            item = QtGui.QTableWidgetItem()
            item.setText(str(inf))
            self.tableProperties.setItem(i, 1, item)
        #self.listElements.clear()
        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def addServo(self):
        servo = ServoWiget(self)
        self.servoW.append(servo)
        self.lastServoNamber +=1


        sub = SubWindow(self.servoW[-1])
        self.servoSub.append(sub)

        self.servoSub[-1].setWidget(self.servoW[-1].getWidget())

        self.servoSub[-1].setWindowTitle("servo "+str(self.lastServoNamber))

        self.mdi.addSubWindow(self.servoSub[-1])

        #self.tableProperties.itemChanged.connect(self.servoW[-1].test)


        sub.show()
        #self.listElements.clear()
        self.listElements.addItem(str(self.mdi.subWindowList()[-1].windowTitle()))

    def servoEvent(self, pos):
        id = self.slider.index(self.sender())
        pin = self.pin[id].value()
        data = 'S|D'+str(pin) +'>'+str(pos)
        #print data
        self.terminal.append('SEND: ' + data)
        if self.port:
            self.usbCom.sendData(data)

    def delServo(self):
        id = self.delButton.index(self.sender())
        servoName = str(self.servoName[id].text())
        quit_msg = "Are you sure want to delete <" + servoName  + "> ?"
        dialog = QtGui.QMessageBox.question(self, 'Delete servo.',
                     quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if dialog == QtGui.QMessageBox.Yes:
            self.massServoGrid.removeItem(self.servoGrid[id])
            self.servoGrid[id] = 0
            #self.centralWidget = QtGui.QWidget()
            #self.setCentralWidget(self.centralWidget)
            #self.centralWidget.setLayout(self.massServoGrid)
            self.servoInWindow -=1
            self.statusBar().showMessage('Servo ' + servoName + ' delete!')

    def setMinForSlider(self, arg):
        id = self.minValue.index(self.sender())
        self.slider[id].setMinimum(arg)

    def setMaxForSlider(self, arg):
        id = self.maxValue.index(self.sender())
        self.slider[id].setMaximum(arg)

    def openProject(self):
        dialog = 0
        print self.servoInWindow
        if self.servoInWindow > 0:
            quit_msg = "Open saved projects? All changes in the current project will be lost!"
            dialog = QtGui.QMessageBox.question(self, 'Open saved projects.',
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if dialog == QtGui.QMessageBox.Yes or self.servoInWindow == 0:
            self.columnServo = 0
            self.rowServo = 0
            self.servoInWindow = 0
            self.lastServoNamber = 0
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'servoControl')
            if filename:
                self.fileName = filename
                settings = ConfigObj(str(filename))
                servoQuantity = int(settings['Servo'])
                self.addSerovoWidget(quantity = servoQuantity, load = 1, file = settings)



    def saveThisFile(self):
        if self.fileName:
            self.saveProject(wasSave=0)
            self.statusBar().showMessage('Saving is done!')
        else:
            self.saveProject()

    def newProject(self):
        portWindow = ChoicePort()
        MainWindow(portWindow)

        main = MainWindow(portWindow)
        portWindow.setMainWindow(main)
        main.show()

    def saveProject(self, wasSave=1):
        if wasSave:
            self.fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save Project', 'servoControl', filter='*.servo', selectedFilter='*.servo')
        if self.fileName and self.lastServoNamber>0:
            if sys.platform.startswith('linux'):
                projectName = str(self.fileName).split('/')[-1]
            else:
                projectName = str(self.fileName).split('\\')[-1]

            self.setWindowTitle('ServoConrol. Project: ' + projectName)

            config = ConfigObj()
            config['ProjectName'] = projectName
            config['Servo'] = self.servoInWindow

            id = 1
            for i in range(1, self.lastServoNamber+1):
                if self.servoGrid[i] != 0:
                    servoName = str(self.servoName[i].text())
                    minPos =self.minValue[i].value()
                    maxPos =self.maxValue[i].value()
                    pin = self.pin[i].value()
                    sliderPos = self.slider[i].value()
                    config[str(id)] = {'servoName'+str(id): servoName, 'minPos'+str(id): minPos,
                                'maxPos'+str(id): maxPos, 'pin'+str(id): pin, 'sliderPos'+str(id): sliderPos}
                    id +=1


            self.fileName = self.fileName if '.servo' in self.fileName else self.fileName+'.servo'
            config.filename = self.fileName
            config.write()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    portWindow = ChoicePort()
    main = MainWindow(portWindow)
    portWindow.setMainWindow(main)
    main.show()
    sys.exit(app.exec_())