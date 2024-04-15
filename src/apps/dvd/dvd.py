from api.base import Base
from rgbmatrix import RGBMatrix

from PIL import Image
from io import BytesIO
from base64 import b64decode
from random import randint
import numpy as np

DVD_LOGO = "iVBORw0KGgoAAAANSUhEUgAAAA8AAAAJCAYAAADtj3ZXAAAAQUlEQVQokWNgwA3+I2Fc8hgK/iPR//HwMWxhYMBuEDZDcSpCNwiX4VhdgK4AlxiKBnRMUB5fiBJyIUHnE6WQZJsBSnw7xZmNBscAAAAASUVORK5CYII="


class DVD(Base):
    def __init__(self, matrix: RGBMatrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.dvd_logo = Image.open(BytesIO(b64decode(DVD_LOGO.encode()))).convert(
            "RGBA"
        )
        self.x = randint(0, 64)
        self.y = randint(0, 32)

    def run(self) -> bool:
        self.offscreen_canvas.Clear()
        self.offscreen_canvas.SetImage(self.get_logo(), self.x, self.y)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        self.sleep(15 * 1000)
        return True

    def get_logo(self) -> Image:
        data = np.array(self.dvd_logo)
        red, green, blue, _ = data.T
        black_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][black_areas.T] = (255, 255, 255)

        return Image.fromarray(data).convert("RGB")
