from core.node import BaseNode
import cv2

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

