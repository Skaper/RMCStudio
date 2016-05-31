from PyQt4 import QtGui, QtCore
from style.style import sliderStyle

version = 1.0

class ServoWiget(QtCore.QObject): #ServoWiget
    def __init__(self, parend):
        self.parend = parend
        self.sock = self.parend.sock
        self.lastServoNamber = 1
        self.Name = 'Servo'
        self.type = '<servo>'
        self.analogPin = False
        self.simpleMode = 0
    def getWidget(self):
        if self.lastServoNamber <= 53:
            self.servoName = QtGui.QLineEdit()
            self.servoName.setText('Servo '+str(self.lastServoNamber))
            self.servoNameText = QtGui.QLabel('Name:')
    
            self.minValue = QtGui.QSpinBox()
            self.minValue.setMaximumWidth(55)
            self.minValue.setMaximum(360)
    
            self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.slider.setStyleSheet(sliderStyle)
            self.slider.setMinimumWidth(150)
            self.slider.setMaximum(180)
    
            self.maxValue = QtGui.QSpinBox()
            self.maxValue.setMaximumWidth(55)
            self.maxValue.setMaximum(360)
            self.maxValue.setValue(180)
            #self.delButton = QtGui.QPushButton(QtGui.QIcon('icons/del.png'), 'Del')
            #self.delButton.setMaximumWidth(55)
    
            self.positionText = QtGui.QLabel('Pos:')
            self.position = QtGui.QLabel('0')
            self.position.setMaximumWidth(25)
            self.pinText = QtGui.QLabel('Pin:')
    
            self.pin = QtGui.QSpinBox()
            self.pin.setMaximumWidth(55)
            self.pin.setMaximum(52)
            self.pin.setValue(self.lastServoNamber+2)

            self.connect(self.servoName, QtCore.SIGNAL('textChanged(QString)'),
                         self.updateData )

            self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'),
                         self.position, QtCore.SLOT('setNum(int)') )

            self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'),
                         self.servoEvent)

            self.connect(self.minValue, QtCore.SIGNAL('valueChanged(int)'),
                         self.setMinimum)
            self.connect(self.minValue, QtCore.SIGNAL('valueChanged(int)'),
                         self.updateData)

            self.connect(self.maxValue, QtCore.SIGNAL('valueChanged(int)'),
                         self.setMaximum)
            self.connect(self.maxValue, QtCore.SIGNAL('valueChanged(int)'),
                         self.updateData)

            self.connect(self.pin, QtCore.SIGNAL('valueChanged(int)'),
                         self.updateData)

            #self.connect(self.delButton, QtCore.SIGNAL('clicked()'),
            #             self.delServo)

            self.servoGrid = QtGui.QGridLayout()
            self.servoGrid.setSpacing(1)

            self.servoGrid.addWidget(self.servoNameText, 1, 0)
            self.servoGrid.addWidget(self.servoName, 1, 1, 1, 3)
            #self.servoGrid.addWidget(self.delButton, 1, 3)

            self.servoGrid.addWidget(self.minValue, 2, 0)
            self.servoGrid.addWidget(self.slider, 2, 1, 2, 2, QtCore.Qt.AlignTop)
            self.servoGrid.addWidget(self.maxValue, 2, 3)

            self.servoGrid.addWidget(self.positionText, 3, 0)
            self.servoGrid.addWidget(self.position, 3, 1)
            self.servoGrid.addWidget(self.pinText, 3, 2, QtCore.Qt.AlignRight)
            self.servoGrid.addWidget(self.pin, 3, 3)
            #self.servoGrid.addWidget(self.pin, 3, 4)

            servoWidget = QtGui.QWidget()
            servoWidget.setLayout(self.servoGrid)

            #self.connect(self.parend.tableProperties, QtCore.SIGNAL('itemChanged(QTableWidgetItem*)'), self.test )
            #self.parend.tableProperties.itemChanged.connect(self.test)
            self.updateData()

    
        return servoWidget

    def setMinimum(self, minP):
        maxV= self.maxValue.value()
        self.minValue.setMaximum(maxV-1)
        self.slider.setMinimum(minP)

    def setMaximum(self, maxP):
        minV = self.minValue.value()
        self.maxValue.setMinimum(minV+1)
        self.slider.setMaximum(maxP)

    def setPin(self, pin):
        pass

    def setName(self, name):
        pass

    def simple(self):
        pass

    def servoEvent(self, pos):
        pin = self.pin.value()
        #print type(pin)
        print str(pos) + '>' + str(pin)
        data = 'S|D'+str(pin)+'>'+str(pos)
        if self.sock != '':
            self.sock.send(data)

    def getData(self):
        data = (['Name', self.servoName.text()], ['Type', self.type], ['Min Pos',self.minValue.value()],
                ['Max Pos', self.maxValue.value()], ['Pin', self.pin.text()],['Analog Pin', self.analogPin],
                ['Simple mode', self.simpleMode])
        return data

    def getName(self):
        return self.Name

    def test(self, item):
        row = item.row()
        column = item.column()

        if column == 1:
            value = self.parend.tableProperties.item(row, column).text() #name
            name = self.parend.tableProperties.item(row, column-1).text()
            print name, '++++++++++++++', value
            if name == 'Min Pos':
                self.minValue.setValue(int(value))
            elif name == 'Max Pos':
                self.maxValue.setValue(int(value))
            elif name == 'Pin':
                self.pin.setValue(int(value))
            elif name == 'Simple mode':
                if int(value) == 1:
                    self.servoGrid.removeWidget(self.slider)
                    self.servoGrid.addWidget(self.slider, 2, 1, 2, 3, QtCore.Qt.AlignTop)
                    self.servoGrid.removeWidget(self.position)
                    self.servoGrid.addWidget(self.position, 2, 4, QtCore.Qt.AlignTop)
                    self.simpleMode = 1
                    self.servoNameText.hide()
                    self.servoName.hide()
                    self.minValue.hide()
                    self.maxValue.hide()
                    self.pin.hide()
                    self.pinText.hide()
                    #self.position.hide()
                    self.positionText.hide()

                else:
                    self.simpleMode = 0
                    self.servoGrid.removeWidget(self.slider)
                    self.servoGrid.addWidget(self.slider, 2, 1, 2, 2, QtCore.Qt.AlignTop)
                    self.servoGrid.removeWidget(self.position)
                    self.servoGrid.addWidget(self.position, 3, 1)
                    self.servoNameText.show()
                    self.servoName.show()
                    self.minValue.show()
                    self.maxValue.show()
                    self.pin.show()
                    self.pinText.show()
                    self.position.show()
                    self.positionText.show()
            elif name == 'Name':
                self.servoName.setText(value)

    def updateTable(self):
        self.parend.docListServo2 = QtGui.QDockWidget('Properties editor')
        self.parend.docListServo_Contents2 = QtGui.QWidget()
        self.parend.docListServo2.setWidget(self.parend.docListServo_Contents2)
        self.parend.docListServo_Layout2 = QtGui.QGridLayout()
        self.parend.tableProperties = QtGui.QTableWidget()
        self.parend.docListServo_Layout2.addWidget(self.parend.tableProperties)
        self.parend.docListServo_Contents2.setLayout(self.parend.docListServo_Layout2)
        self.parend.tableProperties.verticalHeader().hide()
        self.parend.tableProperties.horizontalHeader().hide()
        self.parend.tableProperties.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)


    def updateData(self):
        #self.updateTable()
        self.parend.tableProperties.setColumnCount(2)
        data = self.getData()
        self.parend.tableProperties.setRowCount(len(data))

        for i, obj in enumerate(data):
            item = QtGui.QTableWidgetItem()
            #print obj[0]
            item.setText(obj[0])
            self.parend.tableProperties.setItem(i, 0, item)
            #item.po

            #print obj[1]
            item = QtGui.QTableWidgetItem()
            item.setText(str(obj[1]))
            self.parend.tableProperties.setItem(i, 1, item)
            #self.parend.tableProperties.itemChanged.connect(self.test)

        #itemChanged(QTableWidgetItem*)
        #cellDoubleClicked (int, int)
