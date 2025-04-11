from core.node import BaseNode
import cv2

class OutputNode(BaseNode):
    def __init__(self):
        super().__init__("Output")
        self.image = None

    def set_image(self, image):
        self.image = image

    def save_image(self, filename, format="PNG"):
        if self.image is not None:
            cv2.imwrite(filename, self.image)
