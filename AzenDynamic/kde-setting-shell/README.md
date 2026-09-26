# KDE Settings Shell

A Windows 11–style settings shell for KDE Plasma, written in Python + PyQt6.

> **⚠️ Early Development — Not Stable**
>
> This project is in early development. Features are incomplete, some may not work on your system, and the UI may change without notice. Not recommended for daily use yet.

KDE 设置壳 —— 基于 PyQt6 的 Windows 11 风格外观，为 KDE Plasma 提供一个更现代、更简洁的设置入口。它不替换或修改 KDE Plasma，只是在它之上的一层外壳。

---

## Features

- Windows 11 风格界面，支持深色 / 浅色 / 跟随系统
- 直接读取系统状态并执行系统命令（`nmcli`、`brightnessctl`、`bluetoothctl`、`kscreen-doctor`、`plasma-apply-*` 等）
- 复杂设置项保留“打开原生设置”按钮，回退到 KDE 原生 KCM
- 多语言：中文 / English / 日本語 / Français / Deutsch

---

## Requirements

- KDE Plasma 6（Wayland 或 X11）
- Python 3.10+
- PyQt6
- 系统命令：`brightnessctl`、`wpctl`、`nmcli`、`bluetoothctl`、`kscreen-doctor`、`plasma-apply-lookandfeel`、`plasma-apply-wallpaperimage`、`qdbus6`、`upower` 或 `acpi`

Arch 安装示例：

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
