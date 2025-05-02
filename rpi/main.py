from core.mqtt_client import mqtt_client
from core.motion_detector import motion_monitor

def main():
    mqtt_client.loop()
    motion_monitor.run()

if __name__ == "__main__":
    main()
