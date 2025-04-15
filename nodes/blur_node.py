# nodes/blur_node.py

from PyQt5.QtWidgets import (
    QGraphicsItem, QGraphicsWidget, QGraphicsProxyWidget, 
    QVBoxLayout, QWidget, QLabel, QSlider, QComboBox
)
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class BlurNode(QGraphicsWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.output_image = None
        self.on_output_updated = None

        self.widget = QWidget()
        self.layout = QVBoxLayout()

        self.title = QLabel("Blur Node")
        self.title.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.title)

        # Radius slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 20)
        self.slider.setValue(5)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.apply_blur)
        self.layout.addWidget(QLabel("Radius"))
        self.layout.addWidget(self.slider)

        # Blur direction dropdown
        self.direction_selector = QComboBox()
        self.direction_selector.addItems(["Uniform", "Horizontal", "Vertical"])
        self.direction_selector.currentIndexChanged.connect(self.apply_blur)
        self.layout.addWidget(QLabel("Blur Direction"))
        self.layout.addWidget(self.direction_selector)

        self.widget.setLayout(self.layout)
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)

    def set_input_image(self, image):
        self.image = image
        self.apply_blur()

    def apply_blur(self):
        if self.image is None:
            return

        radius = self.slider.value()
        if radius < 1:
            radius = 1

        direction = self.direction_selector.currentText()

        if direction == "Horizontal":
            ksize = (radius * 2 + 1, 1)
        elif direction == "Vertical":
            ksize = (1, radius * 2 + 1)
        else:  # Uniform
            ksize = (radius * 2 + 1, radius * 2 + 1)

        blurred = cv2.GaussianBlur(self.image, ksize, 0)
        self.output_image = blurred

        if self.on_output_updated:
            self.on_output_updated()

    def get_output(self):
        return self.output_image
