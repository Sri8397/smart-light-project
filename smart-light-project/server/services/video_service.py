import os
from fastapi import UploadFile
from core.state_manager import state

config = state.get_config()["server"]

def save_uploaded_video(file: UploadFile, filename: str):
    upload_path = config["video_upload_path"]
    os.makedirs(upload_path, exist_ok=True)
    file_path = os.path.join(upload_path, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path
