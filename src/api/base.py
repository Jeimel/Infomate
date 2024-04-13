import argparse
import time
import sys
import os

from rgbmatrix import RGBMatrix, graphics
import config


class Base:
    def __init__(self, matrix: RGBMatrix):
        self.matrix = matrix

    def msleep(self, value: float):
        time.sleep(value / 1_000.0)

    def run(self):
        pass

    def process(self):
        try:
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

    @staticmethod
    def get_font(name: str):
        font = graphics.Font()
        font.LoadFont(f"../rpi-rgb-led-matrix/fonts/{name}.bdf")

        return font
