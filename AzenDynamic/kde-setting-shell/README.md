# KDE Settings Shell

A Windows 11–style settings shell for KDE Plasma, written in Python + PyQt6.

> **⚠️ Early Development — Not Stable**
>
> This project is in early development. Features are incomplete, some may not work on your system, and the UI may change without notice. Not recommended for daily use yet.

---

## Features

- windows11-like ui
- excute system command in background（`nmcli`、`brightnessctl`、`bluetoothctl`、`kscreen-doctor`、`plasma-apply-*` 等）
- complex setting have a way to lead to native settings
- languange: CH,EN,JP,FR,DE

---

## Requirements

- KDE Plasma 6（Wayland 或 X11）
- Python 3.10+
- PyQt6
- system command：`brightnessctl`、`wpctl`、`nmcli`、`bluetoothctl`、`kscreen-doctor`、`plasma-apply-lookandfeel`、`plasma-apply-wallpaperimage`、`qdbus6`、`upower` 或 `acpi`

Arch example：

sudo pacman -S brightnessctl wireplumber networkmanager bluez bluez-utils \
               kscreen plasma-workspace qt6-tools upower

## Installation
bash
git clone https://github.com/AzenDev2026/kde-setting-shell.git
cd kde-setting-shell

python3 -m venv myenv
source myenv/bin/activate
pip install pyqt6

## run: cd /to/this/file , python main.py

## License
GPLv3 — see LICENSE for details.

Part of the NVazen / Azen ecosystem under 白企 Whitent.

© 2026 白企 Whitent / Azen Project
