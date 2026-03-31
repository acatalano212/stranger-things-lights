# Stranger Things Wall Lights 💡

Recreate the iconic Stranger Things alphabet wall with real Christmas lights. 100 WS2811 RGB LEDs mounted on a wall, spelling out messages letter by letter — just like Joyce's wall in the show.

Runs on a **Seeed XIAO ESP32-S3** with MicroPython. Tiny footprint, WiFi built-in, reliable LED timing via the RMT peripheral.

## Features

- 🎄 **Christmas Light Idle** — warm twinkling colors (red, green, blue, yellow, purple) on all 100 LEDs
- ✉️ **Message Spelling** — dramatic flicker transition, then letters light up one at a time
- 📱 **Web Interface** — visitors scan a QR code and send custom messages through the lights
- ⚙️ **Admin Panel** — password-protected page to remap letters, change default message, and test individual LEDs
- 👻 **Motion Detection** — optional AM312 PIR sensor triggers spooky Upside Down effects (GPIO 2)

## Hardware

| Component | Details |
|-----------|---------|
| Controller | Seeed XIAO ESP32-S3 |
| LEDs | 100x BTF-LIGHTING WS2811 12mm F8 RGB (12V, individually addressable) |
| Power | 12V Molex adapter (12V on pin 1, 5V on pin 4) |
| Motion Sensor | AM312 PIR (optional, 3.3V) |

## Wiring

```
12V Molex Power Adapter
  ├── Pin 1 (12V) ──→ WS2811 LED string V+ (red wire)
  ├── Pin 4 (5V)  ──→ XIAO ESP32-S3 5V pin
  └── GND ─────────→ Shared ground (LEDs + XIAO)

XIAO ESP32-S3
  ├── D0 (GPIO 1) ──→ WS2811 Data In (green/white wire)
  ├── 5V ───────────→ Molex 5V (pin 4)
  ├── GND ──────────→ Molex GND (shared with LEDs)
  └── D1 (GPIO 2) ──→ AM312 PIR OUT (optional)

AM312 PIR Sensor (optional)
  ├── VCC ──→ XIAO 3.3V
  ├── GND ──→ XIAO GND
  └── OUT ──→ XIAO D1 (GPIO 2)

⚡ Common ground between power supply, XIAO, and LEDs is CRITICAL
⚡ No level shifter needed — 3.3V GPIO works with these WS2811 LEDs
⚡ XIAO can be powered via USB and 5V pin simultaneously (safe)
```

## XIAO ESP32-S3 Pinout

```
        ┌──────────────┐
        │   USB-C      │
   ─────┤              ├─────
   D0/A0│ 1  (GPIO1)   │ 5V    ← Molex 5V
   D1/A1│ 2  (GPIO2)   │ GND   ← Shared GND
   D2/A2│ 3  (GPIO3)   │ 3.3V
   D3/A3│ 4  (GPIO4)   │
   D4   │ 5  (GPIO5)   │
   D5   │ 6  (GPIO6)   │
   D6/TX│ 7  (GPIO43)  │
   ─────┤              ├─────
        └──────────────┘
```

## Letter Mapping

Letters A-Z are mapped to LED indices 0-99 (spread evenly by default). After mounting the lights on the wall, use the **Admin Panel** to remap each letter to the actual LED sitting above it, and use the 💡 flash button to identify individual LEDs.

Default layout (3 rows on the wall):
```
Row 1:  A  B  C  D  E  F  G  H
Row 2:  I  J  K  L  M  N  O  P
Row 3:  Q  R  S  T  U  V  W  X  Y  Z
```

## Installation

### Flash MicroPython

```bash
# Install tools
pip install esptool mpremote

# Put XIAO in bootloader mode: hold BOOT, press RESET, release BOOT
esptool --chip esp32s3 --port COM6 erase-flash
esptool --chip esp32s3 --port COM6 write-flash 0 ESP32_GENERIC_S3-v1.27.0.bin
```

### Upload Project Files

```bash
cd esp32/
mpremote connect COM6 cp boot.py :boot.py
mpremote connect COM6 cp config.py :config.py
mpremote connect COM6 cp led.py :led.py
mpremote connect COM6 cp pages.py :pages.py
mpremote connect COM6 cp main.py :main.py
mpremote connect COM6 reset
```

### WiFi Setup

Edit `esp32/boot.py` with your WiFi credentials:
```python
SSID = "Your-WiFi-Name"
PASSWORD = "your-password"
```

## Web Interface

Once running, the XIAO connects to WiFi and serves:

| URL | Description |
|-----|-------------|
| `http://<ip>/` | Message page — send messages through the lights |
| `http://<ip>/admin` | Admin panel (password protected) |

The admin panel lets you:
- Change the default message and play interval
- Remap letter-to-LED assignments (0-99)
- Flash individual LEDs to identify them on the strand

## Project Structure

```
stranger-things-lights/
├── esp32/                     # MicroPython firmware for XIAO ESP32-S3
│   ├── boot.py                # WiFi connection on startup
│   ├── main.py                # Web server + LED control thread
│   ├── led.py                 # LED effects (idle, flicker, spell, spook)
│   ├── config.py              # Persistent JSON config manager
│   └── pages.py               # HTML pages (index, admin, login)
├── app.py                     # Original Pi version (Flask + neopixel)
├── led_effects.py             # Original Pi LED effects
├── letter_map.py              # Original Pi config
├── config.py                  # Original Pi persistent config
├── sound_effects.py           # Pi audio (disabled — PWM conflict)
├── templates/                 # Original Pi HTML templates
│   ├── index.html
│   ├── admin.html
│   └── admin_login.html
├── install.sh                 # Pi setup script
├── stranger-things.service    # Pi systemd unit file
├── requirements.txt           # Pi Python dependencies
└── README.md
```

## Configuration

All settings are managed via the admin panel at `/admin` and stored in `config.json` on the ESP32 flash. Defaults:

| Setting | Default | Description |
|---------|---------|-------------|
| `default_message` | `"RUN WILL RUN"` | Auto-plays on a timer |
| `message_interval` | `60` seconds | Time between auto-messages |
| `letter_map` | A=0, B=4, ... Z=99 | LED index per letter (evenly spread) |
| `num_leds` | `100` | Total LEDs on the string |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No LED output | Check wiring: Data → GPIO 1 (D0), common ground |
| Colors wrong | These WS2811 use RGB order (set in `led.py`) |
| WiFi won't connect | Check SSID/password in `boot.py`, ensure 2.4GHz network |
| Web page won't load | Wait 8-10s after boot for WiFi, check IP in serial monitor |
| Can't flash via USB | Hold BOOT + press RESET to enter bootloader mode |
| Admin page error | Clear cookies, re-login with password |

## Key Learnings

- **No level shifter needed** for BTF-LIGHTING WS2811 12mm pixels with 3.3V GPIO
- **ESP32-S3 RMT peripheral** provides reliable WS2811 timing (better than Pi's PWM)
- **Pi audio conflicts with GPIO 18 PWM** — if using Pi version, set `dtparam=audio=off` in `/boot/firmware/config.txt`
- **Color order is RGB** for these specific WS2811 LEDs (not GRB)
