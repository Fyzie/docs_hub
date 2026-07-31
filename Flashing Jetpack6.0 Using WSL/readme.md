# Flashing Jetpack6.0 Using WSL

## 1. Download the image
Link [here](https://wiki.seeedstudio.com/reComputer_Industrial_Getting_Started/)

## 2. Install WSL on Windows
On Windows Powershell,
```
wsl.exe --list --online
```
```
wsl.exe --install Ubuntu-24.04
```
## 3. Install usbipd
On Windows Powershell,
```
winget install usbipd
```
## 4. Turn on Jetson into Recovery Mode
Steps for Recovery Mode [here](https://wiki.seeedstudio.com/reComputer_Industrial_Getting_Started/)

## 5. Check for NVIDIA Recovery Device
On Windows Powershell,

```
usbipd list
```
Locate the NVIDIA recovery device in the list (typically named APX or NVIDIA Corp.   
`Note its BUSID (e.g., 2-8)`

## 6. Bind the device to WSL
On Windows Powershell,

```
usbipd bind --busid <BUS-ID> --force
```
(Keep your WSL terminal open in the background while you run this!)

```
usbipd attach --wsl --busid <BUS-ID> --auto-attach
```

## 7. Check the bind to WSL
On WSL terminal,
```
lsusb
```
Similar ouput: `Bus 001 Device 002: ID 0955:7523 NVidia Corp.`

## 8. Flash the image
Go to the image folder,   
(e.g., your home folder or a path on your C drive like /mnt/c/Users/<YourUsername>/Downloads):
```
cd ~
```
Extract the file
```
sudo tar -xvf <file_name>.tar.gz
```
