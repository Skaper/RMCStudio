from PyQt4.QtCore import *
from PyQt4.QtGui import *
import editorItem




tws = ''
class editorSceneClass(QGraphicsScene):
    def __init__(self, parend=None):
        super(editorSceneClass, self).__init__()
        #self.setSceneRect(-1000, -1000, 2000, 2000)
        #self.setSceneRect(0, 0, 2000, 0)
        self.setSceneRect(0, 0, 2000, 0)
        self.grid = 20
        #self.addNode('a')
        self.parend = parend
        self.sock = self.parend.sock

        self.popMenu = QMenu()
        action1 = self.popMenu.addAction(self.tr('Maya_Hello'))
        action2 = self.popMenu.addAction(self.tr('No'))
        self.popMenu.addSeparator()
        action3 = self.popMenu.addAction(self.tr('Around'))
        action1.triggered.connect(self.functional)
        action2.triggered.connect(self.functional)
        action3.triggered.connect(self.functional)

        self.elements= ["Head", "Mouth", "LArm", "RArm"]

        self.tLine = QGraphicsLineItem(60, 100, 60, -60)
        self.tLine.setPen(QPen(QColor(255, 0, 0), 2))
        self.addItem(self.tLine)
        self.tl = QTimeLine(97000)
        self.tl.setCurveShape(3)
        self.tl.setFrameRange(0, 60)
        self.a = QGraphicsItemAnimation()
        self.a.setItem(self.tLine)
        self.a.setTimeLine(self.tl)
        self.a.setPosAt(1.0, QPointF(2000, 0))
        #self.startTimeLine()

    def functional(self):
        global tws
        tws =  self.sender().text()
        #print textin
        cursor = QCursor()
        self.addNode(cursor.pos())

    def drawBackground(self, painter, rect):
        if False:
            painter = QPainter()
        painter.fillRect(rect, QColor(30,30,30))
        left = int(rect.left()) - (int(rect.left()) % self.grid)
        top = int(rect.top()) - int(rect.top()) % self.grid
        right = int(rect.right())
        bottom = int(rect.bottom())
        lines = []
        timelines = []
        i = 0
        element = 0
        for x in range(left, right, self.grid):
            lines.append(QLine(x, top, x, bottom))
            # print x,


            #painter.drawText(x + 122, -42, str(i))

        for y in range(top, bottom, self.grid):
            lines.append(QLine(left, y, right, y))
            #painter.drawText(y + 122, -42, str(y))


        """
        for x in range(left, right, self.grid):
            lines.append(QLine(x, top, x, bottom))
            #print x,
            i+=1
            painter.drawText(x+122, -42, str(i))
        for y in range(top, bottom, self.grid):
            lines.append(QLine(left, y, right, y))
            painter.drawText(y + 122, -42, str(y))
        """
        for x in range(62, 2000, 20):
            i += 1
            # painter.drawText(x + 122, -42, str(i))
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.drawText(x, -42, str(i))

        for y in range(-24, 56, 20):
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.drawText(3, y, self.elements[element])
            element += 1
        painter.setPen(QPen(QColor(100,100,100), 1))
        painter.drawLines(lines)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        #painter.drawLine(QLine(62, 100, 62, -60))

            #painter.drawStaticText()

        self.checkCollision()
    def addNode(self, pos=False, text=""):
        if not pos:
            pos = QPoint(0,0)
        item = editorItem.editorItemClass(self.grid, tws)#len(self.items())+1)

        self.addItem(item)
        item.setPos(pos)

    def mouse(self, event):
        cursor =QCursor()
        self.popMenu.exec_(cursor.pos())
        self.popMenu.connect(self, )
        #self.addNode(event.scenePos())
        super(editorSceneClass, self).mouseDoubleClickEvent(event)

    def checkCollision(self):
        coll = self.collidingItems(self.tLine)
        if coll:
            #self.setPos(self.pos() - QPoint(0, self.h))
            #self.checkCollision()
            for x in coll:
                name = x.getText()
                data = "*"+str(name)+"*\n"
                if self.sock != '':
                    self.sock.send(data)

    def startTimeLine(self):
        print "OK START!"

        self.tl.start()



    def playTime(self):
        self.tl.start()

    def pauseTime(self):
        self.tl.stop()

    def stopTime(self):
        self.tl.destroyed()

    def mouseDoubleClickEvent(self, event):
        cursor =QCursor()
        self.popMenu.exec_(cursor.pos())
        self.addNode(event.scenePos())




        super(editorSceneClass, self).mouseDoubleClickEvent(event)

    def startTime(self):
        pass
    def mouseReleaseEvent(self, event):
        #for i in self.items():
        #    i.adjustpos()
        for i in self.selectedItems():
            i.checkCollision()
        super(editorSceneClass, self).mouseReleaseEvent(event)
