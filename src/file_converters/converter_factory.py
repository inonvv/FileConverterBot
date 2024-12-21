import os.path
from src.files.files_factory import FileFactory
from src.file_converters.supported_conversions import supported_conversions


class ConverterFactory:
    @staticmethod
    def convert_file(file_path, targetExtension):
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        converter_class = supported_conversions[ext][targetExtension]

        new_file = FileFactory.create_file(file_path)

        converter_class.convert(new_file.file_path)
