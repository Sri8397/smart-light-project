import os
from picamera2 import Picamera2
from datetime import datetime
import requests
from core.state_manager import state

video_dir = "storage/videos"
os.makedirs(video_dir, exist_ok=True)

def record_video():
    cam = Picamera2()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{video_dir}/{timestamp}.h264"
    cam.start_recording(filename)
    cam.sleep(state.get_config()["camera"]["video_duration"])
    cam.stop_recording()

    upload_video(filename)

def upload_video(filepath):
    url = state.get_config()["camera"]["upload_endpoint"]
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f)}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("Upload success, deleting local file")
            os.remove(filepath)
        else:
            print("Upload failed:", response.status_code)
