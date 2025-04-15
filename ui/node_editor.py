# ui/node_editor.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout, QGraphicsView, QGraphicsScene, QTextEdit, QGraphicsEllipseItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QImage, QPainterPath, QPen, QColor
from PyQt5.QtCore import Qt, QPointF
from nodes.image_input_node import ImageInputNode
from nodes.output_node import OutputNode
from nodes.brightness_contrast_node import BrightnessContrastNode
from nodes.grayscale_node import GrayscaleNode
from nodes.color_channel_splitter_node import ColorChannelSplitterNode
from nodes.blur_node import BlurNode  # Import the new BlurNode
import cv2

class ConnectionLine(QGraphicsPathItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.setPen(QPen(Qt.white, 2))
        self.update_path()

    def update_path(self):
        start_pos = self.start_item.scenePos()
        end_pos = self.end_item.scenePos()
        path = QPainterPath()
        path.moveTo(start_pos)
        dx = (end_pos.x() - start_pos.x()) * 0.5
        ctrl1 = QPointF(start_pos.x() + dx, start_pos.y())
        ctrl2 = QPointF(end_pos.x() - dx, end_pos.y())
        path.cubicTo(ctrl1, ctrl2, end_pos)
        self.setPath(path)

class NodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-Based Image Editor")
        self.setGeometry(100, 100, 1200, 700)
        self.image_node = None
        self.output_node = OutputNode()
        self.effect_node = None
        self.gray_node = None
        self.splitter_node = None
        self.blur_node = None  # Declare BlurNode
        self.active_nodes = []
        self.connections = []
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        left_panel = QVBoxLayout()

        self.load_btn = QPushButton("Load Image")
        self.save_btn = QPushButton("Save Output")
        self.add_effect_btn = QPushButton("Add Brightness/Contrast Node")
        self.add_grayscale_btn = QPushButton("Add Grayscale Node")
        self.add_splitter_btn = QPushButton("Add Channel Splitter Node")
        self.add_blur_btn = QPushButton("Add Blur Node")  # Button to add the BlurNode
        self.remove_node_btn = QPushButton("Remove Last Node")
        self.reset_btn = QPushButton("Reset Nodes")

        self.image_label = QLabel("Image Preview")
        self.image_label.setFixedSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.meta_display = QTextEdit()
        self.meta_display.setReadOnly(True)

        self.load_btn.clicked.connect(self.load_image)
        self.save_btn.clicked.connect(self.save_output)
        self.add_effect_btn.clicked.connect(self.add_effect_node)
        self.add_grayscale_btn.clicked.connect(self.add_grayscale_node)
        self.add_splitter_btn.clicked.connect(self.add_splitter_node)
        self.add_blur_btn.clicked.connect(self.add_blur_node)  # Connect BlurNode button
        self.remove_node_btn.clicked.connect(self.remove_last_node)
        self.reset_btn.clicked.connect(self.reset_nodes)

        for btn in [self.load_btn, self.save_btn, self.add_effect_btn, self.add_grayscale_btn, self.add_splitter_btn, self.add_blur_btn, self.remove_node_btn, self.reset_btn]:
            left_panel.addWidget(btn)

        left_panel.addWidget(self.image_label)
        left_panel.addWidget(self.meta_display)

        self.canvas = QGraphicsView()
        self.scene = QGraphicsScene()
        self.canvas.setScene(self.scene)
        self.canvas.setStyleSheet("background-color: #f0f0f0; border: 1px solid black;")

        layout.addLayout(left_panel, 1)
        layout.addWidget(self.canvas, 2)

        self.setLayout(layout)

    def create_socket(self, x, y):
        socket = QGraphicsEllipseItem(-5, -5, 10, 10)
        socket.setBrush(QColor("#4caf50"))
        socket.setPos(x, y)
        self.scene.addItem(socket)
        return socket

    def connect_nodes(self, output_socket, input_socket):
        connection = ConnectionLine(output_socket, input_socket)
        self.scene.addItem(connection)
        self.connections.append(connection)

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
            if self.splitter_node:
                self.update_preview_from_splitter()
            if self.blur_node:  # If BlurNode is added, update the preview from it as well
                self.update_preview_from_blur()

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

    def add_grayscale_node(self):
        self.gray_node = GrayscaleNode()
        self.gray_node.setPos(300, 50 + len(self.active_nodes) * 150)
        self.scene.addItem(self.gray_node)
        self.active_nodes.append(self.gray_node)
        self.update_preview_from_grayscale()

    def add_splitter_node(self):
        self.splitter_node = ColorChannelSplitterNode()
        self.splitter_node.setPos(550, 50 + len(self.active_nodes) * 150)
        self.scene.addItem(self.splitter_node)
        self.active_nodes.append(self.splitter_node)

        if self.image_node:
            self.splitter_node.set_input_image(self.image_node.image)

        # Hook live preview callback
        def update_preview_from_channel():
            output = self.splitter_node.get_output()
            if output is not None:
                self.output_node.set_image(output)
                self.update_preview(output)

        self.splitter_node.on_output_updated = update_preview_from_channel
        update_preview_from_channel()

    def add_blur_node(self):
        self.blur_node = BlurNode()  # Create BlurNode instance
        self.blur_node.setPos(800, 50 + len(self.active_nodes) * 150)  # Set position of the blur node
        self.scene.addItem(self.blur_node)
        self.active_nodes.append(self.blur_node)

        if self.image_node:
            self.blur_node.set_input_image(self.image_node.image)

        # Hook live preview callback for blur
        def update_preview_from_blur():
            output = self.blur_node.get_output()
            if output is not None:
                self.output_node.set_image(output)
                self.update_preview(output)

        self.blur_node.on_output_updated = update_preview_from_blur
        update_preview_from_blur()

    def remove_last_node(self):
        if self.active_nodes:
            node = self.active_nodes.pop()
            self.scene.removeItem(node)
            self.effect_node = None if isinstance(node, BrightnessContrastNode) else self.effect_node
            self.gray_node = None if isinstance(node, GrayscaleNode) else self.gray_node
            self.splitter_node = None if isinstance(node, ColorChannelSplitterNode) else self.splitter_node
            self.blur_node = None if isinstance(node, BlurNode) else self.blur_node  # Remove blur node if it's the last node
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
        if self.splitter_node:
            self.scene.removeItem(self.splitter_node)
            self.splitter_node = None
        if self.blur_node:
            self.scene.removeItem(self.blur_node)  # Reset the blur node if added
            self.blur_node = None
        if self.image_node:
            self.output_node.set_image(self.image_node.image)
            self.update_preview(self.image_node.image)

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

    def update_preview_from_splitter(self):
        if self.splitter_node:
            self.splitter_node.set_input_image(self.image_node.image)
            r_channel = self.splitter_node.get_output("R")
            if r_channel is not None:
                self.output_node.set_image(r_channel)
                self.update_preview(r_channel)

    def update_preview_from_blur(self):  # Add the method to update preview after applying blur
        if self.blur_node:
            output = self.blur_node.get_output()
            if output is not None:
                self.output_node.set_image(output)
                self.update_preview(output)

    def update_preview(self, img):
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        q_img = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectRatioMode=1))


