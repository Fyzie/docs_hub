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

Download same for your host PC.   
[NoMachine Website](https://www.nomachine.com/)   
[Getting Started with NoMachine](https://www.nomachine.com/support/documents/getting-started-with-nomachine)

#### For headless monitor,
Create Xorg config
```
sudo nano /etc/X11/xorg.conf
```
Paste:
```
Section "Device"
    Identifier "Device0"
    Driver "nvidia"
    Option "AllowEmptyInitialConfiguration" "true"
EndSection

Section "Monitor"
    Identifier "Monitor0"
    HorizSync 28.0-80.0
    VertRefresh 48.0-75.0
    Option "DPMS"
EndSection

Section "Screen"
    Identifier "Screen0"
    Device "Device0"
    Monitor "Monitor0"
    DefaultDepth 24
    SubSection "Display"
        Depth 24
        Virtual 1920 1080
    EndSubSection
EndSection
```
Save and exit.   
Force-load a fake EDID
```
sudo mkdir -p /lib/firmware/edid/
wget https://raw.githubusercontent.com/ajslater/edid-generator/master/edid.bin -O /lib/firmware/edid/fake_1920x1080.bin
sudo nano /boot/extlinux/extlinux.conf
video=HDMI-A-0:1920x1080@60D drm.edid_firmware=HDMI-A-0:edid/fake_1920x1080.bin
APPEND ${cbootargs} video=HDMI-A-0:1920x1080@60D drm.edid_firmware=HDMI-A-0:edid/fake_1920x1080.bin
```
```
sudo reboot
```
#### In case to remove back,
```
sudo rm /etc/X11/xorg.conf
sudo reboot
```




