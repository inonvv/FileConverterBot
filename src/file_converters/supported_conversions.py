from src.files.files_enum import Extension
from src.file_converters.png_jpeg_converter import PngJpegConverter
from src.file_converters.svg_png_converter import SvgPngConverter
from src.file_converters.webp_png_converter import WebpPngConverter
from src.file_converters.webp_jpeg_converter import WebpJpegConverter
from src.file_converters.svg_jpeg_converter import SvgJpegConverter
from src.file_converters.svg_webp_converter import SvgWebpConverter

supported_conversions = {
    Extension.PNG.value: {
        Extension.JPEG.value: PngJpegConverter,
        # Extension.JPG.value: PngJpegConverter,
        Extension.SVG.value: SvgPngConverter,
        Extension.WEBP.value: WebpPngConverter,

    },
    Extension.JPEG.value: {
        Extension.PNG.value: PngJpegConverter,
        Extension.SVG.value: SvgJpegConverter,
        Extension.WEBP.value: WebpJpegConverter
    },
    Extension.JPG.value: {
        Extension.PNG.value: PngJpegConverter,
        Extension.SVG.value: SvgJpegConverter,
        Extension.WEBP.value: WebpJpegConverter

    },
    Extension.SVG.value: {
        Extension.PNG.value: SvgPngConverter,
        Extension.JPEG.value: SvgJpegConverter,
        # Extension.JPG.value: SvgJpegConverter
        Extension.WEBP.value: SvgWebpConverter
    },
    Extension.WEBP.value: {
        Extension.PNG.value: WebpPngConverter,
        Extension.JPEG.value: WebpJpegConverter,
        Extension.SVG.value: SvgWebpConverter

    }

}
