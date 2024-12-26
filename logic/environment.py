import json
import os, sys


class Environment:
    user_conf = None

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def get_user_configuration_variable(key):
        if Environment.user_conf is None:
            Environment.load_configuration()
        return Environment.user_conf.get(key, None)

    @staticmethod
    def write_user_configuration_variable(key, value):
        if Environment.user_conf is None:
            Environment.load_configuration()
        Environment.user_conf[key] = value
        configuration_file_path = os.path.expanduser(r"~\AppData\Local\MaritimeFlagMaster\configuration.json")
        with open(configuration_file_path, "w") as file:
            json.dump(Environment.user_conf, file)

    @staticmethod
    def load_configuration():
        if not Environment.is_configuration_file_exists():
            Environment.create_configuration_file()
        configuration_file_path = os.path.expanduser(r"~\AppData\Local\MaritimeFlagMaster\configuration.json")
        with open(configuration_file_path, "r") as file:
            Environment.user_conf = json.load(file)

    @staticmethod
    def is_configuration_file_exists():
        configuration_file_path = os.path.expanduser(r"~\AppData\Local\MaritimeFlagMaster\configuration.json")
        return os.path.exists(configuration_file_path)

    @staticmethod
    def create_configuration_file():
        config_dir = os.path.expanduser(r"~\AppData\Local\MaritimeFlagMaster")
        config_file = os.path.expanduser(r"~\AppData\Local\MaritimeFlagMaster\configuration.json")
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, "w") as file:
            data = {}
            json.dump(data, file)
