from rgbmatrix import FrameCanvas, graphics


class Base:
    def __init__(self, canvas: FrameCanvas):
        self.canvas = canvas
        self.delay = 1000

    def sleep(self, value: float):
        self.delay = value

    def run(self) -> bool:
        return False

    @staticmethod
    def env() -> bool:
        return False

    @staticmethod
    def variables() -> list:
        return []

    @staticmethod
    def get_font(name: str) -> graphics.Font:
        font = graphics.Font()
        font.LoadFont(f"../rpi-rgb-led-matrix/fonts/{name}.bdf")

        return font
