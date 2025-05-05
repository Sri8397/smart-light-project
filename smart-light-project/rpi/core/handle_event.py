import os
import json
import requests
from pathlib import Path
from core.state_manager import state

VIDEO_DIR = Path(__file__).parent.parent / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def handle_event(payload):
    try:
        data = json.loads(payload)
        event = data.get("event")

        if event == "video_upload_request":
            handle_upload_request(data)
        elif event == "video_upload_ack":
            handle_acknowledgment(data)
        else:
            print(f"[Event] Unknown event: {event}")
    except Exception as e:
        print(f"[Event] Error: {e}")

def handle_upload_request(data):
    try:
        requested_mac = data.get("mac_address")
        filename = data.get("video_file")
        device_mac = state.get_config()["device"]["mac_address"]

        if requested_mac != device_mac:
            print("[Upload] MAC address does not match. Ignoring.")
            return
        filepath = VIDEO_DIR / filename
        print("filepath: ", filepath)

        if not filepath.exists():
            print(f"[Upload] File not found: {filepath}")
            return

        url = state.get_config()["camera"]["upload_endpoint"]

        with open(filepath, 'rb') as f:
            files = {'file': (filename, f, 'video/mp4')}
            data = {
                'mac_address': device_mac,
                'filename': filename
            }
            print(data, files)
            response = requests.post(url, files=files, data=data) 

        if response.status_code == 200:
            print(f"[Upload] Success. Server stored video.")
        else:
            print(f"[Upload] Failed. Server error: {response.status_code}")

    except Exception as e:
        print(f"[Upload] Error: {e}")

def handle_acknowledgment(data):
    try:
        filename = data.get("filename")
        status = data.get("status")

        if status == "received":
            filepath = VIDEO_DIR / filename
            if filepath.exists():
                print(f"[Delete] Video upload successful. Deleting {filename}")
                os.remove(filepath)
            else:
                print(f"[Delete] File not found for deletion: {filename}")
        else:
            print(f"[Delete] Server did not acknowledge upload success for {filename}")
    except Exception as e:
        print(f"[Delete] Error while processing acknowledgment: {e}")
