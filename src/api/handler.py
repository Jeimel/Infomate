from asyncio import sleep, create_task, CancelledError

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from apps.clock.clock import Clock
import config


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
        self.timer = None

    async def start(self):
        while True:
            if self.next:
                self.app = self.next(self.app.canvas)
                self.next = None

            self.app.canvas.Clear()
            self.app.run()
            self.app.canvas = self.matrix.SwapOnVSync(self.app.canvas)
            self.timer = create_task(self.delay())

            try:
                await self.timer
            except CancelledError or KeyboardInterrupt:
                continue

    async def delay(self):
        try:
            await sleep(self.app.delay / 1_000.0)
        except CancelledError:
            raise

    def set_next(self, next: type):
        self.next = next
        if self.timer:
            self.timer.cancel()
