"""Boot: connect to WiFi with static IP."""
import network
import time

SSID = "UTG_Private"
PASSWORD = "Multiball26!"

STATIC_IP = "192.168.1.99"
GATEWAY = "192.168.1.1"
SUBNET = "255.255.255.0"
DNS = "8.8.8.8"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, DNS))

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
