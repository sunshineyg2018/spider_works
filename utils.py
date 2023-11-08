import configparser
import os
import logging


class DisposeIni:
    def __init__(self, filepath="local_config.ini"):
        config_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(config_path, filepath)
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')

    def get_items(self, sec):
        return self.config.items(sec)


def init_log():
    logger = logging.getLogger()
    file_handler = logging.FileHandler('log.txt')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
