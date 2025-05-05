# Smart Light Project

A smart light control system using FastAPI and MQTT, with support for video uploads from Raspberry Pi devices and real-time event tracking.

---

## Features

- **REST API** for controlling and monitoring smart lights
- **MQTT integration** for real-time communication with Raspberry Pi devices
- **Video upload endpoint** for motion-triggered video files
- **Automatic video transfer** and metadata tracking
- **Cross-origin (CORS) support** for web and mobile clients

---

## Requirements

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [paho-mqtt](https://pypi.org/project/paho-mqtt/)
- [requests](https://pypi.org/project/requests/)
- MongoDB (for metadata storage)

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/smart-light-project.git
    cd smart-light-project
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your settings:**
    - Edit `core/state_manager.py` and update MQTT, camera, and database configurations as needed.

---

## Running the Server

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000/` (or your configured port).

---

## API Endpoints

### Health Check

```http
GET /
```

### Upload Video

```http
POST /upload_video
```
**Form Data:**
- `file`: Video file (binary)
- `mac_address`: MAC address of the device
- `filename`: Name of the video file

**Example (Python requests):**
```python
import requests

url = "http://:8000/upload_video"
mac_address = "B8:27:EB:45:12:34"
filename = "motion_20250505_030159.mp4"
filepath = "/path/to/motion_20250505_030159.mp4"

with open(filepath, 'rb') as f:
    files = {'file': (filename, f, 'video/mp4')}
    data = {'mac_address': mac_address, 'filename': filename}
    response = requests.post(url, files=files, data=data)
    print(response.json())
```

### Get Motion Logs

```http
GET /logs
```
Returns a JSON array of motion event logs.

---

## MQTT Integration

- The server uses MQTT to communicate with Raspberry Pi devices.
- Topics used:  
  - `smartlight/control` (for control and ACK messages)
  - `video/request` (to request video transfer)
  - `video/data` (for video chunks)
  - `video/ack` (for transfer acknowledgments)

**Example:**
- When a motion event ends, the RPi uploads the video and metadata.
- The server sends an ACK via MQTT after successful upload.

---

## Video Storage

- Uploaded videos are saved under `./videos//`.
- Metadata is stored in the configured MongoDB collection, with a `location` field indicating if the video is on the RPi or server.

---

## Troubleshooting

- **422 Unprocessable Entity:** Ensure all required form fields are provided in the upload request.
- **MQTT connection errors:** Check broker address, port, and credentials.
- **File content type is None:** Specify the content type in the `files` dictionary when uploading.

---

## License

MIT License

---

## Authors

- [Srikant Agrawal](https://github.com/sri8397)
- [Rupika Sinha](https://github.com/akipur)

---
