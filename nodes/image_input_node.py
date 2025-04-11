from core.node import BaseNode
import cv2
from PyQt5.QtGui import QImage, QPixmap

class ImageInputNode(BaseNode):
    def __init__(self, path=None):
        super().__init__("Image Input")
        self.image = None
        self.metadata = None
        if path:
            self.load_image(path)

    def load_image(self, path):
        self.image = cv2.imread(path)
        if self.image is not None:
            height, width, channels = self.image.shape
            self.metadata = {
                "dimensions": (width, height),
                "channels": channels,
                "type": str(self.image.dtype)
            }

    def process(self, data=None):
        return self.image

    def get_qpixmap(self):
        if self.image is None:
            return None
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        qimage = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

