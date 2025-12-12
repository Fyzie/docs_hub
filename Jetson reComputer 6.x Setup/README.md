# Jetson reComputer 6.x Setup Guide

This guide describes how to flash, configure, and prepare a Jetson reComputer Industrial Orin Nano 8GB (Jetpack 6.x) for development with CUDA, PyTorch, Pylon, and common utilities.

---

## 📌 Requirements

* Ubuntu **22.04 or newer** (for NVIDIA SDK Manager)
* Jetson device (Jetpack 6.x supported)
* USB-C cable
* Power connector (2-Pin terminal block)

---
## **On Ubuntu,**

### 1. Flash Jetpack 6.x Using NVIDIA SDK Manager


1. Download **NVIDIA SDK Manager** (22.04+)
2. Launch the SDK Manager.
3. Flash **Jetpack 6.x** into the Jetson **NVMe** storage.

#### To flash the reComputer Industrial board:

1. Connect USB-C cable to the **USB2.0 DEVICE** port.
2. Use a pin to press & hold the **RECOVERY** button.
3. While holding recovery:

   * Connect the 2-Pin power connector.
   * Power on the board.
4. Release the recovery button.

---
## **On Jetson,**

### 2. Update & Install JetPack SDK + CUDA

```bash
sudo apt update
sudo apt install nvidia-jetpack -y
sudo apt-get install cuda
```
---
### 3. Install Browser
Make sure to install NVIDIA GPU Driver first (Step 2)
```bash
sudo apt install epiphany-browser
sudo chown $USER:$USER $HOME/Downloads && chmod 755 $HOME/Downloads
```
---

### 4. Install Pip & Configure CUDA Paths

```bash
sudo apt install python3-pip
sudo apt install nano
nano ~/.bashrc
```

Add to bottom of `~/.bashrc`:

```bash
export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
export PATH=$PATH:$CUDA_HOME/bin
```
To save, press `Ctrl+X`, then `Y`, followed by `Enter`   

Apply changes:

```bash
source ~/.bashrc
```

---

### 5. Install JTOP (Jetson Stats)

```bash
sudo python3.10 -m pip install -u jetson-stats
sudo systemctl restart jtop.service
sudo reboot
```

---

### 6. Install Miniconda (AArch64)

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all
```

---

### 7. Install Basler Pylon (AArch64)

**Pylon 25.07 ARM64 Debian Package**  
Download here:
[https://www.baslerweb.com/en/downloads/software/3520605482/?downloadCategory.values.label.data=pylon](https://www.baslerweb.com/en/downloads/software/3520605482/?downloadCategory.values.label.data=pylon)

Extract, go to folder with `.deb` files, then:

```bash
sudo chmod 755 ./pylon_*.deb ./codemeter*.deb
sudo apt-get install ./pylon_*.deb ./codemeter*.deb
```

---

### 8. Create Conda Environment (Python 3.10)

```bash
conda create --name pygpu python=3.10
conda activate pygpu
```

---

### 9. Install Dependencies

#### Pylon binding

```bash
pip install pypylon
```

#### PyTorch for Jetpack 6.0 (cu12.6)

```bash
pip install torch torchvision torchaudio --index-url https://pypi.jetson-ai-lab.io/jp6/cu126/
```

#### Verify CUDA

```bash
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'CUDA Version: {torch.version.cuda}')"
```

#### UI & OS libraries

```bash
pip install PySide6
sudo apt install libdouble-conversion3 libopenblas-dev libxcb-xinerama0 libxcb-xfixes0 libxcb-shape0 libxcb-randr0 libxcb-cursor0
sudo apt install cmake
```

#### RFDETR + Supervision

```bash
pip install rfdetr supervision
```

#### OpenCV

```bash
sudo apt-get update
sudo apt-get install libgtk2.0-dev pkg-config
sudo apt-get install libopencv-dev
pip uninstall opencv-python opencv-python-headless
pip install opencv-python
```

#### Fix numpy version for Jetson compatibility

```bash
pip install "numpy<2"
```
may see some red, but should be fine to proceed

---

### 10. Install Visual Studio Code (ARM64)

Download ARM64 `.deb`:
[https://code.visualstudio.com/download](https://code.visualstudio.com/download)

Then install:

```bash
sudo dpkg -i ./code_*.deb
```

### 11. Install Remote Desktop App (Optional)

Download NoMachine for ARM DEB (arm64) for Jetson:
[https://download.nomachine.com/download/?id=30&platform=linux&distro=arm](https://download.nomachine.com/download/?id=30&platform=linux&distro=arm)

Go to Download folder:
```
sudo dpkg -i ./nomachine_*.deb
```
In case of the package installation interrupted:
```
sudo dpkg --configure -a
sudo apt --fix-broken install
```

Download same for your host PC.   
[NoMachine Website](https://www.nomachine.com/)   
[Getting Started with NoMachine](https://www.nomachine.com/support/documents/getting-started-with-nomachine)

### 12. Remote Headless
1. Open Terminal and Download Xorg
```
sudo apt-get install xserver-xorg-video-dummy
```
1.1. If failed ```E: Unable to locate package xserver-xorg-video-dummy```. Back up the sources.list
```
sudo mv /etc/apt/sources.list /etc/apt/sources.list.backup
```

1.2. Open ```sources.list```
```
sudo nano /etc/apt/sources.list
```
1.3. Paste the following text
```
deb http://ports.ubuntu.com/ubuntu-ports/ jammy main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ jammy-updates main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ jammy-backports main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ jammy-security main restricted universe multiverse
```
1.4. Update the package
```
sudo apt update
```
1.5. Re install the Xorg
```
sudo apt install xserver-xorg-video-dummy
```
1.6. Remove the previous Xorg config file
```
sudo rm /etc/X11/xorg.conf
```


2. Open Xorg config file
```
sudo nano /etc/X11/xorg.conf
```
3. Replace this text
```
# Copyright (c) 2011-2013 NVIDIA CORPORATION.  All Rights Reserved.

#
# This is the minimal configuration necessary to use the Tegra driver.
# Please refer to the xorg.conf man page for more configuration
# options provided by the X server, including display-related options
# provided by RandR 1.2 and higher.

# Disable extensions not useful on Tegra.
Section "Module"
    Disable     "dri"
    SubSection  "extmod"
        Option  "omit xfree86-dga"
    EndSubSection
EndSection

Section "Device"
    Identifier  "Tegra0"
    Driver      "nvidia"
# Allow X server to be started even if no display devices are connected.
    Option      "AllowEmptyInitialConfiguration" "true"
EndSection
```
To this text
```
Section "Device"
Identifier "Configured Video Device"
Driver "dummy"
# Default is 4MiB, this sets it to 16MiB
VideoRam 16384
EndSection

Section "Monitor"
Identifier "Configured Monitor"
HorizSync 31.5-48.5
VertRefresh 50-70
EndSection

Section "Screen"
Identifier "Default Screen"
Monitor "Configured Monitor"
Device "Configured Video Device"
DefaultDepth 24
SubSection "Display"
Depth 24
Modes "1920x1080"
EndSubSection
EndSection
```
**Before reboot**, MAKE SURE to note Jetson IP adress first to host on the NoMachine or **set a static IP**

4. Reboot jetson
```
sudo reboot
```
In case of forgetting to note the IP address, download Putty and get a USB to USB-C cable   
  a. Connect USB-C to USB2.0 DEBUG   
  b. Open Device Manager -> Ports (COM & LPT); can unplug and plug to see which COM it is   
  c. Double-click the COM -> Port Settings -> Bits per seconds -> 115200   
  d. Open PuTTY → Serial → COMx → 115200 baud   
  e. Open the COM   
  f. Key in Jetson username and password   
  g. Find network interface; common: eth.., enp..., eno...   
  ```
  ip link
  ```
  h. Get the address of the network
  ```
  ip addr show {your network interface}
  ```
  e.g. ip addr show enP8p1s0   
  You would find something like:  inet 192.168.137.169/24  

5. Get into NoMachine


**NoMachine connection setup**

Name: Any friendly name (e.g., `Jetson3`)

Host: `192.168.137.169`

Port: Leave default (`4000`)

Protocol: `NX`

Then connect.   

---
💡 Tip: This IP is usually dynamic after flashing.    

Next time Jetson reboots or reconnects, it might change → NoMachine won’t connect.   

To avoid this, should **set a static IP via NetworkManager**.   

### 14. Internet Sharing on Static IP (PC to Jetson)

### **Scenario: Ubuntu PC → Jetson via Ethernet, Internet on Wi-Fi**
---

#### Step 1: Assign static IPs

You already did:

* PC Ethernet: `192.168.0.105`
* Jetson Ethernet: `192.168.0.103`

Great — now make sure **subnet matches** `/24`:

* PC Ethernet: `192.168.0.105/24`
* Jetson Ethernet: `192.168.0.103/24`

---

#### Step 2: Enable IP forwarding on PC

On your **Ubuntu PC**:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

To make permanent:

```bash
sudo nano /etc/sysctl.conf
```

Add or uncomment:

```
net.ipv4.ip_forward=1
```

---

#### Step 3: Setup NAT (Network Address Translation) on PC

Assuming your **Wi-Fi interface** is `wlp2s0`:

```bash
sudo iptables -t nat -A POSTROUTING -o wlp2s0 -j MASQUERADE
sudo iptables -A FORWARD -i wlp2s0 -o enP8p1s0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i enP8p1s0 -o wlp2s0 -j ACCEPT
```

* `enP8p1s0` = PC Ethernet connected to Jetson
* `wlp2s0` = PC Wi-Fi interface connected to internet

---

#### Step 4: Configure Jetson gateway & DNS

On Jetson:

```bash
sudo ip route add default via 192.168.0.105
```

Set DNS (temporary):

```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

* Now Jetson can reach the internet via PC.

---

#### Step 5: Test

```bash
ping 8.8.8.8       # check internet connectivity
ping google.com    # check DNS resolution
```
---

#### Optional: Make persistent

1. On Jetson, add default route and DNS in **NetworkManager** or `/etc/netplan/…`
2. On PC, use **iptables-persistent** to save NAT rules:

```bash
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

### **Scenario: Windows PC → Jetson via Ethernet**
---

If your PC is Windows:

1. Right-click **Wi-Fi** → Properties → **Sharing**
2. Check **“Allow other network users to connect through this computer’s Internet connection”**
3. Choose **Ethernet** as the target network → Jetson will get internet via Ethernet.

* Jetson can still have a static IP (set gateway = PC Ethernet IP).

---

💡 **Tip:** Make sure PC Ethernet and Jetson Ethernet are on **same subnet** (192.168.0.x) to avoid conflicts.

---
