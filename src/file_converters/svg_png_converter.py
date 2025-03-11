from PIL import Image
import subprocess
import os
import svgwrite
import cv2
import cairosvg
from pathlib import Path
from src.file_converters.abstact_file_converter import FileConverter, LogType
from src.files.files_enum import Extension


# try:
# except ImportError:
#     cairosvg = None


class SvgPngConverter(FileConverter):
    @staticmethod
    def convert(file_path):
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        if ext == Extension.SVG.value:
            SvgPngConverter.convert_svg_to_png(file_path)
        elif ext == Extension.PNG.value:
            SvgPngConverter.convert_png_to_svg(file_path)
        else:
            raise Exception(
                f"can only convert between {Extension.SVG.value} AND {Extension.PNG.value}"
            )

    @staticmethod
    def convert_svg_to_png(file_path):
        if cairosvg is None:
            raise ImportError("cairosvg is not available. Ensure it's installed and properly configured.")

        try:
            # Validate input file exists
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            # Generate PNG filename (same directory, different extension)
            png_path = os.path.splitext(file_path)[0] + '.png'

            # Convert SVG to PNG
            cairosvg.svg2png(url=file_path, write_to=png_path)

            print(f"Successfully converted {file_path} to {png_path}")
            FileConverter.get_logger().log(LogType.SUCCESS, FileConverter.build_log(
                {"message": f"Successfully converted {file_path} to {png_path}"}))
            return png_path

        except Exception as e:
            print(f"Unexpected error converting SVG to PNG: {e}")
            return None

    @staticmethod
    def convert_png_to_svg(file_path):
        try:
            # 1. Absolute path check
            file_path = os.path.abspath(file_path)
            if not os.path.exists(file_path):
                FileConverter.get_logger().log(
                    LogType.ERROR,
                    FileConverter.build_log({"message": f"File {file_path} does not exist."})
                )
                return None

            # 2. Define .svg output path & temp PPM path
            stem = Path(file_path).stem
            output_dir = os.path.dirname(file_path)
            svg_path = os.path.join(output_dir, f"{stem}.svg")
            temp_ppm = os.path.join(output_dir, f"{stem}_temp.ppm")

            # 3. Convert the PNG to grayscale PPM for Potrace
            with Image.open(file_path).convert('L') as img:
                img.save(temp_ppm, "PPM")

            # 4. Run Potrace to convert PPM → SVG
            subprocess.run(
                ["potrace", temp_ppm, "-s", "-o", svg_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # 5. Remove temp file
            if os.path.exists(temp_ppm):
                os.remove(temp_ppm)

            # 6. Log success
            FileConverter.get_logger().log(
                LogType.SUCCESS,
                FileConverter.build_log({"message": f"Successfully converted {file_path} to {svg_path}."})
            )
            return svg_path

        except subprocess.CalledProcessError as e:
            # Potrace error
            FileConverter.get_logger().log(
                LogType.ERROR,
                FileConverter.build_log({"message": f"Potrace error: {e.stderr.decode()}", "file_path": file_path})
            )
            return None

        except Exception as e:
            # Any other error
            FileConverter.get_logger().log(
                LogType.ERROR,
                FileConverter.build_log({"message": f"Unexpected error: {e}", "file_path": file_path})
            )
            return None

    @staticmethod
    def convert_png_to_svg1(file_path):
        try:
            # Validate input file exists
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                FileConverter.get_logger().log(LogType.ERROR, FileConverter.build_log(
                    {"message": f"File {file_path} does not exist."}
                ))
                return None

            # Load the PNG image
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError(f"Failed to read {file_path} as an image.")

            # Binarize the image (Thresholding)
            _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

            # Find contours
            contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Generate SVG file path
            svg_path = os.path.splitext(file_path)[0] + '.svg'

            # Create SVG canvas
            height, width = img.shape
            dwg = svgwrite.Drawing(svg_path, size=(width, height), profile='tiny')

            # Add contours as paths to the SVG
            for contour in contours:
                # Convert contour points to path data
                path_data = "M " + " ".join([f"{point[0][0]},{point[0][1]}" for point in contour]) + " Z"
                dwg.add(dwg.path(d=path_data, fill="black", stroke="none"))

            # Save the SVG file
            dwg.save()

            # Log success
            print(f"Successfully converted {file_path} to {svg_path}")
            FileConverter.get_logger().log(LogType.SUCCESS, FileConverter.build_log(
                {"message": f"Successfully converted {file_path} to {svg_path}"}
            ))
            return svg_path

        except Exception as e:
            # Log unexpected errors
            print(f"Unexpected error converting PNG to SVG: {e}")
            FileConverter.get_logger().log(LogType.ERROR, FileConverter.build_log(
                {"message": f"Unexpected error converting PNG to SVG: {e}"}
            ))
            return None
