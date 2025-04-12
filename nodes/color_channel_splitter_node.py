from core.node import BaseNode
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QLabel, QWidget, QGraphicsProxyWidget
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ColorChannelSplitterNode(BaseNode):
    def __init__(self):
        super().__init__("Channel Splitter")
        self.image = None
        self.channels = {}
        self.selected_channel = "R"

        self.build_ui()

    def build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        label = QLabel("Select Channel")
        label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(label)

        self.dropdown = QComboBox()
        self.dropdown.addItems(["R", "G", "B"])  # Add A if RGBA input
        self.dropdown.currentTextChanged.connect(self.on_channel_change)
        layout.addWidget(self.dropdown)

        widget.setLayout(layout)
        widget.setStyleSheet("background-color: #663399; border-radius: 5px; color: white;")
        widget.setFixedSize(180, 80)

        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(widget)

    def set_input_image(self, image):
        self.image = image
        self.split_channels()

    def split_channels(self):
        if self.image is None:
            return

        if self.image.shape[2] == 4:
            b, g, r, a = cv2.split(self.image)
            self.channels = {
                "R": r,
                "G": g,
                "B": b,
                "A": a
            }
            if "A" not in [self.dropdown.itemText(i) for i in range(self.dropdown.count())]:
                self.dropdown.addItem("A")
        else:
            b, g, r = cv2.split(self.image)
            self.channels = {
                "R": r,
                "G": g,
                "B": b
            }

    def on_channel_change(self, channel):
        self.selected_channel = channel
        self.process()
        if hasattr(self, "on_output_updated"):
            self.on_output_updated()

    def process(self):
        if self.image is not None:
            self.split_channels()

    def get_output(self):
        channel_data = self.channels.get(self.selected_channel)
        if channel_data is not None:
            return cv2.cvtColor(channel_data, cv2.COLOR_GRAY2BGR)
        return None
