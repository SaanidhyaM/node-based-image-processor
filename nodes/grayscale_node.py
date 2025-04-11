from core.node import BaseNode
import cv2

class GrayscaleNode(BaseNode):
    def __init__(self):
        super().__init__("Grayscale")

    def process(self, image):
        if image is not None:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            return gray_bgr
        return image

    def get_output(self):
        return self.process(self.input_nodes[0].get_output() if self.input_nodes else None)
