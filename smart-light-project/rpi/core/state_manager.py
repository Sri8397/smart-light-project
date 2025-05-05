import yaml

class GlobalState:
    def __init__(self, config_path='config/settings.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.motion_active = False
        self.recording = False
        self.last_motion_time = None

    def get_config(self):
        return self.config

state = GlobalState()
