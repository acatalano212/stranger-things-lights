"""Persistent config stored as JSON on flash."""
import json

CONFIG_FILE = "config.json"

_defaults = {
    "letter_map": {chr(65 + i): round(i * 99 / 25) for i in range(26)},  # A-Z spread across 0-99
    "default_message": "RUN WILL RUN",
    "message_interval": 60,
    "num_leds": 100,
}

_config = {}


def load():
    global _config
    _config = dict(_defaults)
    try:
        with open(CONFIG_FILE, "r") as f:
            saved = json.load(f)
        _config.update(saved)
        print("Config loaded from flash")
    except:
        print("No config.json, using defaults")


def save():
    with open(CONFIG_FILE, "w") as f:
        json.dump(_config, f)
    print("Config saved")


def get_letter_map():
    return dict(_config["letter_map"])


def get_default_message():
    return _config["default_message"]


def get_message_interval():
    return _config["message_interval"]


def get_all():
    return dict(_config)


def update_all(data):
    if "letter_map" in data:
        _config["letter_map"] = {k.upper(): int(v) for k, v in data["letter_map"].items()}
    if "default_message" in data:
        _config["default_message"] = str(data["default_message"]).upper().strip()
    if "message_interval" in data:
        _config["message_interval"] = max(10, int(data["message_interval"]))
    save()
