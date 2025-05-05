# Smart Light System - Setup Guide

---

## 📟 Raspberry Pi (Device) Setup

1. Install dependencies:
   $ python3 -m venv --system-site-packages venv && source venv/bin/activate && pip install -r requirements.txt

2. Configure `config/settings.yaml` with your device and broker details.

3. Run the project:
   $ python main.py

4. Enable the camera and connect the PIR sensor to GPIO4:
   $ sudo raspi-config
   (Go to: Interface Options > Camera > Enable)

5. Video files are uploaded and deleted upon server acknowledgment.

6. Set up the system to auto-run on boot using systemd:

   a. Create a service file:
      $ sudo nano /etc/systemd/system/smartlight.service

   b. Paste the following content (update paths if needed):

      [Unit]
      Description=Smart Light System
      After=network.target

      [Service]
      User=pi
      WorkingDirectory=/home/pi/smartlight
      ExecStart=/home/pi/smartlight/venv/bin/python /home/pi/smartlight/main.py
      Restart=always
      RestartSec=5

      [Install]
      WantedBy=multi-user.target

   c. Enable and start the service:
      $ sudo systemctl daemon-reexec && sudo systemctl daemon-reload
      $ sudo systemctl enable smartlight.service
      $ sudo systemctl start smartlight.service

   d. Check service status or logs:
      $ sudo systemctl status smartlight.service
      $ journalctl -u smartlight.service -e

---

## 🖥️ Server Setup

1. Create and activate a virtual environment:
   $ python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

2. Set up MongoDB (local or remote), and configure `config/settings.yaml` with:
   - DB URI and collection names
   - MQTT broker settings

3. Run the server:
   $ python main.py

4. Available API Endpoints:

   - POST `/api/upload-video`  
     Upload video files from Raspberry Pi

   - GET `/api/logs`  
     Retrieve motion detection logs

   - GET `/api/devices`  
     List currently known devices

   - POST `/api/control`  
     Send control commands (e.g., turn LED on/off on a specific RPi)

---

✅ Ensure both Raspberry Pi and server use matching MQTT topics and device MAC configurations.
