# GUI Auto Startup for Jetson
> Note: the directory path in this guidance is just a dummy, thus, change accordingly   
> Always make sure your GUI has minimize and exit button first, **believe me**

## Step 1: Create the Startup Shell Script
1. Open  terminal and create the launcher script inside project directory:
```
nano "/home/jetson/Documents/deployment/autostart_app.sh"
```

2. Add the following code into the editor:
```
#!/bin/bash

# Wait 5 seconds for X11 desktop environment and hardware to load
sleep 5

# Set project working directory
cd /home/jetson/Documents/deployment

# Grant display access and detect active DISPLAY
export DISPLAY=${DISPLAY:-:0}
xhost +local:root >/dev/null 2>&1 || true
xhost +local:$USER >/dev/null 2>&1 || true

# Infinite loop to keep restarting application if closed or crashed
while true; do
    echo "[$(date)] Starting VisionEngine application..."
    /usr/bin/python3 main.py
    EXIT_CODE=$?
    
    echo "[$(date)] Application exited with status code: $EXIT_CODE"
    echo "Restarting application in 2 seconds..."
    sleep 2
done
```
Save and exit (Ctrl + O, Enter, Ctrl + X).   

3. Make the script executable:
```
chmod +x "/home/jetson/Documents/deployment/autostart_app.sh"
```

## Step 2: Configure Desktop Autostart (.desktop Entry)
1. Ensure the autostart directory exists:
```
mkdir -p ~/.config/autostart
```
2. Create the .desktop autostart configuration file:
```
nano ~/.config/autostart/visionengine.desktop
```
3. Add the following configuration:
```
[Desktop Entry]
Type=Application
Name=IRnow VisionEngine
Comment=Inspection VisionEngine
Exec="/home/jetson/Documents/deployment/autostart_app.sh"
Terminal=false
X-GNOME-Autostart-enabled=true
```
Save and exit (Ctrl + O, Enter, Ctrl + X).
   
4. To disable the autostart, just remove the file:
```
rm ~/.config/autostart/visionengine.desktop
```

## Step 3: Enable Auto-Login on Jetson
Because .desktop startup entries trigger when a user logs in, automatic desktop login must be enabled so the system doesn't pause at a password screen.   
1. Open System Settings -> User Accounts on Jetson desktop.
2. Click Unlock in the top right corner and enter your password.
3. Toggle Automatic Login to ON.
> (Alternatively, edit /etc/gdm3/custom.conf and ensure AutomaticLoginEnable=true and AutomaticLogin=jetson are set under [daemon]).

## Step 4: Install Missing Qt/XCB Cursor Library
Common missing packages for activating PySide6 GUI at startup:
```
sudo apt-get update
sudo apt-get install -y libxcb-cursor0 libx11-xcb1
```

## Step 5: Configure Hardware Permissions for GPIO (/dev/gpiochip*)
If the program does not have gpio usage, skip to Step 6
1. Install the package
```
pip install gpiod
```
2. Add a udev rule to grant full read/write access to GPIO chips:
```
echo 'SUBSYSTEM=="gpio", KERNEL=="gpiochip*", MODE="0666"' | sudo tee /etc/udev/rules.d/99-gpio.rules
```
3. Reload the udev rules:
```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Step 6: Disable the "Show Desktop" Shortcut in GNOME (System Level)
To disable the shortcut entirely on the Jetson operating system so operators cannot press Super + D at all, clear the shortcut keybinding via terminal.   

Run this command directly in the Jetson terminal:

```
gsettings set org.gnome.desktop.wm.keybindings show-desktop "['']"
```
To re-enable it later (if needed):
```
gsettings reset org.gnome.desktop.wm.keybindings show-desktop
```

## Step 7: Test the Setup
```
"/home/jetson/Documents/deployment/autostart_app.sh"
```
If everything working fine, reboot
```
sudo reboot
```
