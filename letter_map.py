"""
Letter-to-LED mapping for Stranger Things Wall Lights.

Each letter A-Z maps to an LED index (0-99) on the WS2811 string.
Update these values after mounting the lights on the wall — measure
which LED sits above each letter and record the index here.

The show uses 3 rows of letters on the wall:
  Row 1: A B C D E F G H
  Row 2: I J K L M N O P
  Row 3: Q R S T U V W X Y Z
"""

# Map each letter to the LED index directly above it.
# Placeholder indices — UPDATE after measuring your actual installation.
LETTER_MAP = {
    # Row 1: A-H (LEDs 0-7)
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    # Row 2: I-P (LEDs 8-15)
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    # Row 3: Q-Z (LEDs 16-25)
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19,
    'U': 20,
    'V': 21,
    'W': 22,
    'X': 23,
    'Y': 24,
    'Z': 25,
}

# Default message that plays every MESSAGE_INTERVAL seconds
DEFAULT_MESSAGE = "RUN WILL RUN"

# Seconds between automatic message displays
MESSAGE_INTERVAL = 60  # 1 minute (for testing, change to 300 for production)

# How many times a custom message plays before reverting to default
CUSTOM_MESSAGE_PLAYS = 2

# Total number of LEDs on the string
NUM_LEDS = 50

# GPIO pin for LED data (must be PWM-capable: GPIO 18 = PWM0)
LED_PIN = 18

# LED strip type and color order
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 200  # 0-255
LED_INVERT = False
LED_CHANNEL = 0

# LED strip type — change if colors look wrong
# Options: WS2811_STRIP_RGB, WS2811_STRIP_GRB, WS2811_STRIP_BRG
LED_STRIP_TYPE = 'GRB'

# GPIO pin for PIR motion sensor (optional)
PIR_PIN = 17

# Motion sensor cooldown (seconds)
MOTION_COOLDOWN = 30
