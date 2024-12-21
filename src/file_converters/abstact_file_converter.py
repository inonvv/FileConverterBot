from abc import ABC, abstractmethod
from src.Logs.logger import Logger
from src.Logs.log_types_enum import LogType


class FileConverter(ABC):
    @staticmethod
    @abstractmethod
    def convert(file_path):
        pass

    @staticmethod
    def get_logger():
        logger = Logger()
        return logger

    @staticmethod
    def build_log(data):
        note = "here will be a logs using dictionary inside the abstract file converter"
        data["note"] = note
        return data
