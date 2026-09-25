# ALRM 3 — Azen Laptop Resources Management

ALRM (Azen Laptop Resources Management) is a system-level resource
management technology for laptops. It reduces background process
activity and manages system sleep behavior.

Version 3 is a C++17 rewrite of the original Python implementation,
offering lower resource usage and faster response times.

---

## Requirements

- Linux with systemd
- gcc 9+ or clang 10+
- GLib 2.0 development headers
- libsystemd development headers

Install dependencies:

Arch Linux:

bash
sudo pacman -S base-devel cmake glib2 systemd-libs

Debian / Ubuntu:

bash
sudo apt install build-essential cmake libglib2.0-dev libsystemd-dev

# Build
bash
git clone https://github.com/AzenDev2026/Azen_dev.git
cd Azen_dev/AzenDynamic/ALRM
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Install
bash
sudo make install
sudo mkdir -p /etc/azen
sudo cp ../config/Azen-ALRM.conf /etc/azen/
sudo cp ../systemd/azen-alrm.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now azen-alrm.service

# Deploy Script
bash
cd AzenDynamic/ALRM
chmod +x deploy_alrm.sh
sudo ./deploy_alrm.sh
Supports Arch Linux, Ubuntu, and Debian.

# Configuration
Config file: /etc/azen/Azen-ALRM.conf

Option	Values	Description
SYSTEM_MODE	energy-saver, balanced, performance	Operating mode
ENABLE_APP_NAP	true, false	Enable App Nap
SCAN_INTERVAL	integer (seconds)	Process scan interval
FREEZE_TIMEOUT	integer (seconds)	Auto-thaw timeout
CPU_THRESHOLD	integer (percent)	Skip processes above this usage
WHITELIST_APPS	comma-separated	Never frozen

# Apply changes:

bash
sudo systemctl restart azen-alrm.service

# Common Commands
Service
bash
# Start
sudo systemctl start azen-alrm.service

# Stop
sudo systemctl stop azen-alrm.service

# Restart
sudo systemctl restart azen-alrm.service

# Enable at boot
sudo systemctl enable azen-alrm.service

# Disable at boot
sudo systemctl disable azen-alrm.service

# Status
sudo systemctl status azen-alrm.service

# Logs
bash
# Live logs
sudo journalctl -u azen-alrm.service -f

# Recent logs
sudo journalctl -u azen-alrm.service -n 100

# Logs since boot
sudo journalctl -u azen-alrm.service -b
Configuration
bash
# Edit config
sudo nano /etc/azen/Azen-ALRM.conf

# Check current sleep mode
cat /sys/power/mem_sleep

# Check supported sleep modes
cat /sys/power/state
Inspection
bash
# List running application scopes
systemctl --user list-units --type=scope --state=running

# Check a specific scope
systemctl --user status <scope-name>

# Update
bash
cd Azen_dev
git pull
cd AzenDynamic/ALRM
make clean && make
sudo make install
sudo systemctl restart azen-alrm.service

# Uninstall
bash
sudo systemctl disable --now azen-alrm.service
sudo rm /etc/systemd/system/azen-alrm.service
sudo rm /usr/local/bin/alrm
sudo rm -rf /etc/azen
sudo systemctl daemon-reload

# Sleep Mode
ALRM configures sleep via /sys/power/mem_sleep:

s2idle — Modern Standby, used by most laptops after 2020

deep — Traditional ACPI S3, used by older laptops

ALRM 3 defaults to s2idle. Forcing deep on recent hardware
can cause the system to fail to resume.

#License
GPLv3
