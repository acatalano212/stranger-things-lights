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
    # Row 1: A-H
    'A': 0,
    'B': 3,
    'C': 6,
    'D': 9,
    'E': 12,
    'F': 15,
    'G': 18,
    'H': 21,
    # Row 2: I-P
    'I': 25,
    'J': 28,
    'K': 31,
    'L': 34,
    'M': 37,
    'N': 40,
    'O': 43,
    'P': 46,
    # Row 3: Q-Z
    'Q': 50,
    'R': 53,
    'S': 56,
    'T': 59,
    'U': 62,
    'V': 65,
    'W': 68,
    'X': 71,
    'Y': 74,
    'Z': 77,
}

# Default message that plays every MESSAGE_INTERVAL seconds
DEFAULT_MESSAGE = "RUN WILL RUN"

# Seconds between automatic message displays
MESSAGE_INTERVAL = 300  # 5 minutes

# How many times a custom message plays before reverting to default
CUSTOM_MESSAGE_PLAYS = 2

# Total number of LEDs on the string
NUM_LEDS = 100

# GPIO pin for LED data (must be PWM-capable: GPIO 18 = PWM0)
LED_PIN = 18

# LED strip type and color order
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 200  # 0-255
LED_INVERT = False
LED_CHANNEL = 0

# GPIO pin for PIR motion sensor (optional)
PIR_PIN = 17

# Motion sensor cooldown (seconds)
MOTION_COOLDOWN = 30
