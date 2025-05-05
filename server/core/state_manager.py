import yaml

class StateManager:
    def __init__(self):
        with open("config/server_config.yaml") as f:
            config = yaml.safe_load(f)
            self.mqtt = config["mqtt"]
            self.server = config["server"]
            self.db = config["db"]

    def get_config(self):
        return {
            "mqtt": self.mqtt,
            "server": self.server,
            "db": self.db
        }

# Global instance of the StateManager to be used across the project
state = StateManager()
