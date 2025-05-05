
# Smart Light System - Setup Guide

---

## 📟 Raspberry Pi (Device) Setup

1. Install dependencies:

   ```bash
   python3 -m venv --system-site-packages venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure `config/settings.yaml` with your device and broker details.

3. Run the project:

   ```bash
   python main.py
   ```

4. Enable the camera and connect the PIR sensor to GPIO4:

   ```bash
   sudo raspi-config
   ```

   Navigate to: **Interface Options > Camera > Enable**

5. Video files are uploaded and deleted upon server acknowledgment.

6. Set up auto-start on boot with systemd:

   a. Create the service file:

   ```bash
   sudo nano /etc/systemd/system/smartlight.service
   ```

   b. Paste the following (adjust paths as needed):

   ```ini
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
   ```

   c. Enable and start the service:

   ```bash
   sudo systemctl daemon-reexec
   sudo systemctl daemon-reload
   sudo systemctl enable smartlight.service
   sudo systemctl start smartlight.service
   ```

   d. Check service status or logs:

   ```bash
   sudo systemctl status smartlight.service
   journalctl -u smartlight.service -e
   ```

---

## 🖥️ Server Setup

1. Set up virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set up MongoDB (local or remote) and configure `config/settings.yaml`:

   * Database URI and collection names
   * MQTT broker configuration

3. Run the server:

   ```bash
   python main.py
   ```

4. Available API Endpoints:

   * `POST /api/upload-video` – Upload video files from Raspberry Pi
   * `GET /api/logs` – View motion detection logs
   * `GET /api/devices` – List known/connected devices
   * `POST /api/control` – Send control commands (e.g., LED on/off)
