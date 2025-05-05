import paho.mqtt.client as mqtt
import json
from datetime import datetime
from core.state_manager import state
from core.handle_event import handle_event

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

        if msg.topic == config["topic_subscribe"]:
            handle_event(msg.payload)

    def publish_event(self, event_type, extra_data=None):
        payload = {
            "mac_address": state.get_config()["device"]["mac_address"],
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        if extra_data:
            payload.update(extra_data)

        self.client.publish(config["topic_publish"], json.dumps(payload))
        print(f"[MQTT] Published event: {event_type}")

    def loop_start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

mqtt_client = MQTTClient()
