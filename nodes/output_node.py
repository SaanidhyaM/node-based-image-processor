from core.node import BaseNode
import cv2

class OutputNode(BaseNode):
    def __init__(self):
        super().__init__("Output")

    def save_image(self, image, filename, format="PNG"):
        if image is not None:
            cv2.imwrite(filename, image)

