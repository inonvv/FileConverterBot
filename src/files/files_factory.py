import os.path
from .files_enum import Extension
from .images.jpeg_file import JpegFile
from .images.png_file import PngFile
from .images.webp_file import WebpFile
from src.files.images.svg_file import SvgFile
from src.Logs.logger import Logger, LogType


class FileFactory:
    @staticmethod
    def create_file(file_path):
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        if ext == Extension.PNG.value:
            return PngFile(file_path)

        elif ext == Extension.JPEG.value or ext == Extension.JPG.value:
            return JpegFile(file_path)
        elif ext == Extension.WEBP.value:
            return WebpFile(file_path)
        elif ext == Extension.SVG.value:
            return SvgFile(file_path)
        else:
            logger = Logger()
            logger.log(LogType.ERROR, {"message": "extension is not supported yet in files", "extension": ext})
