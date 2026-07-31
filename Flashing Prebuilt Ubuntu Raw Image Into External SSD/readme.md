# Flashing a Prebuilt Raw Image directly to your External SSD**.

Because Canonical (Ubuntu's parent company) primarily provides raw `.img` files for **Ubuntu Server** and **Ubuntu Core** rather than Ubuntu Desktop, this method involves flashing a raw server image directly to the drive and then installing the Desktop interface on first boot.

---

### Step 1: Download the Prebuilt Raw Image

1. Go to the official Ubuntu Cloud Releases page: [cloud-images.ubuntu.com/releases/](https://cloud-images.ubuntu.com/releases/).
2. Select the latest **LTS release** (e.g., `24.04` or `26.04`).
3. Download the raw disk image for standard 64-bit PCs:
* Look for the file ending in **`.img`** or **`-disk1.img`** under `amd64` (e.g., `ubuntu-XX.XX-server-cloudimg-amd64.img`).



---

### Step 2: Flash the Raw Image Directly to Your External SSD

> **CRITICAL WARNING:** Double-check to select **External SSD** and **NOT your internal Windows/Mac drive**. Flashing will completely erase the target drive.

1. Connect **External SSD** to computer.
2. Open **BalenaEtcher** (or **Rufus** on Windows).
3. Click **Flash from file** and select the `.img` file downloaded.
4. Click **Select target** and choose correct **External SSD** (verify using its capacity, e.g., 250 GB / 500 GB / 1 TB).
5. Click **Flash!** and wait for the process to complete.

---

### Step 3: Boot into the External SSD for the First Time

1. Leave the External SSD plugged into PC.
2. Restart the computer and press **Boot Menu key** (`F12`, `F11`, `F8`, or `Option` on Mac) during startup.
3. Select correct **External SSD** from the list to boot from it.
4. It will boot directly into a terminal prompt without needing a Live USB installer. Log in with the default terminal prompts.

---

### Step 4: Install the Desktop GUI (Ubuntu Desktop)

Since the raw image is a minimal command-line system, run a command to install the full Ubuntu Desktop interface:

1. Ensure the PC is connected to the internet (via Ethernet or run `ncli` / `netplan` for Wi-Fi).
2. Type the following command and press Enter:
```bash
sudo apt update && sudo apt install ubuntu-desktop -y

```


3. Once the package download and installation finishes, reboot the drive:
```bash
sudo reboot

```



When the drive restarts, it will launch straight into the full graphical **Ubuntu Desktop** setup wizard.

---
