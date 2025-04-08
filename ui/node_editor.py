# node_editor_ui.py

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsPathItem, QGraphicsRectItem, QLabel, QGraphicsProxyWidget, QGraphicsEllipseItem
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF

class Socket(QGraphicsEllipseItem):
    def __init__(self, parent, position, color=QColor("lightblue")):
        radius = 6
        super().__init__(-radius, -radius, radius * 2, radius * 2, parent)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.NoPen))
        self.setZValue(2)
        self.setPos(position)

class Node(QGraphicsRectItem):
    def __init__(self, x, y, width, height, title, color=QColor(50, 50, 50)):
        super().__init__(0, 0, width, height)
        self.setPos(x, y)
        self.setBrush(QBrush(color))
        self.setPen(QPen(QColor(100, 100, 100), 2))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.title = QLabel(title)
        self.title.setStyleSheet("color: white; background-color: transparent;")
        self.title.setFont(QFont("Arial", 10, QFont.Bold))
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.title)
        self.proxy.setPos(10, 5)

        self.inputs = []
        self.outputs = []
        self.createSockets(width, height)

    def createSockets(self, width, height):
        self.inputs.append(Socket(self, QPointF(0, height / 2), QColor("deepskyblue")))
        self.outputs.append(Socket(self, QPointF(width, height / 2), QColor("orange")))

class Connection(QGraphicsPathItem):
    def __init__(self, start_socket, end_socket):
        super().__init__()
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.setPen(QPen(QColor(255, 255, 255), 2.0))
        self.setZValue(1)
        self.updatePath()

    def updatePath(self):
        start_pos = self.start_socket.scenePos()
        end_pos = self.end_socket.scenePos()

        dx = (end_pos.x() - start_pos.x()) * 0.5
        ctrl1 = QPointF(start_pos.x() + dx, start_pos.y())
        ctrl2 = QPointF(end_pos.x() - dx, end_pos.y())

        path = QPainterPath(start_pos)
        path.cubicTo(ctrl1, ctrl2, end_pos)
        self.setPath(path)

class NodeEditor(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setBackgroundBrush(QColor(40, 40, 40))

        self.initUI()

    def initUI(self):
        node1 = Node(50, 100, 160, 60, "Image Input", QColor(70, 100, 200))
        node2 = Node(300, 100, 160, 60, "Image Output", QColor(100, 200, 100))

        self.scene.addItem(node1)
        self.scene.addItem(node2)

        connection = Connection(node1.outputs[0], node2.inputs[0])
        self.scene.addItem(connection)

        # Bind update on movement
        node1.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        node2.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        node1.itemChange = self.onNodeMove(connection)
        node2.itemChange = self.onNodeMove(connection)

    def onNodeMove(self, connection):
        def itemChange(change, value):
            if change == QGraphicsItem.ItemPositionChange:
                connection.updatePath()
            return value
        return itemChange
