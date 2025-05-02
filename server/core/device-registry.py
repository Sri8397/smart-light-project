from datetime import datetime

device_registry = {}

def update_device(mac_address, data):
    device_registry[mac_address] = {
        "last_seen": datetime.utcnow(),
        **data
    }

def get_devices():
    return device_registry
