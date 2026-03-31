"""Boot: connect to WiFi."""
import network
import time

SSID = "Cat-House"
PASSWORD = "sweetcookies123425"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print(f"Connecting to {SSID}...")
    wlan.connect(SSID, PASSWORD)
    for _ in range(30):
        if wlan.isconnected():
            break
        time.sleep(1)

if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print(f"Connected! IP: {ip}")
else:
    print("WiFi connection failed — starting without network")
