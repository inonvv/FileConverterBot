import os.path

from src.files.abstract_file import File


class SvgFile(File):

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_name, self.extension = os.path.splitext(self.file_name)

    def extension(self):
        return self.extension

    def name(self):
        pass
