import time
import sys

from rgbmatrix import RGBMatrix, graphics


class Base:
    def __init__(self, matrix: RGBMatrix):
        self.matrix = matrix
        self.delay = 1000

    def sleep(self, value: float):
        self.delay = value

    def run(self):
        pass

    @staticmethod
    def get_font(name: str):
        font = graphics.Font()
        font.LoadFont(f"../rpi-rgb-led-matrix/fonts/{name}.bdf")

        return font
