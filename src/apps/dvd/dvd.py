from api.base import Base
from rgbmatrix import RGBMatrix

from PIL import Image
from io import BytesIO
from base64 import b64decode
from random import randint

DVD_LOGO = "iVBORw0KGgoAAAANSUhEUgAAAA8AAAAJCAYAAADtj3ZXAAAAQUlEQVQokWNgwA3+I2Fc8hgK/iPR//HwMWxhYMBuEDZDcSpCNwiX4VhdgK4AlxiKBnRMUB5fiBJyIUHnE6WQZJsBSnw7xZmNBscAAAAASUVORK5CYII="


class DVD(Base):
    def __init__(self, matrix: RGBMatrix):
        super().__init__(matrix)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.dvd_logo = Image.open(BytesIO(b64decode(DVD_LOGO.encode()))).convert("RGB")
        self.x = randint(0, 64)
        self.y = randint(0, 32)

    def run(self) -> bool:
        self.offscreen_canvas.Clear()
        self.offscreen_canvas.SetImage(self.dvd_logo, self.x, self.y)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

        self.sleep(15 * 1000)
        return True
