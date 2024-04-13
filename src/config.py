# Display rows. Default: 32
LED_ROWS = 32
# Display columns. Default: 32
LED_COLS = 64
# Daisy-chained boards. Default: 1
CHAIN_LENGTH = 1
# For Plus-models or RPi2: parallel chains. 1..3. Default: 1
LED_PARALLEL = 1
# Bits used for PWM. Something between 1..11. Default: 11
LED_PWN_BITS = 11
# Sets brightness level. Range: 1..100. Default: 100.
LED_BRIGHTNESS = 60
# Hardware Mapping: "regular", "regular-pi1", "adafruit-hat", "adafruit-hat-pwm". Default: "regular"
LED_GPIO_MAPPING = "regular"
# Progressive or interlaced scan. 0 Progressive, 1 Interlaced. Default: 1
LED_SCAN_MODE = 1
# Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130
LED_PWM_LSB_NANOSECONDS = 130
# Shows the current refresh rate of the LED panel.
LED_SHOW_REFRESH = False
# Slow down writing to GPIO. Range: 0..4. Default: 1
LED_SLOWDOWN_GPIO = 1
# Don't use hardware pin-pulse generation.
LED_NO_HARDWARE_PULSE = True
# Switch if your matrix has led colors swapped. Default: RGB
LED_RGB_SEQUENCE = "RGB"
# Apply pixel mappers. e.g "Rotate:90". Default: ""
LED_PIXEL_MAPPER = ""
# 0 = default; 1=AB-addressed panels; 2=row direct; 3=ABC-addressed panels; 4 = ABC Shift + DE direct. Default: 0
LED_ROW_ADDR_TYPE = 0
# Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven. Default: 0
LED_MULTIPLEXING = 0
# Needed to initialize special panels. Supported: 'FM6126A'. Default: ""
LED_PANEL_TYPE = ""
# Don't drop privileges from 'root' after initializing the hardware.
LED_NO_DROP_PRIVILEGES = False
