import cv2
import numpy as np
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget, QComboBox, QCheckBox, QSlider, QLabel, QVBoxLayout, QWidget, QSpinBox
from PyQt5.QtCore import Qt
from core.node import BaseNode

class EdgeDetectionNode(BaseNode):
    def __init__(self):
        super().__init__("Edge Detection")
        self.title = "Edge Detection"
        self.input_image = None
        self.output_image = None

        self.method = 'Sobel'
        self.low_threshold = 50
        self.high_threshold = 150
        self.kernel_size = 3
        self.overlay = False

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Dropdown to choose method
        self.method_combo = QComboBox()
        self.method_combo.addItems(['Sobel', 'Canny'])
        self.method_combo.currentTextChanged.connect(self.update_params)
        layout.addWidget(QLabel("Method"))
        layout.addWidget(self.method_combo)

        # Threshold sliders
        self.low_slider = QSlider(Qt.Horizontal)
        self.low_slider.setRange(0, 255)
        self.low_slider.setValue(self.low_threshold)
        self.low_slider.valueChanged.connect(self.update_params)

        self.high_slider = QSlider(Qt.Horizontal)
        self.high_slider.setRange(0, 255)
        self.high_slider.setValue(self.high_threshold)
        self.high_slider.valueChanged.connect(self.update_params)

        layout.addWidget(QLabel("Low Threshold"))
        layout.addWidget(self.low_slider)
        layout.addWidget(QLabel("High Threshold"))
        layout.addWidget(self.high_slider)

        # Kernel size
        self.kernel_spin = QSpinBox()
        self.kernel_spin.setRange(1, 31)
        self.kernel_spin.setSingleStep(2)
        self.kernel_spin.setValue(self.kernel_size)
        self.kernel_spin.valueChanged.connect(self.update_params)

        layout.addWidget(QLabel("Kernel Size (odd)"))
        layout.addWidget(self.kernel_spin)

        # Overlay checkbox
        self.overlay_checkbox = QCheckBox("Overlay Edges on Original")
        self.overlay_checkbox.setChecked(self.overlay)
        self.overlay_checkbox.stateChanged.connect(self.update_params)
        layout.addWidget(self.overlay_checkbox)

        # Wrap in QWidget for proxy
        container = QWidget()
        container.setLayout(layout)
        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(container)
        proxy.setPos(0, 50)

        self.setFlag(QGraphicsItem.ItemIsMovable)

    def update_params(self):
        self.method = self.method_combo.currentText()
        self.low_threshold = self.low_slider.value()
        self.high_threshold = self.high_slider.value()
        self.kernel_size = self.kernel_spin.value()
        if self.kernel_size % 2 == 0:
            self.kernel_size += 1  # ensure it's odd
        self.overlay = self.overlay_checkbox.isChecked()
        self.update_output()

    def set_input_image(self, image):
        self.input_image = image
        self.update_output()

    def update_output(self):
        if self.input_image is None:
            return

        gray = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
        edges = None

        if self.method == 'Sobel':
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self.kernel_size)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self.kernel_size)
            edges = cv2.magnitude(sobelx, sobely)
            edges = np.uint8(np.clip(edges, 0, 255))
        elif self.method == 'Canny':
            edges = cv2.Canny(gray, self.low_threshold, self.high_threshold)

        if self.overlay:
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.output_image = cv2.addWeighted(self.input_image, 0.8, edges_colored, 0.8, 0)
        else:
            self.output_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        if hasattr(self, 'on_output_updated'):
            self.on_output_updated()

    def get_output(self):
        return self.output_image
