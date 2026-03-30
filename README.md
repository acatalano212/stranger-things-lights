# Stranger Things Wall Lights 💡

Recreate the iconic Stranger Things alphabet wall with real Christmas lights. A string of 100 WS2811 RGB LEDs mounted on a wall, spelling out messages letter by letter — just like Joyce's wall in the show.

## Features

- 🎄 **Christmas Light Idle** — warm twinkling colors on all 100 LEDs
- ✉️ **Message Spelling** — dramatic flicker, then letters light up one at a time
- 📱 **QR Code Web Page** — visitors can send custom messages through the lights
- 👻 **Motion Detection** — optional PIR sensor triggers spooky Upside Down effects
- 🔊 **Sound Effects** — optional speaker plays atmospheric sounds

## Hardware

| Component | Details |
|-----------|---------|
| Controller | Raspberry Pi 3B+ |
| LEDs | 100x WS2811 RGB (12V, individually addressable) |
| Power | 12V power supply (5A+ recommended) |
| Level Shifter | SN74AHCT125 or similar (3.3V → 5V for data line) |
| Speaker | 3W 8Ω with JST-PH2.0 (driven via PAM8403 amp) |
| Motion Sensor | PIR sensor (optional) |

## Wiring

```
12V Power Supply
  ├── +12V ──→ WS2811 LED string +12V (red wire)
  ├── GND ───→ WS2811 LED string GND (white wire)
  │            └── ALSO connect to Pi GND (Pin 6)
  │
Raspberry Pi 3B+
  ├── GPIO 18 (Pin 12) ──→ Level Shifter IN
  ├── 3.3V (Pin 1) ──────→ Level Shifter LV
  ├── GND (Pin 6) ───────→ Level Shifter GND (both sides)
  ├── GPIO 17 (Pin 11) ──→ PIR sensor OUT (optional)
  ├── 3.5mm jack ────────→ PAM8403 amp input(optional)
  │
Level Shifter (SN74AHCT125)
  ├── HV ────────→ 5V (Pi Pin 2)
  └── OUT ───────→ WS2811 DATA (green wire)

⚡ Add a 300-470Ω resistor on the data line near the first LED
⚡ Add a 1000µF capacitor across +12V/GND near the first LED
⚡ Common ground between 12V supply, Pi, and LEDs is CRITICAL
```

## Letter Mapping

After mounting the LED string on the wall with letters painted below, update `letter_map.py` with the actual LED index above each letter:

```python
LETTER_MAP = {
    'A': 0,   # LED index 0 is above the letter A
    'B': 3,   # LED index 3 is above the letter B
    ...
}
```

The show uses 3 rows:
```
Row 1:  A  B  C  D  E  F  G  H
Row 2:  I  J  K  L  M  N  O  P
Row 3:  Q  R  S  T  U  V  W  X  Y  Z
```

## Installation

```bash
# Clone to the Pi
git clone <repo-url> /opt/stranger-things-lights
cd /opt/stranger-things-lights

# Run the installer
chmod +x install.sh
sudo ./install.sh

# Start the service
sudo systemctl start stranger-things

# View logs
sudo journalctl -u stranger-things -f
```

## Web Interface

Once running, visit the Pi's IP address in a browser to send custom messages. Generate a QR code pointing to `http://<pi-ip>/` and post it near the wall.

Custom messages play **2 times** then revert to the default message.

## Configuration

Edit `letter_map.py` to change:

| Setting | Default | Description |
|---------|---------|-------------|
| `DEFAULT_MESSAGE` | `"RUN WILL RUN"` | Message displayed every 5 minutes |
| `MESSAGE_INTERVAL` | `300` (5 min) | Seconds between auto-messages |
| `CUSTOM_MESSAGE_PLAYS` | `2` | Times a custom message repeats |
| `NUM_LEDS` | `100` | Total LEDs on the string |
| `LED_PIN` | `18` | GPIO pin (must be PWM: 18 or 12) |
| `LED_BRIGHTNESS` | `200` | Brightness 0-255 |
| `PIR_PIN` | `17` | GPIO for motion sensor |
| `MOTION_COOLDOWN` | `30` | Seconds between motion triggers |

## Sound Effects

Sound is generated programmatically (no .wav files needed) and played through the Pi's **3.5mm audio jack** via a **PAM8403 amplifier** to the speaker:

```
Pi 3.5mm jack ──→ PAM8403 input (L or R channel + GND)
PAM8403 output ──→ Speaker (JST-PH2.0 connector)
PAM8403 VCC ─────→ Pi 5V (Pin 2) or 3.3V-5V source
PAM8403 GND ─────→ Pi GND
```

Effects are generated as waveforms and played via `aplay`:
- **Flicker sound** — electrical buzzing during message transitions
- **Letter tones** — short pitched tone for each letter (A=low, Z=high)
- **Spook sound** — deep drones and eerie sweeps on motion detection
- **Startup chime** — ascending tone sequence on boot

## Project Structure

```
stranger-things-lights/
├── app.py                    # Main app: Flask + LED control + scheduling
├── led_effects.py            # All LED animations and effects
├── sound_effects.py          # GPIO PWM sound generation
├── letter_map.py             # Configuration: letter mapping + settings
├── requirements.txt          # Python dependencies
├── install.sh                # Setup script
├── stranger-things.service   # systemd unit file
├── sounds/                   # Sound effect .wav files
├── templates/
│   └── index.html            # "Send to the Upside Down" web page
└── README.md
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No LED output | Check wiring, common ground, level shifter, GPIO 18 |
| "Must run as root" | LEDs require root: `sudo python3 app.py` |
| Colors look wrong | WS2811 may use GRB order — adjust in `led_effects.py` |
| Web page won't load | Check Pi IP, ensure port 80 is free |
| Motion sensor always triggers | Adjust PIR sensitivity pot, increase `MOTION_COOLDOWN` |
