from PyQt5.QtWidgets import QGraphicsProxyWidget, QVBoxLayout, QLabel, QSlider, QWidget
from PyQt5.QtCore import Qt
import numpy as np
from core.node import BaseNode

class BrightnessContrastNode(BaseNode):
    def __init__(self):
        super().__init__("Brightness/Contrast")

        self.widget = QWidget()
        self.widget.setStyleSheet("background-color: #4B3F72; border-radius: 6px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        label = QLabel("Brightness/Contrast")
        label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(label)

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.process)
        layout.addWidget(self.brightness_slider)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(300)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.process)
        layout.addWidget(self.contrast_slider)

        self.widget.setLayout(layout)
        self.widget.setFixedSize(200, 130)

        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(self.widget)

        self.original_image = None
        self.processed_image = None

    def set_input_image(self, image):
        self.original_image = image.copy()
        self.process()

    def process(self, _=None):
        if self.original_image is None:
            return
        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value() / 100.0
        img = self.original_image.astype(np.float32)
        img = (img - 127.5) * contrast + 127.5 + brightness
        img = np.clip(img, 0, 255).astype(np.uint8)
        self.processed_image = img

    def get_output(self):
        return self.processed_image
