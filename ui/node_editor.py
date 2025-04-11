# ui/node_editor.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout, QGraphicsView, QGraphicsScene, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from nodes.image_input_node import ImageInputNode
from nodes.output_node import OutputNode
from nodes.brightness_contrast_node import BrightnessContrastNode
from nodes.grayscale_node import GrayscaleNode
import cv2

class NodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Based Image Editor")
        self.setGeometry(100, 100, 1200, 700)

        self.image_node = None
        self.output_node = OutputNode()
        self.effect_node = None
        self.gray_node = None

        self.init_ui()

    def init_ui(self):
        self.active_nodes = []
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()

        self.load_btn = QPushButton("Load Image")
        self.save_btn = QPushButton("Save Output")
        self.add_effect_btn = QPushButton("Add Brightness/Contrast Node")
        self.add_grayscale_btn = QPushButton("Add Grayscale Node")
        self.reset_btn = QPushButton("Reset Nodes")
        self.reset_btn.clicked.connect(self.reset_nodes)
        
        self.image_label = QLabel("Image Preview")
        self.image_label.setFixedSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.remove_node_btn = QPushButton("Remove Last Node")
        self.remove_node_btn.clicked.connect(self.remove_last_node)

        self.meta_display = QTextEdit()
        self.meta_display.setReadOnly(True)

        self.load_btn.clicked.connect(self.load_image)
        self.save_btn.clicked.connect(self.save_output)
        self.add_effect_btn.clicked.connect(self.add_effect_node)
        self.add_grayscale_btn.clicked.connect(self.add_grayscale_node)

        left_panel.addWidget(self.load_btn)
        left_panel.addWidget(self.save_btn)
        left_panel.addWidget(self.add_effect_btn)
        left_panel.addWidget(self.add_grayscale_btn)
        left_panel.addWidget(self.remove_node_btn)
        left_panel.addWidget(self.reset_btn)
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
            if self.gray_node:
                self.update_preview_from_grayscale()

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
        self.effect_node = BrightnessContrastNode()
        self.effect_node.setPos(50, 50 + len(self.active_nodes) * 150)
        self.scene.addItem(self.effect_node)
        self.active_nodes.append(self.effect_node)

        if self.image_node:
            self.effect_node.set_input_image(self.image_node.image)

        self.effect_node.brightness_slider.valueChanged.connect(self.update_preview_from_effect)
        self.effect_node.contrast_slider.valueChanged.connect(self.update_preview_from_effect)

    def update_preview_from_effect(self):
        if self.effect_node:
            base_img = self.image_node.image if self.image_node else None
            if base_img is None:
                return
            self.effect_node.set_input_image(base_img)
            edited_img = self.effect_node.get_output()

            if self.gray_node:
                edited_img = self.gray_node.process(edited_img)

            if edited_img is not None:
                self.output_node.set_image(edited_img)
                self.update_preview(edited_img)

    def add_grayscale_node(self):
        self.gray_node = GrayscaleNode()
        self.gray_node.setPos(300, 50 + len(self.active_nodes) * 150)
        self.scene.addItem(self.gray_node)
        self.active_nodes.append(self.gray_node)
        self.update_preview_from_grayscale()

    def update_preview_from_grayscale(self):
        if self.gray_node:
            base_img = self.image_node.image if self.image_node else None
            if base_img is None:
                return
            if self.effect_node:
                self.effect_node.set_input_image(base_img)
                base_img = self.effect_node.get_output()

            gray_img = self.gray_node.process(base_img)

            if gray_img is not None:
                self.output_node.set_image(gray_img)
                self.update_preview(gray_img)

    def remove_last_node(self):
        if self.active_nodes:
            node = self.active_nodes.pop()
            self.scene.removeItem(node)
            self.effect_node = None if isinstance(node, BrightnessContrastNode) else self.effect_node
            self.gray_node = None if isinstance(node, GrayscaleNode) else self.gray_node
            if self.image_node:
                self.output_node.set_image(self.image_node.image)
                self.update_preview(self.image_node.image)

    def reset_nodes(self):
        if self.effect_node:
            self.effect_node.brightness_slider.setValue(0)
            self.effect_node.contrast_slider.setValue(100)
        if self.gray_node:
            self.scene.removeItem(self.gray_node)
            self.gray_node = None
        if self.image_node:
            self.output_node.set_image(self.image_node.image)
            self.update_preview(self.image_node.image)

    def update_preview(self, img):
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        qimage = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=1))
