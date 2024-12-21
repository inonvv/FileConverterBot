# from PIL import Image
# import cairosvg
# import svgwrite
# import os
# from src.file_converters.abstact_file_converter import FileConverter, LogType
# from src.files.files_enum import Extension
#
#
# class SvgPngConverter(FileConverter):
#     @staticmethod
#     def convert(file_path):
#         file_name = os.path.basename(file_path)
#         name, ext = os.path.splitext(file_name)
#         if ext == Extension.SVG.value:
#             SvgPngConverter.convert_svg_to_png(file_path)
#         elif ext == Extension.PNG.value:
#             SvgPngConverter.convert_png_to_svg(file_path)
#         else:
#             raise Exception(
#                 f"can only convert between {Extension.SVG.value} AND {Extension.PNG.value} ")
#
#     @staticmethod
#     def convert_svg_to_png(file_path):
#         try:
#             # Validate input file exists
#             if not os.path.exists(file_path):
#                 print(f"Error: File {file_path} does not exist.")
#                 return None
#
#             # Generate PNG filename (same directory, different extension)
#             png_path = os.path.splitext(file_path)[0] + '.png'
#
#             # Convert SVG to PNG
#             cairosvg.svg2png(url=file_path, write_to=png_path)
#
#             print(f"Successfully converted {file_path} to {png_path}")
#             return png_path
#
#         except IOError:
#             print(f"Cannot convert {file_path}")
#             return None
#         except Exception as e:
#             print(f"Unexpected error converting {file_path}: {e}")
#             return None
#
#     @staticmethod
#     def convert_png_to_svg(file_path):
#         try:
#             if not os.path.exists(file_path):
#                 print(f"Error: File {file_path} does not exist.")
#                 return None
#
#             # Convert PNG to black and white
#             with Image.open(file_path) as img:
#                 img = img.convert('L')  # Grayscale
#                 threshold = 128
#                 img = img.point(lambda x: 255 if x > threshold else 0, mode='1')  # Binarize
#                 bw_path = os.path.splitext(file_path)[0] + '_bw.png'
#                 img.save(bw_path)
#
#             # Generate SVG manually
#             svg_path = os.path.splitext(file_path)[0] + '.svg'
#             dwg = svgwrite.Drawing(svg_path, profile='tiny')
#             dwg.add(dwg.image(href=bw_path, insert=(0, 0)))
#             dwg.save()
#
#             print(f"Successfully converted {file_path} to {svg_path}")
#             return svg_path
#
#         except Exception as e:
#             print(f"Unexpected error converting {file_path}: {e}")
#             return None
