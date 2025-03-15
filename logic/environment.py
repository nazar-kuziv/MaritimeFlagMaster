import json
import os
import sys

from appdirs import user_data_dir

CONFIGURATION_DIR = user_data_dir("MaritimeFlagMaster", "NoName")
CONFIGURATION_FILE_PATH = os.path.join(CONFIGURATION_DIR, "configuration.json")


class Environment:
    user_conf = None

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def get_user_configuration_variable(key):
        if Environment.user_conf is None:
            Environment._load_configuration()
        return Environment.user_conf.get(key, None)

    @staticmethod
    def write_user_configuration_variable(key, value):
        if Environment.user_conf is None:
            Environment._load_configuration()
        Environment.user_conf[key] = value
        with open(CONFIGURATION_FILE_PATH, "w") as file:
            json.dump(Environment.user_conf, file)

    @staticmethod
    def _load_configuration():
        if not Environment._is_configuration_file_exists():
            Environment._create_configuration_file()
        with open(CONFIGURATION_FILE_PATH, "r") as file:
            Environment.user_conf = json.load(file)

    @staticmethod
    def _is_configuration_file_exists():
        return os.path.exists(CONFIGURATION_FILE_PATH)

    @staticmethod
    def _create_configuration_file():
        os.makedirs(CONFIGURATION_DIR, exist_ok=True)
        with open(CONFIGURATION_FILE_PATH, "w") as file:
            data = {}
            json.dump(data, file)
