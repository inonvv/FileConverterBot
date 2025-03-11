from PIL import Image
import cairosvg
import os
import subprocess
from src.file_converters.abstact_file_converter import FileConverter, LogType


class SvgJpegConverter(FileConverter):
    @staticmethod
    def convert(file_path):
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)
        if ext == ".svg":
            SvgJpegConverter.convert_svg_to_jpeg(file_path)
        elif ext == ".jpeg" or ext == ".jpg":
            SvgJpegConverter.convert_jpeg_to_svg(file_path)
        else:
            raise Exception("Can only convert between .svg and .jpeg/.jpg")

    @staticmethod
    def convert_svg_to_jpeg(file_path):
        if cairosvg is None:
            raise ImportError("cairosvg is not available. Ensure it's installed and properly configured.")

        try:
            # Validate input file exists
            if not os.path.exists(file_path):
                FileConverter.get_logger().log(LogType.ERROR, FileConverter.build_log({
                    "message": f"File {file_path} does not exist."
                }))
                return None

            # Generate temporary PNG filename and final JPEG filename
            temp_png_path = os.path.splitext(file_path)[0] + '_temp.png'
            jpeg_path = os.path.splitext(file_path)[0] + '.jpeg'

            # Log start of conversion
            FileConverter.get_logger().log(LogType.INFO, FileConverter.build_log({
                "message": f"Starting conversion from SVG to JPEG for {file_path}."
            }))

            # Convert SVG to temporary PNG using cairosvg
            cairosvg.svg2png(url=file_path, write_to=temp_png_path)

            # Validate the created temporary PNG file
            if not os.path.exists(temp_png_path):
                FileConverter.get_logger().log(LogType.ERROR, FileConverter.build_log({
                    "message": f"Temporary PNG file {temp_png_path} not created during conversion."
                }))
                return None

            # Open the PNG and convert it to JPEG, handling transparency
            with Image.open(temp_png_path) as img:
                # Create a white background for transparency
                if img.mode == "RGBA":
                    background = Image.new("RGB", img.size, (255, 255, 255))  # White background
                    background.paste(img, mask=img.split()[3])  # Apply alpha channel as mask
                    img = background

                # Save the final JPEG
                img.save(jpeg_path, "JPEG", quality=95)  # Save with high quality

            # Clean up the temporary PNG file
            if os.path.exists(temp_png_path):
                os.remove(temp_png_path)

            # Log success
            FileConverter.get_logger().log(LogType.SUCCESS, FileConverter.build_log({
                "message": f"Successfully converted {file_path} to {jpeg_path}."
            }))
            return jpeg_path

        except Exception as e:
            # Log any unexpected errors
            FileConverter.get_logger().log(LogType.ERROR, FileConverter.build_log({
                "message": f"Unexpected error converting SVG to JPEG: {e}",
                "file_path": file_path
            }))
            return None

    @staticmethod
    def convert_jpeg_to_svg(file_path):
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
            temp_ppm = os.path.splitext(file_path)[0] + '_temp.ppm'

            # 3. Convert the JPEG to a grayscale PPM for Potrace
            with Image.open(file_path).convert('L') as img:
                img.save(temp_ppm, "PPM")

            # 4. Run Potrace to trace that PPM into an SVG
            subprocess.run(
                ["potrace", temp_ppm, "-s", "-o", svg_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # 5. Clean up temp file
            if os.path.exists(temp_ppm):
                os.remove(temp_ppm)

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
                    "message": f"Unexpected error converting JPEG to SVG: {e}",
                    "file_path": file_path
                })
            )
            return None

    @staticmethod
    def convert_jpeg_to_svg1(file_path):
        try:
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} does not exist.")
                return None

            svg_path = os.path.splitext(file_path)[0] + '.svg'

            # Convert JPEG to grayscale for vector approximation
            with Image.open(file_path).convert('L') as img:
                img.save("temp_bw.jpeg")

            with open(svg_path, "w") as svg_file:
                svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg">'
                               f'<image href="temp_bw.jpeg" width="100%" height="100%" />'
                               f'</svg>')

            os.remove("temp_bw.jpeg")
            print(f"Successfully converted {file_path} to {svg_path}")
            return svg_path

        except Exception as e:
            print(f"Unexpected error converting JPEG to SVG: {e}")
            return None
