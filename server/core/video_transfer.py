import base64
import json
from pathlib import Path
from datetime import datetime
from database.db_connector import video_metadata_collection

VIDEO_STORAGE = Path("storage/videos")
VIDEO_STORAGE.mkdir(parents=True, exist_ok=True)

class VideoTransfer:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.in_progress = {}
        
    def request_video(self, mac_address: str, video_file: str):
        """Initiate video transfer from RPi"""
        payload = {
            "mac_address": mac_address,
            "video_file": video_file,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.mqtt_client.client.publish("video/request", json.dumps(payload))
        
    def handle_video_chunk(self, payload):
        """Process incoming video chunks from RPi"""
        data = json.loads(payload)
        
        # Create temporary file for assembling chunks
        temp_file = VIDEO_STORAGE / f"temp_{data['video_file']}"
        
        # Decode and write chunk
        with open(temp_file, "ab") as f:
            f.write(base64.b64decode(data["chunk"]))
            
        # Check if transfer complete
        if data["chunk_index"] == data["total_chunks"] - 1:
            final_path = VIDEO_STORAGE / data["video_file"]
            temp_file.rename(final_path)

            video_metadata_collection.update_one(
                {"video_file": data["video_file"]},
                {"$set": {"location": "server"}}
            )
            
            # Send ACK
            ack_payload = {
                "mac_address": data["mac_address"],
                "video_file": data["video_file"],
                "status": "success",
                "timestamp": datetime.utcnow().isoformat()
            }
            self.mqtt_client.client.publish("video/ack", json.dumps(ack_payload))
