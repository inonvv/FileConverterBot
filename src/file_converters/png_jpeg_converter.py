from PIL import Image
import os
from src.file_converters.abstact_file_converter import FileConverter, LogType
from src.files.files_enum import Extension


class PngJpegConverter(FileConverter):
    @staticmethod
    def convert(file_path):
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        if ext == Extension.JPEG.value or ext == Extension.JPG.value:
            PngJpegConverter.convert_jpeg_to_png(file_path)
        elif ext == Extension.PNG.value:
            PngJpegConverter.convert_png_to_jpeg(file_path)
        else:
            raise Exception(
                f"can only convert between {Extension.PNG.value} AND {Extension.JPEG.value}/{Extension.JPG.value} ")

    @staticmethod
    def convert_png_to_jpeg(file_path):
        try:
            # Validate input file exists and is JPEG
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            # Open the png image
            with Image.open(file_path) as img:
                # Generate PNG filename (same directory, different extension)
                jpeg_path = os.path.splitext(file_path)[0] + '.jpeg'

                # Convert and save image
                img.save(jpeg_path, 'JPEG')

                print(f"Successfully converted {file_path} to {jpeg_path}")
                return jpeg_path

        except IOError:
            print(f"Cannot convert {file_path}")
            return None
        except Exception as e:
            print(f"Unexpected error converting {file_path}: {e}")
            return None

    @staticmethod
    def convert_jpeg_to_png(file_path):
        try:
            # Validate input file exists and is JPEG
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            # Open the JPEG image
            with Image.open(file_path) as img:
                # Generate PNG filename (same directory, different extension)
                png_path = os.path.splitext(file_path)[0] + '.png'

                # Convert and save image
                img.save(png_path, 'PNG')

                print(f"Successfully converted {file_path} to {png_path}")
                FileConverter.get_logger().log(LogType.INFO,
                                               FileConverter.build_log(
                                                   {"message": f"Successfully converted {file_path} to {png_path}"}))
                return png_path

        except IOError:
            print(f"Cannot convert {file_path}")
            FileConverter.get_logger().log(LogType.ERROR,
                                           {"message": f"Cannot convert {file_path}", "ERROR_TYPE": "IOError"})
            return None
        except Exception as e:
            print(f"Unexpected error converting {file_path}: {e}")
            FileConverter.get_logger().log(LogType.ERROR, {"message": f"Unexpected error converting {file_path}: {e}"})
            return None
