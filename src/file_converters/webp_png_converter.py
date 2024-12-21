from PIL import Image
import os
from src.file_converters.abstact_file_converter import FileConverter, LogType
from src.files.files_enum import Extension


class WebpPngConverter(FileConverter):
    @staticmethod
    def convert(file_path):
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        if ext == Extension.WEBP.value:
            WebpPngConverter.convert_webp_to_png(file_path)
        elif ext == Extension.PNG.value:
            WebpPngConverter.convert_png_to_webp(file_path)
        else:
            raise Exception(
                f"can only convert between {Extension.WEBP.value} AND {Extension.PNG.value}"
            )

    @staticmethod
    def convert_webp_to_png(file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            with Image.open(file_path) as img:
                png_path = os.path.splitext(file_path)[0] + '.png'
                img.save(png_path, "PNG")
                print(f"Successfully converted {file_path} to {png_path}")
                return png_path

        except Exception as e:
            print(f"Unexpected error converting {file_path} to PNG: {e}")
            return None

    @staticmethod
    def convert_png_to_webp(file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            with Image.open(file_path) as img:
                webp_path = os.path.splitext(file_path)[0] + '.webp'
                img.save(webp_path, "WEBP")
                print(f"Successfully converted {file_path} to {webp_path}")
                return webp_path

        except Exception as e:
            print(f"Unexpected error converting {file_path} to WebP: {e}")
            return None
