"""
Stranger Things Wall Lights — MicroPython on XIAO ESP32-S3

Lightweight HTTP server + LED control using _thread.
"""
import time
import os
import json
import socket
import _thread
import network

import gc
import config
import led
from pages import INDEX_PAGE, LOGIN_PAGE, ADMIN_PAGE, ADMIN_PASSWORD

# ── OTA Update ──────────────────────────────────────────────────

REPO_RAW = "https://raw.githubusercontent.com/acatalano212/stranger-things-lights/master/esp32/"
OTA_FILES = ["pages.py", "config.py", "led.py", "main.py", "boot.py"]


def ota_update():
    """Download latest files from GitHub and write to flash."""
    import urequests
    updated = []
    errors = []

    for fname in OTA_FILES:
        gc.collect()
        try:
            url = REPO_RAW + fname
            print(f"OTA: fetching {fname}...")
            r = urequests.get(url)
            if r.status_code == 200:
                with open(fname, "w") as f:
                    f.write(r.text)
                updated.append(fname)
                print(f"OTA: updated {fname}")
            else:
                errors.append(f"{fname}: HTTP {r.status_code}")
                print(f"OTA: failed {fname} ({r.status_code})")
            r.close()
        except Exception as e:
            errors.append(f"{fname}: {str(e)}")
            print(f"OTA: error {fname}: {e}")

    return updated, errors

# ── Cloud Polling ───────────────────────────────────────────────

CLOUD_API_URL = ""  # e.g. "https://xxx.azurestaticapps.net/api/get-message"
CLOUD_DEVICE_KEY = ""  # must match DEVICE_KEY in Azure app settings
CLOUD_POLL_INTERVAL = 5


def poll_cloud():
    """Check Azure for pending messages. Returns message string or None."""
    if not CLOUD_API_URL:
        return None
    try:
        import urequests
        headers = {}
        if CLOUD_DEVICE_KEY:
            headers["x-device-key"] = CLOUD_DEVICE_KEY
        r = urequests.get(CLOUD_API_URL, headers=headers)
        data = json.loads(r.text) if r.status_code == 200 else {}
        r.close()
        gc.collect()
        return data.get("message")
    except Exception as e:
        print(f"Cloud poll error: {e}")
        return None


# ── State ───────────────────────────────────────────────────────

message_queue = []
queue_lock = _thread.allocate_lock()
admin_tokens = {}  # simple token-based auth


# ── LED Thread ──────────────────────────────────────────────────

def led_loop():
    """Runs in a background thread — idle animation + message display."""
    print("LED thread started")
    idle = led.ChristmasIdle()
    last_msg_time = time.time()
    last_cloud_poll = 0

    while True:
        now = time.time()

        # Check for queued custom message
        msg = None
        queue_lock.acquire()
        if message_queue:
            msg = message_queue.pop(0)
        queue_lock.release()

        if msg:
            print(f"Playing message: {msg}")
            led.display_message(msg)
            idle = led.ChristmasIdle()
            last_msg_time = time.time()
            continue

        # Scheduled default message
        interval = config.get_message_interval()
        if now - last_msg_time >= interval:
            default_msg = config.get_default_message()
            print(f"Scheduled: {default_msg}")
            led.display_message(default_msg)
            idle = led.ChristmasIdle()
            last_msg_time = time.time()
            continue

        # Idle animation step
        idle.step()
        time.sleep_ms(50)

        # Cloud polling (during idle only)
        if CLOUD_API_URL and now - last_cloud_poll >= CLOUD_POLL_INTERVAL:
            last_cloud_poll = now
            cloud_msg = poll_cloud()
            if cloud_msg:
                print(f"Cloud message: {cloud_msg}")
                queue_lock.acquire()
                message_queue.append(cloud_msg)
                queue_lock.release()


# ── HTTP Server ─────────────────────────────────────────────────

def parse_request(client):
    """Parse HTTP request, return (method, path, headers, body)."""
    raw = client.recv(2048)
    if not raw:
        return None, None, {}, ""
    text = raw.decode("utf-8", "ignore")
    lines = text.split("\r\n")
    first = lines[0].split(" ")
    method = first[0]
    path = first[1] if len(first) > 1 else "/"

    headers = {}
    i = 1
    while i < len(lines) and lines[i]:
        if ":" in lines[i]:
            k, v = lines[i].split(":", 1)
            headers[k.strip().lower()] = v.strip()
        i += 1

    body = ""
    if "\r\n\r\n" in text:
        body = text.split("\r\n\r\n", 1)[1]

    return method, path, headers, body


def get_cookie(headers, name):
    cookies = headers.get("cookie", "")
    for part in cookies.split(";"):
        part = part.strip()
        if part.startswith(name + "="):
            return part[len(name) + 1:]
    return None


def is_admin(headers):
    token = get_cookie(headers, "admin_token")
    return token and token in admin_tokens


def send_response(client, status, content_type, body, extra_headers=""):
    if isinstance(body, str):
        body = body.encode()
    header = f"HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nContent-Length: {len(body)}\r\nConnection: close\r\n{extra_headers}\r\n"
    client.sendall(header.encode())
    # Send body in chunks to avoid memory issues on large pages
    mv = memoryview(body)
    off = 0
    while off < len(body):
        n = client.send(mv[off:off + 2048])
        off += n


def send_json(client, data, status="200 OK", extra_headers=""):
    send_response(client, status, "application/json", json.dumps(data), extra_headers)


def send_redirect(client, location, extra_headers=""):
    header = f"HTTP/1.1 302 Found\r\nLocation: {location}\r\nContent-Length: 0\r\nConnection: close\r\n{extra_headers}\r\n"
    client.sendall(header.encode())


def handle_client(client):
    client.settimeout(5)
    try:
        method, path, headers, body = parse_request(client)
        if method is None:
            client.close()
            return

        # ── Public routes ───────────────────────────────────
        if path == "/" and method == "GET":
            send_response(client, "200 OK", "text/html", INDEX_PAGE)

        elif path == "/api/status" and method == "GET":
            send_json(client, {"state": "idle", "message": ""})

        elif path == "/api/message" and method == "POST":
            try:
                data = json.loads(body)
                msg = data.get("message", "").upper().strip()
            except:
                send_json(client, {"error": "Invalid JSON"}, "400 Bad Request")
                return

            if not msg:
                send_json(client, {"error": "No message"}, "400 Bad Request")
                return
            if not all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ " for c in msg):
                send_json(client, {"error": "A-Z and spaces only"}, "400 Bad Request")
                return
            if len(msg) > 50:
                send_json(client, {"error": "Max 50 chars"}, "400 Bad Request")
                return

            queue_lock.acquire()
            if len(message_queue) > 0:
                queue_lock.release()
                send_json(client, {"error": "A message is already queued"}, "429 Too Many")
                return
            message_queue.append(msg)
            queue_lock.release()
            print(f"Queued: {msg}")
            send_json(client, {"success": True, "message": msg})

        # ── Admin login ─────────────────────────────────────
        elif path == "/admin/login" and method == "GET":
            send_response(client, "200 OK", "text/html", LOGIN_PAGE.replace("{error}", ""))

        elif path == "/admin/login" and method == "POST":
            # Parse form data
            pw = ""
            for part in body.split("&"):
                if part.startswith("password="):
                    pw = part[9:].replace("+", " ").replace("%20", " ")

            if pw == ADMIN_PASSWORD:
                import random
                token = str(random.getrandbits(30)) + str(random.getrandbits(30))
                admin_tokens[token] = True
                send_redirect(client, "/admin", f"Set-Cookie: admin_token={token}; Path=/; HttpOnly\r\n")
            else:
                page = LOGIN_PAGE.replace("{error}", '<p class="e">Wrong password</p>')
                send_response(client, "200 OK", "text/html", page)

        elif path == "/admin/logout" and method == "GET":
            token = get_cookie(headers, "admin_token")
            if token and token in admin_tokens:
                del admin_tokens[token]
            send_redirect(client, "/", "Set-Cookie: admin_token=; Path=/; Max-Age=0\r\n")

        elif path == "/admin" and method == "GET":
            if not is_admin(headers):
                send_redirect(client, "/admin/login")
                return
            send_response(client, "200 OK", "text/html", ADMIN_PAGE)

        elif path == "/api/admin/config" and method == "GET":
            if not is_admin(headers):
                send_json(client, {"error": "Unauthorized"}, "401 Unauthorized")
                return
            send_json(client, config.get_all())

        elif path == "/api/admin/config" and method == "POST":
            if not is_admin(headers):
                send_json(client, {"error": "Unauthorized"}, "401 Unauthorized")
                return
            try:
                data = json.loads(body)
                config.update_all(data)
                send_json(client, {"success": True})
            except Exception as e:
                send_json(client, {"error": str(e)}, "500 Error")

        elif path == "/api/admin/test-led" and method == "POST":
            if not is_admin(headers):
                send_json(client, {"error": "Unauthorized"}, "401 Unauthorized")
                return
            try:
                data = json.loads(body)
                idx = int(data["led_index"])
                if 0 <= idx < led.NUM_LEDS:
                    # Flash in a thread so we don't block the server
                    _thread.start_new_thread(led.flash_led, (idx,))
                    send_json(client, {"success": True, "led_index": idx})
                else:
                    send_json(client, {"error": "Invalid index"}, "400 Bad Request")
            except Exception as e:
                send_json(client, {"error": str(e)}, "400 Bad Request")

        elif path == "/api/admin/ota-update" and method == "POST":
            if not is_admin(headers):
                send_json(client, {"error": "Unauthorized"}, "401 Unauthorized")
                return
            try:
                updated, errors = ota_update()
                send_json(client, {"success": len(errors) == 0, "updated": updated, "errors": errors})
                if not errors:
                    import machine
                    time.sleep(1)
                    machine.reset()
            except Exception as e:
                send_json(client, {"error": str(e)}, "500 Error")

        else:
            send_response(client, "404 Not Found", "text/plain", "Not Found")

    except OSError:
        pass
    except Exception as e:
        print(f"Request error: {e}")
        try:
            send_response(client, "500 Error", "text/plain", str(e))
        except:
            pass
    finally:
        try:
            client.close()
        except:
            pass


def start_server(port=80):
    """Start the HTTP server on the given port."""
    addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    s.settimeout(None)

    wlan = network.WLAN(network.STA_IF)
    ip = wlan.ifconfig()[0] if wlan.isconnected() else "unknown"
    print(f"Web server at http://{ip}:{port}/")
    print(f"Admin page at http://{ip}:{port}/admin")

    while True:
        client, addr = s.accept()
        try:
            handle_client(client)
        except Exception as e:
            print(f"Client error: {e}")
            try:
                client.close()
            except:
                pass


# ── Entry Point ─────────────────────────────────────────────────

def main():
    print("=" * 40)
    print("Stranger Things Wall Lights")
    print("=" * 40)

    config.load()
    led.init_strip()
    print(f"LEDs initialized: {led.NUM_LEDS} on GPIO {led.LED_PIN}")

    # Start LED animation in background thread
    _thread.start_new_thread(led_loop, ())

    # Run web server in main thread
    start_server(80)


main()
