from asyncio import sleep, create_task, CancelledError

from api.base import Base
from rgbmatrix import RGBMatrix, RGBMatrixOptions, FrameCanvas, graphics
from apps.clock.clock import Clock
from api.main import logger
import config


FONT_NAME = "6x10"
SMALL_FONT_NAME = "4x6"


class ErrorApp(Base):
    def __init__(self, canvas: FrameCanvas):
        super().__init__(canvas)
        self.font = Base.get_font(FONT_NAME)
        self.small_font = Base.get_font(SMALL_FONT_NAME)
        self.red_color = graphics.color(255, 0, 0)
        self.white_color = graphics.color(255, 255, 255)

    def run(self) -> bool:
        graphics.DrawText(
            self.canvas,
            self.font,
            14,
            5,
            self.red_color,
            "Error!",
        )
        graphics.DrawText(
            self.canvas,
            self.small_font,
            14,
            17,
            self.white_color,
            "See logs.",
        )

        self.sleep(60 * 1000)
        return True


class AppHandler:
    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = config.LED_ROWS
        options.cols = config.LED_COLS
        options.chain_length = config.CHAIN_LENGTH
        options.parallel = config.LED_PARALLEL
        options.pwm_bits = config.LED_PWN_BITS
        options.brightness = config.LED_BRIGHTNESS
        options.hardware_mapping = config.LED_GPIO_MAPPING
        options.scan_mode = config.LED_SCAN_MODE
        options.pwm_lsb_nanoseconds = config.LED_PWM_LSB_NANOSECONDS
        options.show_refresh_rate = config.LED_SHOW_REFRESH
        options.gpio_slowdown = config.LED_SLOWDOWN_GPIO
        options.disable_hardware_pulsing = config.LED_NO_HARDWARE_PULSE
        options.led_rgb_sequence = config.LED_RGB_SEQUENCE
        options.pixel_mapper_config = config.LED_PIXEL_MAPPER
        options.row_address_type = config.LED_ROW_ADDR_TYPE
        options.multiplexing = config.LED_MULTIPLEXING
        options.panel_type = config.LED_PANEL_TYPE
        options.drop_privileges = config.LED_NO_DROP_PRIVILEGES

        self.matrix = RGBMatrix(options=options)
        self.app = Clock(self.matrix.CreateFrameCanvas())
        self.next = None
        self.sleeper = None
        self.running = True

    async def start(self) -> None:
        while self.running:
            try:
                if self.next:
                    self.app = self.next(self.app.canvas)
                    self.next = None

                self.app.canvas.Clear()
                if not self.app.run():
                    raise Exception("Internal error in current app.")
                self.app.canvas = self.matrix.SwapOnVSync(self.app.canvas)
            except Exception as e:
                logger.exception(e)
                self.app = ErrorApp(self.app.canvas)
                self.next = None

            self.sleeper = create_task(self.delay())

            try:
                await self.sleeper
            except CancelledError:
                continue

    async def delay(self):
        try:
            await sleep(self.app.delay / 1_000.0)
        except CancelledError:
            raise

    def set_next(self, next: type) -> None:
        self.next = next
        if self.sleeper:
            self.sleeper.cancel()

    def update_brightness(self, brightness: int) -> None:
        self.matrix.brightness = brightness
        self.app.canvas.brightness = brightness

        if self.sleeper:
            self.sleeper.cancel()
