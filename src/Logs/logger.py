import os
import json
from datetime import datetime
from src.Logs.log_types_enum import LogType


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.root_folder_path = r"C:\Users\inon\working-projects\logs"

    def set_folder_path(self, root_folder_path):
        self.root_folder_path = root_folder_path

    def log(self, log_type, log_data):
        full_path = self.root_folder_path
        #         rearange in months
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        full_file_name = ""
        current_date = datetime.now()
        full_file_name += current_date.strftime("%Y-%m-%d-%H-%M-%S.%f")[:-3]
        full_file_name += "_"
        full_file_name += log_type.value
        full_file_name += ".json"
        og_full_path = os.path.join(full_path, full_file_name)
        with open(og_full_path, 'w', encoding='utf-8') as file:
            json.dump(log_data, file, ensure_ascii=False, indent=4)

    def log_error(self, data):
        self.log(LogType.ERROR, data)

    def log_success(self, data):
        self.log(LogType.SUCCESS, data)

    def log_info(self, data):
        self.log(LogType.INFO, data)
