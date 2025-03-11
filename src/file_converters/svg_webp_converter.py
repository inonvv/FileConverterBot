from PIL import Image
import cairosvg
import os
import subprocess
from src.file_converters.abstact_file_converter import FileConverter, LogType


class SvgWebpConverter(FileConverter):
    @staticmethod
    def convert(file_path):
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        if ext == ".svg":
            SvgWebpConverter.convert_svg_to_webp(file_path)
        elif ext == ".webp":
            SvgWebpConverter.convert_webp_to_svg(file_path)
        else:
            raise Exception("Can only convert between .svg and .webp")

    @staticmethod
    def convert_svg_to_webp(file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            webp_path = os.path.splitext(file_path)[0] + '.webp'
            cairosvg.svg2png(url=file_path, write_to="temp.png")

            with Image.open("temp.png") as img:
                img.save(webp_path, "WEBP")

            os.remove("temp.png")
            print(f"Successfully converted {file_path} to {webp_path}")
            return webp_path

        except Exception as e:
            print(f"Unexpected error converting SVG to WEBP: {e}")
            return None

    @staticmethod
    def convert_webp_to_svg(file_path):
        try:
            # Resolve absolute paths
            file_path = os.path.abspath(file_path)
            output_dir = os.path.dirname(file_path)
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            temp_pbm = os.path.join(output_dir, f"{base_name}_temp.pbm")
            svg_path = os.path.join(output_dir, f"{base_name}.svg")

            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Convert WEBP to 1-bit PBM (binary)
            with Image.open(file_path).convert('L') as img:  # Grayscale
                img = img.point(lambda x: 255 if x > 128 else 0).convert('1')  # Threshold to black/white
                img.save(temp_pbm, "PPM")  # Pillow uses "PPM" for binary PBM

            # Verify PBM file exists
            if not os.path.exists(temp_pbm):
                raise FileNotFoundError(f"Temp PBM file {temp_pbm} not created!")

            # Run Potrace (ensure it's in PATH or use absolute path)
            subprocess.run(
                ["potrace", temp_pbm, "-s", "-o", svg_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Cleanup
            os.remove(temp_pbm)
            print(f"Successfully converted to {svg_path}")
            return svg_path

        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def convert_webp_to_svg2(file_path):
        try:
            # 1. Check if file exists
            if not os.path.exists(file_path):
                FileConverter.get_logger().log(
                    LogType.ERROR,
                    FileConverter.build_log({
                        "message": f"File {file_path} does not exist."
                    })
                )
                return None

            # 2. Define .svg output path & a temp PPM path
            svg_path = os.path.splitext(file_path)[0] + '.svg'
            temp_pbm = os.path.splitext(file_path)[0] + '_temp.ppm'

            # 3. Convert the JPEG to a grayscale PPM for Potrace
            with Image.open(file_path).convert('L') as img:
                img.save(temp_pbm, "PPM")

            # 4. Run Potrace to trace that PPM into an SVG
            subprocess.run(
                ["potrace", temp_pbm, "-s", "-o", svg_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # 5. Clean up temp file
            if os.path.exists(temp_pbm):
                os.remove(temp_pbm)

            # 6. Log success
            FileConverter.get_logger().log(
                LogType.SUCCESS,
                FileConverter.build_log({
                    "message": f"Successfully converted {file_path} to {svg_path}."
                })
            )
            return svg_path

        except subprocess.CalledProcessError as e:
            # Potrace-specific errors
            FileConverter.get_logger().log(
                LogType.ERROR,
                FileConverter.build_log({
                    "message": f"Potrace error: {e.stderr.decode()}",
                    "file_path": file_path
                })
            )
            return None

        except Exception as e:
            # Unexpected errors
            FileConverter.get_logger().log(
                LogType.ERROR,
                FileConverter.build_log({
                    "message": f"Unexpected error converting WEBP to SVG: {e}",
                    "file_path": file_path
                })
            )
            return None

    @staticmethod
    def convert_webp_to_svg1(file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            svg_path = os.path.splitext(file_path)[0] + '.svg'

            with Image.open(file_path).convert('L') as img:
                img.save("temp_bw.webp")

            with open(svg_path, "w") as svg_file:
                svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg">'
                               f'<image href="temp_bw.webp" width="100%" height="100%" />'
                               f'</svg>')

            os.remove("temp_bw.webp")
            print(f"Successfully converted {file_path} to {svg_path}")
            return svg_path

        except Exception as e:
            print(f"Unexpected error converting WEBP to SVG: {e}")
            return None
