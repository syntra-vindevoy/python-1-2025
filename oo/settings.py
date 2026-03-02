from pathlib import Path
import yaml

class Settings:
    def __init__(self):
        self.__config_file = Path(__file__).parent / 'config.yaml'

# NOT FINISHED
