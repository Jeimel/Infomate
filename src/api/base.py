import time
import sys

from rgbmatrix import FrameCanvas, graphics, Font


class Base:
    def __init__(self, canvas: FrameCanvas):
        self.canvas = canvas
        self.delay = 1000

    def sleep(self, value: float):
        self.delay = value

    def run(self) -> bool:
        pass

    @staticmethod
    def get_font(name: str) -> Font:
        font = graphics.Font()
        font.LoadFont(f"../rpi-rgb-led-matrix/fonts/{name}.bdf")

        return font
