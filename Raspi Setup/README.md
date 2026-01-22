# Raspberry Pi Setup

To run PySide6 GUI, need to change Wayland to X11 server

sudo raspi-config
Advanced Settings > Wayland > X11
reboot

sudo apt update
sudo apt install -y \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0
