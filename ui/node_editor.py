# ui/node_editor.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout, QGraphicsView, QGraphicsScene, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from nodes.image_input_node import ImageInputNode
from nodes.output_node import OutputNode
from nodes.brightness_contrast_node import BrightnessContrastNode
import cv2

class NodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Based Image Editor")
        self.setGeometry(100, 100, 1200, 700)

        self.image_node = None
        self.output_node = OutputNode()
        self.effect_node = None

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()

        self.load_btn = QPushButton("Load Image")
        self.save_btn = QPushButton("Save Output")
        self.add_effect_btn = QPushButton("Add Brightness/Contrast Node")
        self.image_label = QLabel("Image Preview")
        self.image_label.setFixedSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.meta_display = QTextEdit()
        self.meta_display.setReadOnly(True)

        self.load_btn.clicked.connect(self.load_image)
        self.save_btn.clicked.connect(self.save_output)
        self.add_effect_btn.clicked.connect(self.add_effect_node)

        left_panel.addWidget(self.load_btn)
        left_panel.addWidget(self.save_btn)
        left_panel.addWidget(self.add_effect_btn)
        left_panel.addWidget(self.image_label)
        left_panel.addWidget(self.meta_display)

        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.canvas.setStyleSheet("background-color: #f0f0f0; border: 1px solid black;")

        layout.addLayout(left_panel, 1)
        layout.addWidget(self.canvas, 2)

        self.setLayout(layout)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.image_node = ImageInputNode(file_path)
            pixmap = self.image_node.get_qpixmap()
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=1))
            self.output_node.set_image(self.image_node.image)
            self.display_metadata()

            if self.effect_node:
                self.effect_node.set_input_image(self.image_node.image)
                self.update_preview_from_effect()

    def display_metadata(self):
        if self.image_node:
            meta = self.image_node.metadata
            text = "\n".join([f"{key}: {value}" for key, value in meta.items()])
            self.meta_display.setText(text)

    def save_output(self):
        if self.output_node.image is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                self.output_node.save_image(file_path)

    def add_effect_node(self):
        self.effect_node = BrightnessContrastNode(50, 50)
        self.scene.addItem(self.effect_node)

        if self.image_node:
            self.effect_node.set_input_image(self.image_node.image)

        self.effect_node.brightness_slider.valueChanged.connect(self.update_preview_from_effect)
        self.effect_node.contrast_slider.valueChanged.connect(self.update_preview_from_effect)

    def update_preview_from_effect(self):
        if self.effect_node:
            edited_img = self.effect_node.get_output_image()
            if edited_img is not None:
                self.output_node.set_image(edited_img)

                rgb_image = cv2.cvtColor(edited_img, cv2.COLOR_BGR2RGB)
                height, width, channel = rgb_image.shape
                bytes_per_line = 3 * width
                qimage = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=1))