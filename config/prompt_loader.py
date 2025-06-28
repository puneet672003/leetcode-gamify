import os
import json


class PromptManager:
    def __init__(self, prompts_folder="prompts", config_path=None):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.prompt_dir = os.path.join(self.base_dir, prompts_folder)
        self.config_path = config_path or os.path.join(self.base_dir, "config.json")

        self.prompt_map = self._load_prompt_config()
        self.prompt_cache = self._load_all_prompts()

    def _load_prompt_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        return config.get("prompts", {})

    def _load_all_prompts(self):
        prompt_cache = {}
        for name, rel_path in self.prompt_map.items():
            full_path = os.path.join(self.prompt_dir, rel_path)
            with open(full_path, "r") as f:
                prompt_cache[name] = f.read()

        return prompt_cache

    def get_prompt(self, name) -> str:
        if name not in self.prompt_cache:
            raise ValueError(f"Prompt '{name}' not found in loaded cache.")
        return self.prompt_cache[name]
