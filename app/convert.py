import math
import logging

from PIL import Image, ImageEnhance
from io import BytesIO

logger = logging.getLogger(__name__)

# TODO: причесать

def convert(data: BytesIO, outputSize: tuple[int, int]):
    image = Image.open(data)

    outputWidth, outputHeight = outputSize
    if image.width > image.height:
        height = int(image.height * (outputWidth / image.width))
        width = outputWidth
    else:
        height = outputHeight
        width = int(image.width * (outputHeight / image.height))

    image.thumbnail((width, height), Image.Resampling.LANCZOS)

    left = int((width - outputWidth) / 2)
    top = int((height - outputHeight) / 2)
    right = left + outputWidth
    bottom = top + outputHeight

    image = image.crop((left, top, right, bottom))

    palettedata = [
        0x00, 0x00, 0x00,
        0xff, 0xff, 0xff,
        0x00, 0xff, 0x00,
        0x00, 0x00, 0xff,
        0xff, 0x00, 0x00,
        0xff, 0xff, 0x00,
        0xff, 0x80, 0x00,
    ]

    for i in range(0, 249 * 3):
        palettedata.append(0)

    p_img = Image.new('P', outputSize)
    p_img.putpalette(palettedata)

    return image.quantize(palette=p_img, dither=1)
