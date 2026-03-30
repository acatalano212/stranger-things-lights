"""
LED effects for Stranger Things Wall Lights.

All effects operate on a rpi_ws281x PixelStrip instance.
Effects are designed to be called from the main loop and block
until the effect completes (the main app runs them in a thread).
"""

import time
import random
from rpi_ws281x import Color
from letter_map import LETTER_MAP, NUM_LEDS


# ── Color Palettes ──────────────────────────────────────────────

# Warm Christmas light colors (R, G, B)
CHRISTMAS_COLORS = [
    (255, 30, 0),    # warm red
    (0, 180, 0),     # green
    (255, 170, 0),   # warm gold/amber
    (0, 80, 255),    # blue
    (255, 80, 0),    # orange
    (200, 0, 80),    # magenta/pink
    (0, 200, 100),   # teal
    (255, 255, 80),  # warm white/yellow
]

# Letter highlight color — bright warm white with a slight yellow tint
LETTER_COLOR = (255, 255, 180)

# Dim flicker color — faint warm glow
FLICKER_DIM = (40, 15, 0)


# ── Helper Functions ────────────────────────────────────────────

def color(r, g, b):
    """Create a Color from RGB tuple."""
    return Color(r, g, b)


def set_all(strip, r, g, b):
    """Set all LEDs to the same color."""
    c = Color(r, g, b)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, c)
    strip.show()


def clear(strip):
    """Turn off all LEDs."""
    set_all(strip, 0, 0, 0)


# ── Idle Animation: Christmas Lights ───────────────────────────

class ChristmasIdle:
    """
    Manages the idle Christmas light animation state.
    Each LED gets a random warm color. Periodically, random LEDs
    twinkle (briefly brighten then dim back).
    """

    def __init__(self, strip):
        self.strip = strip
        self.num = strip.numPixels()
        # Assign a random Christmas color to each LED
        self.base_colors = [
            random.choice(CHRISTMAS_COLORS) for _ in range(self.num)
        ]
        # Current brightness multiplier per LED (0.0 - 1.0)
        self.brightness = [
            random.uniform(0.5, 1.0) for _ in range(self.num)
        ]
        # Target brightness (for smooth transitions)
        self.target = list(self.brightness)
        self._apply()

    def _apply(self):
        """Push current state to the LED strip."""
        for i in range(self.num):
            r, g, b = self.base_colors[i]
            m = self.brightness[i]
            self.strip.setPixelColor(i, Color(int(r * m), int(g * m), int(b * m)))
        self.strip.show()

    def step(self):
        """
        Advance one animation frame. Call this in a loop with ~50ms delay.
        Returns immediately — non-blocking.
        """
        # Pick a few random LEDs to twinkle
        for _ in range(random.randint(1, 4)):
            idx = random.randint(0, self.num - 1)
            # Randomly brighten or dim
            if random.random() < 0.5:
                self.target[idx] = random.uniform(0.8, 1.0)
            else:
                self.target[idx] = random.uniform(0.2, 0.5)

        # Smoothly move brightness toward target
        for i in range(self.num):
            diff = self.target[i] - self.brightness[i]
            self.brightness[i] += diff * 0.15  # easing factor

        # Occasionally reassign a color to keep it interesting
        if random.random() < 0.02:
            idx = random.randint(0, self.num - 1)
            self.base_colors[idx] = random.choice(CHRISTMAS_COLORS)

        self._apply()


# ── Dramatic Flicker Effect ────────────────────────────────────

def flicker_transition(strip, duration=2.0):
    """
    Dramatic flicker effect like a power surge / Upside Down intrusion.
    Lights stutter between dim warm glow and darkness.
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        # Random flash
        if random.random() < 0.4:
            # Brief bright flash on random subset
            for i in range(strip.numPixels()):
                if random.random() < 0.3:
                    r, g, b = FLICKER_DIM
                    m = random.uniform(1.0, 3.0)
                    strip.setPixelColor(i, Color(
                        min(255, int(r * m)),
                        min(255, int(g * m)),
                        min(255, int(b * m))
                    ))
                else:
                    strip.setPixelColor(i, Color(0, 0, 0))
        else:
            # Mostly dark with a few dim flickers
            for i in range(strip.numPixels()):
                if random.random() < 0.1:
                    strip.setPixelColor(i, Color(*FLICKER_DIM))
                else:
                    strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(random.uniform(0.03, 0.15))

    clear(strip)
    time.sleep(0.5)


# ── Spell Message Letter by Letter ─────────────────────────────

def spell_message(strip, message):
    """
    Spell out a message one letter at a time.
    Each letter's mapped LED lights up bright, holds, then dims.
    Spaces create a longer pause (like word gaps in the show).
    """
    message = message.upper()

    for char in message:
        if char == ' ':
            # Word gap — brief darkness
            time.sleep(0.8)
            continue

        if char not in LETTER_MAP:
            continue  # skip unmapped characters

        led_idx = LETTER_MAP[char]
        r, g, b = LETTER_COLOR

        # Quick flicker before lighting the letter (like the bulb struggling)
        for _ in range(random.randint(2, 4)):
            brightness = random.uniform(0.1, 0.5)
            strip.setPixelColor(led_idx, Color(
                int(r * brightness), int(g * brightness), int(b * brightness)
            ))
            strip.show()
            time.sleep(random.uniform(0.04, 0.1))
            strip.setPixelColor(led_idx, Color(0, 0, 0))
            strip.show()
            time.sleep(random.uniform(0.03, 0.08))

        # Light up the letter fully
        strip.setPixelColor(led_idx, Color(r, g, b))
        strip.show()
        time.sleep(0.6)

        # Fade out the letter
        steps = 10
        for s in range(steps):
            m = 1.0 - (s / steps)
            strip.setPixelColor(led_idx, Color(int(r * m), int(g * m), int(b * m)))
            strip.show()
            time.sleep(0.03)

        strip.setPixelColor(led_idx, Color(0, 0, 0))
        strip.show()
        time.sleep(0.2)


# ── Full Message Display Sequence ──────────────────────────────

def display_message(strip, message):
    """
    Complete message display sequence:
    1. Flicker transition (entering the Upside Down)
    2. Spell the message letter by letter
    3. Brief pause
    4. Flicker transition out
    """
    flicker_transition(strip, duration=2.0)
    time.sleep(0.3)
    spell_message(strip, message)
    time.sleep(0.5)
    flicker_transition(strip, duration=1.5)


# ── Motion Trigger Effect ──────────────────────────────────────

def motion_spook(strip, duration=3.0):
    """
    Triggered by PIR sensor — rapid chaotic flickering like
    the Upside Down is breaking through. More intense than
    the normal flicker transition.
    """
    end_time = time.time() + duration

    while time.time() < end_time:
        # Intense random strobing
        for i in range(strip.numPixels()):
            if random.random() < 0.2:
                # Random color flash — reds and cold whites
                if random.random() < 0.5:
                    strip.setPixelColor(i, Color(
                        random.randint(150, 255),
                        random.randint(0, 30),
                        random.randint(0, 20)
                    ))
                else:
                    v = random.randint(100, 255)
                    strip.setPixelColor(i, Color(v, v, v))
            else:
                strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(random.uniform(0.02, 0.08))

    # Fade out
    for step in range(20):
        m = 1.0 - (step / 20)
        for i in range(strip.numPixels()):
            c = strip.getPixelColor(i)
            r = int(((c >> 16) & 0xFF) * m)
            g = int(((c >> 8) & 0xFF) * m)
            b = int((c & 0xFF) * m)
            strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        time.sleep(0.04)

    clear(strip)
