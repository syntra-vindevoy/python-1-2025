from pathlib import Path

import yaml


class Settings:
    settings: dict = {}

    def init(self):
        current_dir = Path(__file__).parent

        with open(current_dir / "settings.yaml", "r") as f:
            self.settings = yaml.safe_load(f)

    def get_user(self):
        return self.settings["user"]

    def get_password(self):
        return self.settings["password"]

settings = Settings()
settings.init()

print(settings.get_user())

