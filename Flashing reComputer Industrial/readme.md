# Flashing reComputer Industrial J3011
NVIDIA Jetson Orin Nano 8GB, 40TOPS

Requirements:
1. PC with Ubuntu (Tested on version 22.04)
2. USB Type-C cable
3. Pin

## Install Ubuntu
[Desktop Image](https://releases.ubuntu.com/22.04/?_gl=1*1gj7xvh*_gcl_au*MTU0NzE3NzI1MS4xNzg1NDYyNzk2Li0uLS4xNzg1NDYyNzk1LjE3NjM2ODQ2MTMuMTc4NTU2MDMxMS4xNzg1NTYwMzE1)
> For external SSD installation
   
1. Flash the downloaded image into SD card using [BalenaEtcher](https://etcher.balena.io/)   
> While connecting the SD card and external SSD,
2. Get into One Time Boot Menu (F12 during PC boot)
3. Install the image manually
4. Choose the external SSD (Add + fat32/vfat and ext4 space mounted on root / for the external ssd)

## Flash Jetson
[Original Guide](https://wiki.seeedstudio.com/reComputer_Industrial_Getting_Started/)
   
1. Enter Force Recovery Mode
  - Connect a USB Type-C cable between USB2.0 DEVICE port and your PC.
  - Use a pin and insert into the RECOVERY hole to press recovery button and while holding this.
  - Connect the included 2-Pin Terminal block power connector to the power connector on the board and connect the included power adapter with a power cord to turn on the board.
  - Release the recovery button.
    
2. On Ubuntu,
  - Download **correct** Jetpack 6.2 image correspond to the Jetson model (e.g. J3011 Orin Nano 8GB)
  > Carefully look at the device table and jetpack filename
  - Go to the Downloads directory and extract the image file
    ```
    sudo tar -xvf <file_name>.tar.gz
    ```
  - Go to the extracted directory
    ```
    cd mfi_xxx
    ```
  - Flash the image
    ```
    sudo ./tools/kernel_flash/l4t_initrd_flash.sh --flash-only --massflash 1 --network usb0 --showlogs
    ```
