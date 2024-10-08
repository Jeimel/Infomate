from api.base import Base
from rgbmatrix import FrameCanvas, graphics

from PIL import Image
from datetime import datetime
from io import BytesIO
from base64 import b64decode
from os import getenv


DEFAULT_IMAGE = "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"
FONT_NAME = "6x10"


class Clock(Base):
    def __init__(self, canvas: FrameCanvas):
        super().__init__(canvas)
        self.font = Base.get_font(FONT_NAME)
        self.text_color = graphics.Color(255, 255, 255)
        self.image = (
            Image.open(
                BytesIO(
                    b64decode(getenv("CLOCK_PHOTO", default=DEFAULT_IMAGE).encode())
                )
            )
            .convert("RGB")
            .resize((22, 22))
        )

    def run(self) -> bool:
        self.canvas.SetImage(self.image, 4, 5)
        graphics.DrawText(
            self.canvas,
            self.font,
            31,
            19,
            self.text_color,
            Clock.get_time_formatted(),
        )

        self.sleep((60 - datetime.now().second) * 1000)
        return True

    @staticmethod
    def env() -> bool:
        return True

    @staticmethod
    def variables() -> list:
        return ["PHOTO"]

    @staticmethod
    def get_time_formatted() -> str:
        return datetime.now().strftime("%H:%M")
