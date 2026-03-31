"""
Persistent configuration manager.
Stores letter map, default message, and other settings in a JSON file
so they can be updated at runtime from the admin page.
Falls back to defaults in letter_map.py if no config file exists.
"""

import json
import os
import logging

from letter_map import (
    LETTER_MAP as DEFAULT_LETTER_MAP,
    DEFAULT_MESSAGE as DEFAULT_MSG,
    MESSAGE_INTERVAL as DEFAULT_INTERVAL,
    NUM_LEDS, LED_PIN, LED_BRIGHTNESS,
)

log = logging.getLogger("stranger-things")

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# In-memory config — loaded at startup, updated by admin page
_config = {
    "letter_map": dict(DEFAULT_LETTER_MAP),
    "default_message": DEFAULT_MSG,
    "message_interval": DEFAULT_INTERVAL,
    "num_leds": NUM_LEDS,
}


def load():
    """Load config from disk. Call once at startup."""
    global _config
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                saved = json.load(f)
            _config.update(saved)
            log.info(f"Config loaded from {CONFIG_PATH}")
        except Exception as e:
            log.warning(f"Failed to load config, using defaults: {e}")
    else:
        log.info("No config.json found, using defaults from letter_map.py")


def save():
    """Persist current config to disk."""
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(_config, f, indent=2)
        log.info(f"Config saved to {CONFIG_PATH}")
    except Exception as e:
        log.error(f"Failed to save config: {e}")
        raise


def get_letter_map():
    return dict(_config["letter_map"])


def set_letter_map(mapping):
    _config["letter_map"] = dict(mapping)
    save()


def get_default_message():
    return _config["default_message"]


def set_default_message(msg):
    _config["default_message"] = msg
    save()


def get_message_interval():
    return _config["message_interval"]


def set_message_interval(seconds):
    _config["message_interval"] = int(seconds)
    save()


def get_all():
    """Return full config dict for the admin API."""
    return dict(_config)


def update_all(data):
    """Bulk update from admin page."""
    if "letter_map" in data:
        _config["letter_map"] = {k.upper(): int(v) for k, v in data["letter_map"].items()}
    if "default_message" in data:
        _config["default_message"] = str(data["default_message"]).upper().strip()
    if "message_interval" in data:
        _config["message_interval"] = max(10, int(data["message_interval"]))
    save()
