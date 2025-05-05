import paho.mqtt.client as mqtt
import json
from datetime import datetime
from core.state_manager import state
from database.db_connector import video_metadata_collection, motion_logs_collection, devices_collection

config = state.get_config()["mqtt"]

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(config["broker"], config["port"])

    def on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] Connected to broker {config['broker']} (code {rc})")
        self.client.subscribe(config["topic_subscribe"])

    def on_message(self, client, userdata, msg):
        print(f"[MQTT] Received: {msg.payload.decode()}")
        print(f"[MQTT] Topic: {config['topic_subscribe']}")

        if msg.topic == config["topic_subscribe"]:
            try:
                payload = json.loads(msg.payload.decode())
                event_type = payload.get("event")
                mac = payload.get("mac_address")
                
                # find the mac address in the database
                mac_present = devices_collection.find_one({"mac_address": mac})
                if not mac_present:
                    devices_collection.insert_one({"mac_address": mac})
                    print(f"[DB] New device detected: {mac}")
                
                if event_type == "motion_detected":
                    motion_logs_collection.insert_one(payload)
                    print("[DB] Saving motion log.")
                elif event_type == "motion_ended":
                    print("[DB] Saving motion end log.")

                    # add also location
                    payload["location"] = "rpi"
                    video_metadata_collection.insert_one(payload)
                    print(f"[AUTO] Requested video transfer for {payload['video_file']}")

                    self.publish_event("video_upload_request", {
                        "mac_address": payload["mac_address"],
                        "video_file": payload["video_file"],
                    })
                else:
                    print(f"[MQTT] Unknown event type: {event_type}")
            except json.JSONDecodeError:
                print("[MQTT] Failed to decode JSON payload.")

    def publish_event(self, event_type, extra_data=None):
        payload = {
            "server_mac_address": state.get_config()["mqtt"]["mac_address"],  # Get MAC address from the config
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        if extra_data:
            payload.update(extra_data)
        print(f"[MQTT] Publishing event: {event_type} with payload: {payload}")
        print(f"[MQTT] Topic: {config['topic_publish']}")
        self.client.publish(config["topic_publish"], json.dumps(payload))

    def loop_start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

mqtt_client = MQTTClient()