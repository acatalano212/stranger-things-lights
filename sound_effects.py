"""
Sound effects via GPIO PWM for Stranger Things Wall Lights.

Drives a speaker connected through a transistor on a GPIO pin.
Generates eerie tones, frequency sweeps, and flickering buzzes
programmatically — no .wav files needed.

Wiring:
  GPIO 13 → 1kΩ resistor → NPN transistor base (e.g. 2N2222)
  Transistor collector → Speaker (−)
  Transistor emitter → GND
  5V (Pi Pin 2) → Speaker (+)
"""

import time
import random
import threading

try:
    import RPi.GPIO as GPIO
    PWM_AVAILABLE = True
except ImportError:
    PWM_AVAILABLE = False

# GPIO pin for speaker (PWM1 channel — GPIO 13 or 19)
SPEAKER_PIN = 13

_pwm = None
_lock = threading.Lock()


def init_audio():
    """Initialize the speaker GPIO pin. Call once at startup."""
    global _pwm
    if not PWM_AVAILABLE:
        return False
    try:
        GPIO.setup(SPEAKER_PIN, GPIO.OUT)
        _pwm = GPIO.PWM(SPEAKER_PIN, 440)
        return True
    except Exception:
        return False


def _tone(freq, duration):
    """Play a single tone at given frequency for duration seconds."""
    if _pwm is None:
        return
    _pwm.ChangeFrequency(max(freq, 20))
    _pwm.start(50)  # 50% duty cycle
    time.sleep(duration)
    _pwm.stop()


def _sweep(start_freq, end_freq, duration, steps=50):
    """Sweep frequency from start to end over duration."""
    if _pwm is None:
        return
    step_time = duration / steps
    for i in range(steps):
        t = i / steps
        freq = start_freq + (end_freq - start_freq) * t
        _pwm.ChangeFrequency(max(freq, 20))
        _pwm.start(50)
        time.sleep(step_time)
    _pwm.stop()


def _stutter(freq, duration, on_time=0.03, off_time=0.05):
    """Rapid stuttering tone — like a dying lightbulb buzzing."""
    if _pwm is None:
        return
    end_time = time.time() + duration
    while time.time() < end_time:
        _pwm.ChangeFrequency(max(freq + random.randint(-20, 20), 20))
        _pwm.start(50)
        time.sleep(on_time + random.uniform(0, 0.02))
        _pwm.stop()
        time.sleep(off_time + random.uniform(0, 0.03))


# ── Public Sound Effects ────────────────────────────────────────

def play_flicker_sound():
    """
    Electrical buzzing/flickering sound for message transitions.
    Like fluorescent lights stuttering in the Upside Down.
    """
    with _lock:
        if _pwm is None:
            return
        # Initial electrical buzz
        _stutter(120, 0.5, on_time=0.02, off_time=0.03)
        time.sleep(0.1)
        # Descending hum
        _sweep(200, 60, 0.4)
        time.sleep(0.05)
        # Quick stutter
        _stutter(80, 0.3, on_time=0.01, off_time=0.04)


def play_letter_sound(char):
    """
    Short tone when a letter lights up. Pitch varies by letter
    position for a musical quality.
    """
    with _lock:
        if _pwm is None:
            return
        # Map A-Z to ascending frequencies (200-600 Hz)
        if char.isalpha():
            idx = ord(char.upper()) - ord('A')
            freq = 200 + (idx * 15)
            _tone(freq, 0.08)


def play_spook_sound():
    """
    Triggered by motion sensor — unsettling Upside Down ambience.
    Low drones, eerie sweeps, and electrical crackle.
    """
    with _lock:
        if _pwm is None:
            return
        # Deep rumble
        _sweep(60, 30, 0.8)
        time.sleep(0.1)
        # Eerie ascending whine
        _sweep(100, 800, 1.2)
        time.sleep(0.05)
        # Electrical crackle
        _stutter(300, 0.6, on_time=0.01, off_time=0.02)
        time.sleep(0.1)
        # Descending moan
        _sweep(500, 40, 1.0)
        # Final stutter out
        _stutter(60, 0.4, on_time=0.02, off_time=0.06)


def play_startup_sound():
    """Short ascending tone sequence on boot — "I'm alive"."""
    with _lock:
        if _pwm is None:
            return
        for freq in [220, 330, 440, 550]:
            _tone(freq, 0.1)
            time.sleep(0.05)
        time.sleep(0.1)
        _tone(440, 0.2)


def cleanup_audio():
    """Stop PWM and clean up. Call on shutdown."""
    global _pwm
    if _pwm is not None:
        try:
            _pwm.stop()
        except Exception:
            pass
        _pwm = None
