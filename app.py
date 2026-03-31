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
import functools
from queue import Queue, Empty

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from letter_map import (
    DEFAULT_MESSAGE, MESSAGE_INTERVAL, CUSTOM_MESSAGE_PLAYS,
    NUM_LEDS, PIR_PIN, MOTION_COOLDOWN,
)
from led_effects import (
    ChristmasIdle, create_strip, display_message, motion_spook, clear,
)
import config

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

# Reference to the LED strip (set in main, used by admin test-led)
_strip = None

# Admin password
ADMIN_PASSWORD = "utgst"

# ── Optional: PIR Sensor ────────────────────────────────────────

PIR_AVAILABLE = False

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    PIR_AVAILABLE = True
    log.info(f"PIR sensor ready on GPIO {PIR_PIN}")
except Exception as e:
    log.warning(f"PIR sensor not available: {e}")

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
        default_msg = config.get_default_message()
        interval = config.get_message_interval()
        if now - last_message_time >= interval:
            log.info(f"Scheduled message: '{default_msg}'")
            current_status["state"] = "message"
            current_status["message"] = default_msg

            with led_lock:
                display_message(strip, default_msg)

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
app.secret_key = os.urandom(24)


# ── Admin Auth Helper ───────────────────────────────────────────

def admin_required(f):
    """Decorator: require admin login via session cookie."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            if request.is_json:
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper

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

# ── Admin Routes ────────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        pw = request.form.get("password", "")
        if pw == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_page"))
        return render_template("admin_login.html", error="Wrong password")
    return render_template("admin_login.html", error=None)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin_page():
    return render_template("admin.html")


@app.route("/api/admin/config", methods=["GET"])
@admin_required
def api_admin_get_config():
    return jsonify(config.get_all())


@app.route("/api/admin/config", methods=["POST"])
@admin_required
def api_admin_set_config():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    try:
        config.update_all(data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/admin/test-led", methods=["POST"])
@admin_required
def api_admin_test_led():
    data = request.get_json()
    if not data or "led_index" not in data:
        return jsonify({"error": "No led_index provided"}), 400

    idx = int(data["led_index"])
    if idx < 0 or idx >= NUM_LEDS:
        return jsonify({"error": f"LED index must be 0-{NUM_LEDS - 1}"}), 400

    def flash_led():
        if _strip is None:
            return
        with led_lock:
            old_color = _strip[idx]
            _strip[idx] = (255, 255, 255)
            _strip.show()
            time.sleep(3)
            _strip[idx] = old_color
            _strip.show()

    threading.Thread(target=flash_led, daemon=True).start()
    return jsonify({"success": True, "led_index": idx})

# ── Main ────────────────────────────────────────────────────────

def main():
    global _strip
    log.info("=" * 50)
    log.info("Stranger Things Wall Lights")
    log.info("=" * 50)

    # Check for root (required by neopixel for DMA access)
    if os.geteuid() != 0:
        log.error("Must run as root (sudo) for LED control!")
        sys.exit(1)

    # Load persistent config (letter map, default message, etc.)
    config.load()

    # Initialize LED strip
    strip = create_strip()
    _strip = strip
    log.info(f"LED strip initialized: {NUM_LEDS} LEDs on GPIO 18")

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
