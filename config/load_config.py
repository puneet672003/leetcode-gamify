import os
import json


class Config:
    def __init__(self, config_path=None):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.config_path = config_path or os.path.join(self.base_dir, "config.json")

        self.config = None
        self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        self.config = config

    def get_users(self):
        if self.config is not None:
            return self.config.get("users", [])
        return []
