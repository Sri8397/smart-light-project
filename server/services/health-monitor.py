from datetime import datetime, timedelta
from core.device_registry import get_devices

def check_inactive_devices(timeout=300):
    now = datetime.utcnow()
    inactive = []
    for mac, data in get_devices().items():
        if (now - data["last_seen"]) > timedelta(seconds=timeout):
            inactive.append(mac)
    return inactive
