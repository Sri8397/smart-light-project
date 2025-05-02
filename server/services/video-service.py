import os
from flask import request
from werkzeug.utils import secure_filename
from core.state_manager import state
from core.mqtt_handler import send_control

video_dir = state.get_config()["video_storage"]
os.makedirs(video_dir, exist_ok=True)

def save_video():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(video_dir, filename)
    file.save(filepath)

    # Notify RPi to delete local file
    mac = filename.split("_")[0]  # assume file named like <mac>_<timestamp>.h264
    send_control(mac, "delete_video")
    return {"message": "Video received", "filename": filename}
