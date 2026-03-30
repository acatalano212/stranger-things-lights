"""
Sound effects via audio output for Stranger Things Wall Lights.

Uses the Pi's audio output (3.5mm or HDMI) through a PAM8403
amplifier board to drive a 3W/8Ω speaker. Generates tones
programmatically using the wave module — no external .wav files needed.

Wiring:
  Pi 3.5mm jack → PAM8403 input (L or R + GND)
  PAM8403 output → Speaker (via JST or solder)
  PAM8403 VCC → Pi 5V (Pin 2)
  PAM8403 GND → Pi GND (Pin 6)
"""

import os
import math
import wave
import struct
import tempfile
import subprocess
import threading

_lock = threading.Lock()
AUDIO_AVAILABLE = False
SAMPLE_RATE = 22050


def init_audio():
    """Check if aplay is available."""
    global AUDIO_AVAILABLE
    try:
        result = subprocess.run(
            ["aplay", "--version"],
            capture_output=True, timeout=5
        )
        AUDIO_AVAILABLE = result.returncode == 0
        return AUDIO_AVAILABLE
    except Exception:
        return False


def _generate_wav(samples):
    """Write samples to a temp .wav file and return the path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for s in samples:
            clamped = max(-32767, min(32767, int(s * 32767)))
            wf.writeframes(struct.pack('<h', clamped))
    return tmp.name


def _play_wav(filepath):
    """Play a .wav file with aplay and then delete it."""
    try:
        subprocess.run(
            ["aplay", "-q", filepath],
            timeout=15, capture_output=True
        )
    except Exception:
        pass
    finally:
        try:
            os.unlink(filepath)
        except Exception:
            pass


def _play_samples(samples):
    """Generate wav from samples and play it."""
    if not AUDIO_AVAILABLE:
        return
    path = _generate_wav(samples)
    _play_wav(path)


def _tone_samples(freq, duration, volume=0.6):
    """Generate sine wave samples."""
    n = int(SAMPLE_RATE * duration)
    return [volume * math.sin(2 * math.pi * freq * i / SAMPLE_RATE) for i in range(n)]


def _sweep_samples(start_freq, end_freq, duration, volume=0.6):
    """Generate a frequency sweep."""
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / n
        freq = start_freq + (end_freq - start_freq) * t
        samples.append(volume * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))
    return samples


def _noise_samples(duration, volume=0.3):
    """Generate crackly noise."""
    import random
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        if random.random() < 0.15:
            samples.append(volume * random.uniform(-1, 1))
        else:
            samples.append(0.0)
    return samples


def _silence_samples(duration):
    """Generate silence."""
    return [0.0] * int(SAMPLE_RATE * duration)


# ── Public Sound Effects ────────────────────────────────────────

def play_flicker_sound():
    """Electrical buzzing/flickering for message transitions."""
    with _lock:
        samples = []
        # Electrical buzz — low frequency with harmonics
        for i in range(int(SAMPLE_RATE * 0.8)):
            t = i / SAMPLE_RATE
            s = 0.4 * math.sin(2 * math.pi * 60 * i / SAMPLE_RATE)
            s += 0.2 * math.sin(2 * math.pi * 120 * i / SAMPLE_RATE)
            s += 0.1 * math.sin(2 * math.pi * 180 * i / SAMPLE_RATE)
            # Amplitude modulation for stuttering effect
            mod = 0.5 + 0.5 * math.sin(2 * math.pi * 8 * t)
            samples.append(s * mod)
        # Descending sweep
        samples += _sweep_samples(200, 40, 0.5, volume=0.5)
        # Crackle
        samples += _noise_samples(0.3, volume=0.4)
        _play_samples(samples)


def play_letter_sound(char):
    """Short tone when a letter lights up."""
    with _lock:
        if char.isalpha():
            idx = ord(char.upper()) - ord('A')
            freq = 200 + (idx * 15)
            samples = _tone_samples(freq, 0.08, volume=0.5)
            _play_samples(samples)


def play_spook_sound():
    """Motion-triggered Upside Down ambience."""
    with _lock:
        samples = []
        # Deep rumble
        samples += _sweep_samples(60, 25, 1.0, volume=0.6)
        samples += _silence_samples(0.1)
        # Eerie ascending whine
        samples += _sweep_samples(80, 900, 1.5, volume=0.5)
        samples += _silence_samples(0.05)
        # Crackle burst
        samples += _noise_samples(0.5, volume=0.5)
        # Descending moan
        samples += _sweep_samples(400, 30, 1.2, volume=0.5)
        _play_samples(samples)


def play_startup_sound():
    """Ascending chime on boot."""
    with _lock:
        samples = []
        for freq in [220, 330, 440, 550]:
            samples += _tone_samples(freq, 0.12, volume=0.4)
            samples += _silence_samples(0.05)
        samples += _silence_samples(0.1)
        samples += _tone_samples(440, 0.25, volume=0.5)
        _play_samples(samples)


def cleanup_audio():
    """Nothing to clean up for aplay-based audio."""
    pass
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
