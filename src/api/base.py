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

    @staticmethod
    def hex_to_rgb(hex: str) -> tuple:
        return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def draw_rect(
        canvas: FrameCanvas,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        color: tuple[int, int, int],
    ):
        assert x0 < x1 and y0 < y1 and x0 + x1 < 64 and y0 + y1 < 64

        for y in range(y0, y1):
            for x in range(x0, x1):
                canvas.setPixel(x, y, color[0], color[1], color[2])
