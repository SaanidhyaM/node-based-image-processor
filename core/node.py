from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter

class BaseNode(QGraphicsItem):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.input_connections = []
        self.output_connections = []
        self.title = QGraphicsTextItem(self.name, self)
        self.title.setPos(10, -20)

    def boundingRect(self):
        return QRectF(0, 0, 160, 100)

    def paint(self, painter, option, widget):
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def process(self, data):
        return data