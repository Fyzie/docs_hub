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

### Option 1. Flash Jetpack 6.x Using NVIDIA SDK Manager


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

### Option 2. (Recommended) Flash Jetpack 6.x Using Downloadable System Image
Refer [here](https://github.com/Fyzie/docs_hub/tree/main/reComputer%20Industrial%20Flashing%20Steps)
   
or   
   
1. Youtube Guide [link](https://www.youtube.com/watch?v=poQ4JQw56Gc)
2. Website Documentation [link](https://wiki.seeedstudio.com/reComputer_J4012_Flash_Jetpack/)

---
## **On Jetson,**

### 2. Update & Install JetPack SDK + CUDA (If none installed initially)

```bash
sudo apt update
```
If you had problems with the update, might be due to backdated clock:
1. Check Current System Date
```
date
```
2. Enable Network Time Sync (NTP)
```
sudo timedatectl set-ntp true
```
3. Set Date Manually (If NTP fails to sync automatically)
```
sudo date -s "2026-08-07 10:10:00"
```
4. Verify Hardware Clock Sync
```
sudo hwclock --systohc
```
Then, you can update back the system

If your Jetson has issue no cuda detected through [jtop](https://github.com/Fyzie/docs_hub/tree/main/reComputer%20Industrial%206.x%20Setup#5-install-jtop-jetson-stats), do below:
```
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
```
sudo chown -R $USER:$USER ~/Downloads
cd ~/Downloads
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
sudo pip3 install -U jetson-stats
sudo jtop --install-service
sudo reboot
```

---

### 6. Install Miniconda (AArch64) or Virtual Environment
> WARNING: I would recommend to just use and install everything on NATIVE python :)   
> to avoid unnecessary issues with CUDA/ CUDNN within environments   

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
conda init --all
```
Alternatively, can use python virtual environment:
```
sudo apt install python3.10-venv
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
Alternatively, to activate virtual environment:
```
source myenv/bin/activate
```

---

### 9. Install Dependencies
> In case got warning about pip PATH:
```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

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
If error,
```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/arm64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cudss
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

### 11. Install Remote Desktop App (Deprecated)

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

### 12. Remote Headless (Optional if you dont have GUI-based script)
#### 1. Open Terminal and Download Xorg
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


#### 2. Open Xorg config file
```
sudo nano /etc/X11/xorg.conf
```
#### 3. Replace this text
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

#### 4. Reboot jetson
```
sudo reboot
```
In case of forgetting to note the IP address, download Putty and get a USB to USB-C cable   
- Connect USB-C to USB2.0 DEBUG
- Open Device Manager -> Ports (COM & LPT); can unplug and plug to see which COM it is
- Double-click the COM -> Port Settings -> Bits per seconds -> 115200   
-  Open PuTTY → Serial → COMx → 115200 baud   
-  Open the COM   
-  Key in Jetson username and password   
-  Find network interface; common: eth.., enp..., eno...   
```
ip link
```
- Get the address of the network
```
ip addr show {your network interface}
```
e.g. ip addr show enP8p1s0   
You would find something like:  inet 192.168.137.169/24  

#### 5. Get into NoMachine


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

#### 6. Remote Headless Removal

6.1 Remove the dummy Xorg driver
```
sudo apt remove --purge xserver-xorg-video-dummy
sudo apt autoremove
```
6.2 Restore / remove the custom Xorg config (Recommended)   
The dummy mode only works because of /etc/X11/xorg.conf.   
Just delete it and let Jetson auto-detect HDMI:   
```
sudo rm /etc/X11/xorg.conf
```
6.3 Restore NVIDIA default behavior   
Make sure you are NOT forcing “AllowEmptyInitialConfiguration”.   
Check if any leftover configs exist:   
```
ls /etc/X11/xorg.conf.d/
```
If you see files like:
```
10-dummy.conf
99-headless.conf
```
delete them:
```
sudo rm /etc/X11/xorg.conf.d/*.conf
```
6.4 Make sure graphical target is enabled
```
sudo systemctl set-default graphical.target
```
6.5 Reboot
```
sudo reboot
```

### 14. Internet Sharing on Static IP (PC to Jetson)

### **Scenario: Windows PC → Jetson via Ethernet**
---

#### Windows ICS automatically sets the PC Ethernet IP

When you enable ICS on the Wi-Fi adapter:

- Windows **forces the Ethernet adapter to 192.168.137.1** (default ICS subnet)

- It automatically acts as **gateway and DNS server** for the connected device.

If manually set PC Ethernet to custom static IP, ICS may not work properly.

#### Correct Windows ICS setup for Jetson

**1. Reset PC Ethernet to automatic (DHCP):**

- Go to **Network Connections → Ethernet → Properties → IPv4 → Obtain IP automatically**

**2. Enable ICS on Wi-Fi:**

- Right-click **Wi-Fi → Properties → Sharing**

- Check **“Allow other network users to connect through this computer’s Internet connection”**

- Select **Ethernet** as the “Home networking connection”

**3. Windows will now:**

- Set Ethernet IP to **192.168.137.1**

- Assign connected devices **192.168.137.x** via DHCP automatically

**4. Set Jetson to DHCP on Ethernet** (or manually set IP in the 192.168.137.x range, gateway `192.168.137.1`, DNS `192.168.137.1`)

Example:
```
Jetson IP: 192.168.137.x
Subnet mask: 255.255.255.0
Gateway: 192.168.137.1
DNS: 192.168.137.1
```

Basically, Jetson gateway has to be same as Windows Ethernet IP   

`ping 8.8.8.8` or `ping google.com` to test internet connection on Jetson   

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

