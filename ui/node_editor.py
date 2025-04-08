from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from nodes.image_input_node import ImageInputNode
from nodes.output_node import OutputNode
import cv2

class NodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Based Image Editor")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.label = QLabel("Welcome to Node Editor!")
        self.layout.addWidget(self.label)

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_preview)

        self.setLayout(self.layout)

        self.input_node = None
        self.output_node = OutputNode()

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.input_node = ImageInputNode(path)
            self.label.setText(f"Loaded: {path} | {self.input_node.metadata}")
            self.display_image(self.input_node.image)

    def save_image(self):
        if self.input_node:
            image = self.input_node.process()
            path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
            if path:
                self.output_node.save_image(image, path)

    def display_image(self, img):
        """Convert OpenCV image (BGR) to QPixmap and display it."""
        if img is None:
            return
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img_rgb.shape
        bytes_per_line = channels * width
        q_img = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_preview.setPixmap(scaled_pixmap)

