import configparser
import os


class DisposeIni:
    def __init__(self, filepath="local_config.ini"):
        config_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(config_path,filepath)
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')

    def get_items(self, sec):
        return self.config.items(sec)

