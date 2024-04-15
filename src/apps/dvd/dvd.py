from api.base import Base
from rgbmatrix import RGBMatrix

from PIL import Image
from io import BytesIO
from base64 import b64decode
from random import randint
import numpy as np

DVD_LOGO = "iVBORw0KGgoAAAANSUhEUgAAAA8AAAAJCAYAAADtj3ZXAAAAQUlEQVQokWNgwA3+I2Fc8hgK/iPR//HwMWxhYMBuEDZDcSpCNwiX4VhdgK4AlxiKBnRMUB5fiBJyIUHnE6WQZJsBSnw7xZmNBscAAAAASUVORK5CYII="
DVD_WIDTH = 15
DVD_HEIGHT = 9
COLORS = [
    (0, 238, 255),
    (255, 119, 0),
    (0, 34, 255),
    (255, 238, 0),
    (255, 34, 0),
    (255, 0, 136),
    (187, 0, 255),
]


class DVD(Base):
    def __init__(self, matrix: RGBMatrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.dvd_logo = Image.open(BytesIO(b64decode(DVD_LOGO.encode())))
        self.color_index = 0
        self.x = randint(0, 64)
        self.y = randint(0, 32)
        self.vel_x = 3
        self.vel_y = 3

    def run(self) -> bool:
        self.offscreen_canvas.Clear()
        self.offscreen_canvas.SetImage(self.get_logo(), self.x, self.y)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        self.x += self.vel_x
        self.y += self.vel_y

        if self.x + DVD_WIDTH >= 64:
            self.vel_x *= -1
            self.x = 64 - DVD_WIDTH
            self.change_color()
        elif self.x <= 0:
            self.vel_x *= -1
            self.x = 0
            self.change_color()

        if self.y + DVD_HEIGHT >= 32:
            self.vel_y *= -1
            self.y = 32 - DVD_HEIGHT
            self.change_color()
        elif self.y <= 0:
            self.vel_y *= -1
            self.y = 0
            self.change_color()

        self.sleep(250)
        return True

    def get_logo(self) -> Image:
        data = np.array(self.dvd_logo)
        _, _, _, alpha = data.T
        empty_areas = alpha == 0
        data[..., :-1][empty_areas.T] = COLORS[self.color_index]

        return Image.fromarray(data).convert("RGB")

    def change_color(self):
        self.color_index = (self.color_index + 1) % len(COLORS)
