"""LED effects for WS2811 via MicroPython neopixel."""
import time
import random
import neopixel
from machine import Pin
import config

LED_PIN = 1   # GPIO1 = D0 on XIAO ESP32-S3
NUM_LEDS = 100

CHRISTMAS_COLORS = [
    (255, 0, 0),      # red
    (0, 150, 0),      # green
    (0, 0, 255),      # blue
    (255, 200, 0),    # yellow
    (150, 0, 255),    # purple
]

LETTER_COLOR = (255, 255, 180)
FLICKER_DIM = (40, 15, 0)

strip = None


def init_strip():
    global strip
    strip = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS, timing=1)
    clear()
    return strip


def clear():
    for i in range(NUM_LEDS):
        strip[i] = (0, 0, 0)
    strip.write()


def set_all(r, g, b):
    for i in range(NUM_LEDS):
        strip[i] = (r, g, b)
    strip.write()


# ── Idle Animation ──────────────────────────────────────────────

class ChristmasIdle:
    def __init__(self):
        self.base_colors = [
            CHRISTMAS_COLORS[i % len(CHRISTMAS_COLORS)] for i in range(NUM_LEDS)
        ]
        self.brightness = [random.uniform(0.5, 1.0) for _ in range(NUM_LEDS)]
        self.target = list(self.brightness)
        self._apply()

    def _apply(self):
        for i in range(NUM_LEDS):
            r, g, b = self.base_colors[i]
            m = self.brightness[i]
            strip[i] = (int(r * m), int(g * m), int(b * m))
        strip.write()

    def step(self):
        for _ in range(random.randint(1, 4)):
            idx = random.randint(0, NUM_LEDS - 1)
            if random.random() < 0.5:
                self.target[idx] = random.uniform(0.8, 1.0)
            else:
                self.target[idx] = random.uniform(0.2, 0.5)

        for i in range(NUM_LEDS):
            diff = self.target[i] - self.brightness[i]
            self.brightness[i] += diff * 0.15

        if random.random() < 0.02:
            idx = random.randint(0, NUM_LEDS - 1)
            self.base_colors[idx] = random.choice(CHRISTMAS_COLORS)

        self._apply()


# ── Effects ─────────────────────────────────────────────────────

def flicker_transition(duration=2.0):
    end = time.ticks_add(time.ticks_ms(), int(duration * 1000))
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        if random.random() < 0.4:
            for i in range(NUM_LEDS):
                if random.random() < 0.3:
                    r, g, b = FLICKER_DIM
                    m = random.uniform(1.0, 3.0)
                    strip[i] = (min(255, int(r * m)), min(255, int(g * m)), min(255, int(b * m)))
                else:
                    strip[i] = (0, 0, 0)
        else:
            for i in range(NUM_LEDS):
                if random.random() < 0.1:
                    strip[i] = FLICKER_DIM
                else:
                    strip[i] = (0, 0, 0)
        strip.write()
        time.sleep_ms(random.randint(30, 150))
    clear()
    time.sleep_ms(500)


def spell_message(message):
    message = message.upper()
    letter_map = config.get_letter_map()

    for char in message:
        if char == ' ':
            time.sleep_ms(800)
            continue
        if char not in letter_map:
            continue

        idx = letter_map[char]
        r, g, b = LETTER_COLOR

        # Flicker before lighting
        for _ in range(random.randint(2, 4)):
            br = random.uniform(0.1, 0.5)
            strip[idx] = (int(r * br), int(g * br), int(b * br))
            strip.write()
            time.sleep_ms(random.randint(40, 100))
            strip[idx] = (0, 0, 0)
            strip.write()
            time.sleep_ms(random.randint(30, 80))

        # Full brightness
        strip[idx] = (r, g, b)
        strip.write()
        time.sleep_ms(600)

        # Fade out
        for s in range(10):
            m = 1.0 - (s / 10)
            strip[idx] = (int(r * m), int(g * m), int(b * m))
            strip.write()
            time.sleep_ms(30)

        strip[idx] = (0, 0, 0)
        strip.write()
        time.sleep_ms(200)


def display_message(message):
    flicker_transition(2.0)
    time.sleep_ms(300)
    spell_message(message)
    time.sleep_ms(500)
    flicker_transition(1.5)


def flash_led(index, duration_ms=3000):
    """Flash a single LED white for identification."""
    old = strip[index]
    strip[index] = (255, 255, 255)
    strip.write()
    time.sleep_ms(duration_ms)
    strip[index] = old
    strip.write()
