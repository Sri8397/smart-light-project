import paho.mqtt.client as mqtt
import json
from database.mongo_client import get_db
from core.state_manager import state
from core.device_registry import update_device

config = state.get_config()["mqtt"]
db = get_db()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")
    client.subscribe(config["topic_subscribe"])

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print(f"MQTT Message: {payload}")
    
    mac = payload.get("mac_address")
    if mac:
        update_device(mac, {"status": "online"})

    db.logs.insert_one(payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(config["broker"], config["port"])
client.loop_start()

def send_control(mac, command):
    payload = {
        "mac_address": mac,
        "command": command
    }
    client.publish(config["topic_control"], json.dumps(payload))
