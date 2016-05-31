from PyQt4.QtCore import *
from PyQt4.QtGui import *
import editorItem

tws = ''
class editorSceneClass(QGraphicsScene):
    def __init__(self):
        super(editorSceneClass, self).__init__()
        #self.setSceneRect(-1000, -1000, 2000, 2000)
        self.setSceneRect(0, 0, 2000, 0)
        self.grid = 20
        #self.addNode('a')


        self.popMenu = QMenu()
        action1 = self.popMenu.addAction(self.tr('Maya_Hello'))
        action2 = self.popMenu.addAction(self.tr('HandUp'))
        self.popMenu.addSeparator()
        action3 = self.popMenu.addAction(self.tr('TurnLeft'))
        action1.triggered.connect(self.functional)
        action2.triggered.connect(self.functional)
        action3.triggered.connect(self.functional)

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
        i = 0
        for x in range(left, right, self.grid):
            lines.append(QLine(x, top, x, bottom))
            #print x,
            i+=1
            painter.drawText(x+122, -42, str(i))
        for y in range(top, bottom, self.grid):
            lines.append(QLine(left, y, right, y))
            painter.drawText(y + 122, -42, str(y))

        painter.setPen(QPen(QColor(100,100,100), 1))
        painter.drawLines(lines)


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


    def mouseDoubleClickEvent(self, event):
        cursor =QCursor()
        self.popMenu.exec_(cursor.pos())
        self.addNode(event.scenePos())
        super(editorSceneClass, self).mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        for i in self.items():
            i.adjustpos()
        for i in self.selectedItems():
            i.checkCollision()
        super(editorSceneClass, self).mouseReleaseEvent(event)