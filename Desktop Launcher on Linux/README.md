This is quickest way (as I know) to create desktop launcher without compiling all materials.

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

Better approach is:

### Run automatically on boot

Create systemd service:

```bash
sudo nano /etc/systemd/system/lensavi.service
```

Paste:

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

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lensavi.service
sudo systemctl start lensavi.service
```

Now:

* Auto start on boot
* Auto restart if crash
* No need to double click
* More production ready

---
