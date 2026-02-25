from pathlib import Path

import yaml


class Settings:
    def __init__(self):
        self.__config_file = Path(__file__).parent.parent / "config" / "config.yaml"
        # self.__config_file = Path("../config/config.yaml")  # NOOOOOOOOOOOOOOOO !
        self.__config = None

        with open(self.__config_file) as f:
            self.__config = yaml.safe_load(f)

    @property
    def user(self):
        return self.__config["user"]

    @property
    def password(self):
        return self.__config["pwd"]

s = Settings()

print(s.user)
