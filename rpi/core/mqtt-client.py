import paho.mqtt.client as mqtt
import json
from core.state_manager import state

config = state.get_config()["mqtt"]

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(config["broker"], config["port"])

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker")
        self.client.subscribe(config["topic_subscribe"])

    def on_message(self, client, userdata, msg):
        print("Received MQTT message:", msg.payload.decode())

    def publish_event(self, event_type, extra_data=None):
        payload = {
            "mac_address": state.get_config()["device"]["mac_address"],
            "event": event_type,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
        if extra_data:
            payload.update(extra_data)

        self.client.publish(config["topic_publish"], json.dumps(payload))

    def loop(self):
        self.client.loop_start()

mqtt_client = MQTTClient()
