from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem

class BaseNode(QGraphicsItem):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.input_connections = []
        self.output_connections = []
        self.title = QGraphicsTextItem(self.name, self)
        self.title.setPos(10, -20)

    def process(self, data):
        pass
