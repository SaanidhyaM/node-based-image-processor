from core.node import BaseNode
from PyQt5.QtWidgets import QGraphicsProxyWidget, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import cv2

class GrayscaleNode(BaseNode):
    def __init__(self):
        super().__init__("Grayscale")

        self.build_ui()

    def build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        label = QLabel("Grayscale Node")
        label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(label)

        widget.setLayout(layout)
        widget.setStyleSheet("background-color: #44475a; border-radius: 6px; color: white;")
        widget.setFixedSize(180, 60)

        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(widget)

    def process(self, image):
        if image is not None:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return image

    def get_output(self):
        if hasattr(self, 'input_nodes') and self.input_nodes:
            return self.process(self.input_nodes[0].get_output())
        return None

