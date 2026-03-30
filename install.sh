#!/bin/bash
# Stranger Things Wall Lights — Installation Script
# Run on Raspberry Pi 3B+ with Raspberry Pi OS

set -e

echo "=================================="
echo "Stranger Things Wall Lights Setup"
echo "=================================="

# Check we're on a Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "WARNING: This doesn't look like a Raspberry Pi"
fi

# Update packages
echo ""
echo "[1/5] Updating system packages..."
sudo apt-get update -qq

# Install system dependencies
echo ""
echo "[2/5] Installing system dependencies..."
sudo apt-get install -y -qq python3-pip python3-venv python3-dev \
    libatlas-base-dev alsa-utils pulseaudio

# Create virtual environment (optional but clean)
echo ""
echo "[3/5] Installing Python dependencies..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

sudo pip3 install -r requirements.txt

# Enable SPI (needed for some LED configurations)
echo ""
echo "[4/5] Configuring hardware..."
if ! grep -q "^dtparam=spi=on" /boot/config.txt 2>/dev/null; then
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
    echo "  SPI enabled (reboot may be required)"
fi

# Ensure audio is enabled
if ! grep -q "^dtparam=audio=on" /boot/config.txt 2>/dev/null; then
    echo "dtparam=audio=on" | sudo tee -a /boot/config.txt
    echo "  Audio enabled"
fi

# Install systemd service
echo ""
echo "[5/5] Installing systemd service..."
sudo cp "$SCRIPT_DIR/stranger-things.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable stranger-things.service

echo ""
echo "=================================="
echo "Installation complete!"
echo ""
echo "To start now:  sudo systemctl start stranger-things"
echo "To check logs: sudo journalctl -u stranger-things -f"
echo "To stop:       sudo systemctl stop stranger-things"
echo ""
echo "The web interface will be at: http://$(hostname -I | awk '{print $1}')/"
echo "=================================="
