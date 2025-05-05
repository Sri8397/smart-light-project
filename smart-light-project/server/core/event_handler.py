import json
from database.db_connector import motion_logs_collection, video_metadata_collection
from core.mqtt_client import mqtt_client
from datetime import datetime

def handle_event(payload):
    try:
        data = json.loads(payload)

        event_type = data.get("event")

        if event_type == "motion_detected":
            motion_logs_collection.insert_one(data)
            print("[DB] Saved motion log.")
        elif event_type == "motion_ended":
            video_metadata_collection.insert_one(data)
            print("[DB] Saved motion end log.")
            
            # Immediately trigger transfer
            mqtt_client.client.publish(
                "video/request",
                json.dumps({
                    "mac_address": data["mac_address"],
                    "video_file": data["video_file"],
                    "timestamp": datetime.utcnow().isoformat()
                })
            )
            print(f"[AUTO] Requested video transfer for {data['video_file']}")
        else:
            print(f"[WARN] Unknown event type: {event_type}")
    
    except json.JSONDecodeError:
        print("[ERROR] Failed to decode JSON payload.")
