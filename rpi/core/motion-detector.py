from gpiozero import MotionSensor
from time import sleep, time
from threading import Thread
from picamera2 import Picamera2
from core.state_manager import state
from core.mqtt_client import mqtt_client
from storage.video_manager import record_video

pir = MotionSensor(4)  # GPIO pin 4
video_timeout = state.get_config()["camera"]["video_duration"]

class MotionMonitor:
    def __init__(self):
        self.timer_thread = None
        self.reset_flag = False

    def motion_detected(self):
        print("Motion detected")
        state.motion_active = True
        mqtt_client.publish_event("motion_detected")
        if not state.recording:
            self.start_recording_timer()

    def start_recording_timer(self):
        state.recording = True
        self.reset_flag = False
        self.timer_thread = Thread(target=self.recording_thread)
        self.timer_thread.start()

    def recording_thread(self):
        start_time = time()
        while time() - start_time < video_timeout:
            if pir.motion_detected:
                start_time = time()  # Reset timer
            sleep(1)
        print("Recording video...")
        record_video()
        state.recording = False
        state.motion_active = False

    def run(self):
        while True:
            pir.wait_for_motion()
            self.motion_detected()

motion_monitor = MotionMonitor()
