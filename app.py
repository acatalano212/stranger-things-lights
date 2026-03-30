"""
Stranger Things Wall Lights — Main Application

Runs on Raspberry Pi 3B+ with WS2811 LED string.
- Christmas light idle animation
- Periodic message display (default: "RUN WILL RUN" every 5 min)
- Flask web server for custom messages via QR code
- Optional PIR motion sensor + sound effects
"""

import os
import sys
import time
import threading
import logging
from queue import Queue, Empty

from rpi_ws281x import PixelStrip
from flask import Flask, render_template, request, jsonify

from letter_map import (
    DEFAULT_MESSAGE, MESSAGE_INTERVAL, CUSTOM_MESSAGE_PLAYS,
    NUM_LEDS, LED_PIN, LED_FREQ_HZ, LED_DMA,
    LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL,
    PIR_PIN, MOTION_COOLDOWN,
)
from led_effects import (
    ChristmasIdle, display_message, motion_spook, clear,
)

# ── Logging ─────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("stranger-things")

# ── Global State ────────────────────────────────────────────────

# Thread-safe queue for custom messages from the web UI
message_queue = Queue()

# Lock to prevent concurrent LED access
led_lock = threading.Lock()

# Flag to signal the LED thread to stop
shutdown_event = threading.Event()

# Current status for the web UI
current_status = {"state": "idle", "message": ""}

# ── Optional: PIR Sensor + Audio ────────────────────────────────

PIR_AVAILABLE = False
AUDIO_AVAILABLE = False

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    PIR_AVAILABLE = True
    log.info(f"PIR sensor ready on GPIO {PIR_PIN}")
except Exception as e:
    log.warning(f"PIR sensor not available: {e}")

try:
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
    log.info("Audio system ready")
except Exception as e:
    log.warning(f"Audio not available: {e}")

# ── Sound Effects ───────────────────────────────────────────────

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

def play_sound(filename):
    """Play a sound file if audio is available."""
    if not AUDIO_AVAILABLE:
        return
    filepath = os.path.join(SOUNDS_DIR, filename)
    if os.path.exists(filepath):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            log.info(f"Playing sound: {filename}")
        except Exception as e:
            log.warning(f"Failed to play {filename}: {e}")

# ── LED Control Thread ──────────────────────────────────────────

def led_thread(strip):
    """
    Main LED control loop. Runs idle animation, handles scheduled
    messages, custom messages from the queue, and motion events.
    """
    log.info("LED thread started")
    idle = ChristmasIdle(strip)
    last_message_time = time.time()
    last_motion_time = 0

    while not shutdown_event.is_set():
        now = time.time()

        # Check for custom messages from web UI
        try:
            custom_msg = message_queue.get_nowait()
            log.info(f"Custom message received: '{custom_msg}'")
            current_status["state"] = "message"
            current_status["message"] = custom_msg

            with led_lock:
                play_sound("flicker.wav")
                for play in range(CUSTOM_MESSAGE_PLAYS):
                    log.info(f"  Playing custom message ({play + 1}/{CUSTOM_MESSAGE_PLAYS})")
                    display_message(strip, custom_msg)
                    if play < CUSTOM_MESSAGE_PLAYS - 1:
                        time.sleep(1.0)

            # Reset idle state and timer
            idle = ChristmasIdle(strip)
            last_message_time = time.time()
            current_status["state"] = "idle"
            current_status["message"] = ""
            continue
        except Empty:
            pass

        # Check for scheduled default message
        if now - last_message_time >= MESSAGE_INTERVAL:
            log.info(f"Scheduled message: '{DEFAULT_MESSAGE}'")
            current_status["state"] = "message"
            current_status["message"] = DEFAULT_MESSAGE

            with led_lock:
                play_sound("flicker.wav")
                display_message(strip, DEFAULT_MESSAGE)

            idle = ChristmasIdle(strip)
            last_message_time = time.time()
            current_status["state"] = "idle"
            current_status["message"] = ""
            continue

        # Check PIR motion sensor
        if PIR_AVAILABLE and (now - last_motion_time >= MOTION_COOLDOWN):
            if GPIO.input(PIR_PIN):
                log.info("Motion detected!")
                last_motion_time = now
                current_status["state"] = "motion"

                with led_lock:
                    play_sound("upside_down.wav")
                    motion_spook(strip)

                idle = ChristmasIdle(strip)
                current_status["state"] = "idle"
                continue

        # Normal idle animation
        with led_lock:
            idle.step()

        time.sleep(0.05)  # ~20 FPS idle animation

    # Clean shutdown
    clear(strip)
    log.info("LED thread stopped")

# ── Flask Web Server ────────────────────────────────────────────

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    return jsonify(current_status)

@app.route("/api/message", methods=["POST"])
def api_message():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    msg = data["message"].upper().strip()

    # Validate: A-Z and spaces only
    if not all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ " for c in msg):
        return jsonify({"error": "Only letters A-Z and spaces allowed"}), 400

    if len(msg) == 0:
        return jsonify({"error": "Message cannot be empty"}), 400

    if len(msg) > 50:
        return jsonify({"error": "Message too long (max 50 characters)"}), 400

    if not message_queue.empty():
        return jsonify({"error": "A message is already queued — wait for it to finish"}), 429

    message_queue.put(msg)
    log.info(f"Message queued from web: '{msg}'")
    return jsonify({"success": True, "message": msg})

# ── Main ────────────────────────────────────────────────────────

def main():
    log.info("=" * 50)
    log.info("Stranger Things Wall Lights")
    log.info("=" * 50)

    # Check for root (required by rpi_ws281x for DMA access)
    if os.geteuid() != 0:
        log.error("Must run as root (sudo) for LED control!")
        sys.exit(1)

    # Initialize LED strip
    strip = PixelStrip(
        NUM_LEDS, LED_PIN, LED_FREQ_HZ,
        LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
    )
    strip.begin()
    log.info(f"LED strip initialized: {NUM_LEDS} LEDs on GPIO {LED_PIN}")

    # Start LED control thread
    led_t = threading.Thread(target=led_thread, args=(strip,), daemon=True)
    led_t.start()

    # Start Flask web server
    log.info("Starting web server on port 80...")
    try:
        app.run(host="0.0.0.0", port=80, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        log.info("Shutting down...")
        shutdown_event.set()
        led_t.join(timeout=5)
        clear(strip)
        if PIR_AVAILABLE:
            GPIO.cleanup()
        log.info("Goodbye!")


if __name__ == "__main__":
    main()
