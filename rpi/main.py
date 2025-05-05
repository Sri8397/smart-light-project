from core.mqtt_client import mqtt_client
from core.motion_detector import motion_monitor
import signal
import sys
import time

def graceful_exit(signum, frame):
    print("\n[System] Exiting gracefully...")
    mqtt_client.stop()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, graceful_exit)
    mqtt_client.loop_start()

    # Give MQTT time to connect and print output
    time.sleep(2)

    motion_monitor.run()

if __name__ == "__main__":
    main()
