This is quickest way (as I know) to create desktop launcher without compiling all materials.
Disadvatages: Need to copy exact environment

## 1️⃣ Create Desktop Launcher

Open terminal:

```bash
nano ~/Desktop/LensAVI.desktop
```

Paste this:

```ini
[Desktop Entry]
Name=Lens AVI
Comment=Run Lens AVI Application
Exec=/home/pi/Documents/lenv/bin/python /home/pi/Documents/lens_avi/main.py
Icon=utilities-terminal
Terminal=true
Type=Application
Categories=Development;
```

⚠️ Change `/home/pi` if your username is different.

Save:

```
CTRL + X
Y
Enter
```

---

## 2️⃣ Make It Executable

```bash
chmod +x ~/Desktop/LensAVI.desktop
```

---

## 3️⃣ Enable Double Click Execution

Right click the file →
**Properties → Permissions → Allow executing file as program**

---

Now you can double-click it.

---

### ✅ For NO Terminal Window

Change:

```
Terminal=true
```

to:

```
Terminal=false
```

But for debugging automation system, I strongly recommend keeping terminal visible.

---

## 🔥 Even Better (More Stable)

Instead of activating environment like:

```
source activate python
```

Just directly call the venv python:

```
/home/pi/Documents/lenv/bin/python
```

It’s:

* Faster
* Cleaner
* No shell dependency
* Better for automation

---

## 🚀 Industrial Setup (Recommended for your multi-Jetson + Pi coordinator system)

Since your Pi is coordinator:

Best approach tested: [**Option 3**](https://github.com/Fyzie/docs_hub/blob/main/Raspi%20Desktop%20Launcher%20and%20Script%20AutoStart/README.md#option-3-desktop-autostart-wrapper)   
In case your app use PySide6, might want to look into [this](https://github.com/Fyzie/docs_hub/blob/main/Raspi%20Startup%20Setup%20for%20PySide6%20GUI%20Display/README.md)

> WARNING : if you are about to set this app and "this app" is (1) with GUI, (2) top taskbar removed and (3) set to full screen, better to have *minimize* and *exit* button

### Run automatically on boot

#### Option 1. Using Systemd

Create systemd service:

```bash
sudo nano /etc/systemd/system/lensavi.service
```

Paste:
Without GUI:
```ini
[Unit]
Description=Lens AVI Coordinator
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Documents/lens_avi
ExecStart=/home/pi/Documents/lenv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```
With GUI:
```ini
[Unit]
Description=Lens AVI Coordinator
After=graphical.target
Wants=graphical.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
ExecStartPre=/bin/sleep 10
ExecStart=/home/pi/Documents/lenv/bin/python /home/pi/Documents/lens_avi/main.py
WorkingDirectory=/home/pi/Documents/lens_avi
Restart=on-failure

[Install]
WantedBy=graphical.target
```
Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lensavi.service
sudo systemctl start lensavi.service
```
Disable:
```bash
sudo systemctl disable lensavi.service
sudo systemctl stop lensavi.service
```
#### Option 2. Desktop AutoStart
If using systemd does not work, try **desktop autostart** for the `pi` user as below:

1. Create the autostart folder if it doesn’t exist:

```bash
mkdir -p /home/pi/.config/lxsession/LXDE-pi
```

2. Create or edit the autostart file:

```bash
nano /home/pi/.config/lxsession/LXDE-pi/autostart
```

3. Add your app:

```text
@/home/pi/Documents/lenv/bin/python /home/pi/Documents/lens_avi/main.py &
```

4. Make sure your app is executable:

```bash
chmod +x /home/pi/Documents/lens_avi/main.py
```

5. Reboot into desktop mode. The app should start full-screen (or maximized).

#### Option 3. Desktop AutoStart (Wrapper)
Create a wrapper script:

```bash
nano /home/pi/Documents/lens_avi/start_lensavi.sh
```

```bash
#!/bin/bash
# Keep the desktop alive if app exits
while true; do
    /home/pi/Documents/lenv/bin/python /home/pi/Documents/lens_avi/main.py
    sleep 5
done
```

* Make it executable:

```bash
chmod +x /home/pi/Documents/lens_avi/start_lensavi.sh
```

* Change autostart to:

```text
mkdir -p /home/pi/.config/lxsession/LXDE-pi
nano /home/pi/.config/lxsession/LXDE-pi/autostart
```
* Write in the autostart:
```
@/home/pi/Documents/lens_avi/start_lensavi.sh
```

* Now, even if your app crashes, it will restart automatically, and desktop won’t go blank.

**NOTE**: If your script is an GUI app (e.g. to run PySide6 GUI at startup):   

1. Install below:

```
sudo apt update \
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
```

2. Change **Wayland** to **X11 server**

```
sudo raspi-config
``` 
Advanced Settings > Wayland > X11   
```
reboot
```

---
If want to **REMOVE** the autostart file:
```
rm /home/pi/.config/lxsession/LXDE-pi/autostart
```

Now:

* Auto start on boot
* Auto restart if crash
* No need to double click
* More production ready

---
