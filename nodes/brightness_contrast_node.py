from core.node import BaseNode
from PyQt5.QtWidgets import QGraphicsProxyWidget, QLabel, QSlider
from PyQt5.QtGui import QFont, QColor, QBrush, QPen
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class BrightnessContrastNode(BaseNode):
    def __init__(self, x, y, width=180, height=100):
        super().__init__("Brightness/Contrast")
        self.setPos(x, y)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)

        self.setToolTip("Adjust brightness and contrast")
        self.original_image = None
        self.processed_image = None

        self.create_controls(width)

    def boundingRect(self):
        return super().boundingRect()

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(QColor(80, 80, 120)))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def create_controls(self, width):
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.setFixedWidth(width - 20)
        self.brightness_slider.valueChanged.connect(self.update_image)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(300)
        self.contrast_slider.setValue(100)
        self.contrast_slider.setFixedWidth(width - 20)
        self.contrast_slider.valueChanged.connect(self.update_image)

        brightness_proxy = QGraphicsProxyWidget(self)
        brightness_proxy.setWidget(self.brightness_slider)
        brightness_proxy.setPos(10, 25)

        contrast_proxy = QGraphicsProxyWidget(self)
        contrast_proxy.setWidget(self.contrast_slider)
        contrast_proxy.setPos(10, 55)

    def set_input_image(self, image):
        self.original_image = image.copy()
        self.update_image()

    def get_output_image(self):
        return self.processed_image

    def update_image(self):
        if self.original_image is None:
            return

        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value() / 100.0  # 1.0 = neutral

        img = self.original_image.astype(np.float32)
        img = (img - 127.5) * contrast + 127.5 + brightness
        img = np.clip(img, 0, 255).astype(np.uint8)

        self.processed_image = img
