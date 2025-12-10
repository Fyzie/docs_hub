# Case Study on Jetson Nano

## A. Using the Startup Applications Menu
You can add your script to the Startup Applications, typically found in the system menu.
 Example command:
```
python3 /home/jetson/script.py
```

Limitation: This method will not work if you need the script to run before the user logs in (e.g., before the password login screen).

---
## B. Using systemd to Run the Script at Boot (Works on Login Page)
### 1. Place the Python Script in a Suitable Location
Save your Python script in a specific directory, for example:   
```
/home/your_username/scripts/my_script.py
````
Make the script executable:   
```
chmod +x /home/your_username/scripts/my_script.py
```
### 2. Create a systemd Service File
#### 2.1. Using nano
Create a new service file:
```
sudo nano /etc/systemd/system/my_script.service
```
If nano command not found:
```
sudo apt install nano
```
#### 2.2. Using vscode
Run vscode as admin on terminal :
```
sudo code --no-sandbox --user-data-dir="/root/.vscode-root"
```

Create a new service file and save as:
```
/etc/systemd/system/my_script.service
```
### 3. Configure the Service File
Add the following content to the service file:
```
[Unit]
Description=Run Python Script at Boot
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/your_username/scripts/my_script.py
Restart=on-failure
User=your_username
WorkingDirectory=/home/your_username/scripts
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

#### Deployed on Jetson reComputer with miniconda3 env for Lens AVI
```
[Unit]
Description=Run Lens AVI at Boot
After=multi-user.target

[Service]
Type=simple
ExecStart=/home/jetson2/miniconda3/envs/pygpu/bin/python /home/jetson2/Documents/lens_avi/jetson_listener.py
Restart=on-failure
User=jetson2
WorkingDirectory=/home/jetson2/Documents/lens_avi
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

 Replace your_username with your actual Jetson Nano username.

### 4. Reload systemd and Enable the Service
Reload systemd to apply the changes:
```
sudo systemctl daemon-reload
```
Enable the service to run at boot:
```
sudo systemctl enable my_script.service
```
### 5. Test the Service
Start the service manually to test it without rebooting:
```
sudo systemctl start my_script.service
```
### 6. Verify the Service
Check the status of the service to ensure it is running:
```
systemctl status my_script.service
```
Managing the systemd Service
Immediate restart the Service
```
sudo systemctl restart my_script.service
```
Stopping and Disabling the Service
Stop the service immediately:
```
sudo systemctl stop my_script.service
```
Prevent the service from starting at boot:
```
sudo systemctl disable my_script.service
```
Optional: Removing the Service File
If you no longer need the service, delete the service file:
```
sudo rm /etc/systemd/system/my_script.service
```
Reload the systemd daemon to apply changes:
```
sudo systemctl daemon-reload
```
## Viewing Logs for the Service
### 1. View Logs
To check detailed logs for the service:
```
sudo journalctl -u my_script.service
```
### 2. View Live Logs
To view live logs in real-time:
```
sudo journalctl -u my_script.service -f
```
### 3. View Logs from a Specific Time Period
To view logs from the last 10 minutes:
```
sudo journalctl -u my_script.service --since "10 minutes ago"
```
## Arising Issues To Run Script Before Log In Page by 27 Nov 2024
### 1. cv2.imshow and QT Platform Requirements
#### Problem:
cv2.imshow requires a QT platform to display images, causing dependency issues in a headless environment or when the DISPLAY variable is not set.
#### Symptoms:
Errors such as qt.qpa.xcb could not connect to display and QT platform plugin xcb could not be initialized.
#### Solution:

Echo display at terminal

```
echo $DISPLAY
```
Sample Output
```
:1
```
Add display environment in service file

```
Environment=DISPLAY=:1
```
However, this still not solved display at login page…only works after login when service restarts

### 2. Writing Results to USB Drive
#### Problem:
Writing results to a USB drive can fail if the drive is not mounted or has insufficient permissions.
#### Symptoms:
File writing operations fail or raise exceptions.
Results are lost if the USB path is unavailable.

For now, avoid the above implementations within the script until issues are solved. These issues seem to stem from the system being at the password login page, requiring additional setup to ensure display access and proper mounting of external drives


### 3. Access to Basler Camera daA4200 particularly for Jetson Nano
#### Problem:
Access to real cameras of daA4200 through service file.
#### Symptoms:
File writing operations fail or raise exceptions.
Solution:


### 1. Check Camera Permissions
Ensure your service user (jetson) has sufficient permissions to access the camera hardware:
#### List connected cameras:

```
ls /dev/video*
```
#### Check the permissions:

```
ls -l /dev/video*
```
Example output:

```
crw-rw----+ 1 root video 81, 0 Nov 28 10:00 /dev/video0
```
#### Add the service user to the video group if necessary:

```
sudo usermod -aG video jetson
```
#### After adding the user to the group, verify the membership:

```
groups jetson
```
#### Add library path of pylon and bcon in service file
Pylon files with *.so   
Bcon files with *.cti
#### Example Final Service File (on Jetson Nano for Minitopled AVI)
```
[Unit]
Description=Run Python Script at Boot
After=multi-user.target

[Service]
Type=simple
ExecStartPre=/bin/sleep 10
ExecStart=/usr/bin/python3 /home/your_username/scripts/my_script.py
Restart=on-failure
User=your_username
Environment=DISPLAY=:1
Environment=PYLON_CAMEMU=0
Environment=LD_LIBRARY_PATH=/opt/pylon/lib:$LD_LIBRARY_PATH
Environment=GENICAM_GENTL64_PATH=/opt/dart-bcon-mipi/lib
SupplementaryGroups=video

[Install]
WantedBy=multi-user.target
```


