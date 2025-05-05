from gpiozero import MotionSensor, LED
from threading import Timer
from core.state_manager import state
from core.mqtt_client import mqtt_client
from time import sleep, time, strftime
from pathlib import Path
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import os

pir = MotionSensor(17)
led = LED(27)
motion_timeout = state.get_config()["camera"]["video_duration"]  # seconds

VIDEO_DIR = Path(__file__).parent.parent / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

class MotionMonitor:
    def __init__(self):
        self.timer_thread = None
        self.active = False
        self.waiting_printed = False
        self.motion_start_time = None

        # Initialize camera
        self.camera = Picamera2()
        video_config = self.camera.create_video_configuration()
        self.camera.configure(video_config)
        self.encoder = H264Encoder()
        self.output = None
        self.video_filename = None

    def timeout_handler(self):
        motion_end_time = time()
        duration_ms = int((motion_end_time - self.motion_start_time) * 1000)

        print("Motion period ended. Turning off LED.")
        led.off()
        state.motion_active = False
        state.recording = False
        self.active = False
        self.waiting_printed = False

        # Stop recording
        self.camera.stop_recording()
        print(f"Recording stopped. Saved to: {self.video_filename}")

        # Publish "motion_ended" event
        mqtt_client.publish_event("motion_ended", {
            "motion_duration_ms": duration_ms,
            "video_file": str(self.video_filename.name),
            # "video_file": str(self.video_filename),
        })

    def reset_motion_timer(self): 
        if self.timer_thread is not None:
            self.timer_thread.cancel()
        self.timer_thread = Timer(motion_timeout, self.timeout_handler)
        self.timer_thread.start()

    def motion_detected(self):
        if not self.active:
            print("Motion detected")
            self.motion_start_time = time()
            state.motion_active = True
            state.recording = True
            mqtt_client.publish_event("motion_detected")
            led.on()
            self.start_video_recording()
            self.active = True

        self.reset_motion_timer()
        self.waiting_printed = False

    def start_video_recording(self):
        timestamp = strftime("%Y%m%d_%H%M%S")
        self.video_filename = VIDEO_DIR / f"motion_{timestamp}.mp4"
        self.output = FfmpegOutput(str(self.video_filename))

        self.camera.start()
        self.camera.start_recording(self.encoder, self.output)
        print(f"Recording started: {self.video_filename}")

    def run(self):
        print("Motion monitor started.")
        while True:
            if pir.motion_detected:
                self.motion_detected()
            else:
                if not self.waiting_printed and not self.active:
                    print("Waiting for motion...")
                    self.waiting_printed = True
                sleep(0.2)

motion_monitor = MotionMonitor()
