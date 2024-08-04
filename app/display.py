import epaper
import logging
import asyncio

from PIL import Image, ImageEnhance
from io import BytesIO

logger = logging.getLogger(__name__)

class Display:
    def __init__(self, model: str):
        self._epd = epaper.epaper(model).EPD()
        self._epd.init()

        self._render_task = None

    @property
    def width(self) -> int:
        return self._epd.width

    @property
    def height(self) -> int:
        return self._epd.height

    async def render(self, data: BytesIO) -> None:
        if self._render_task and not self._render_task.done():
            raise Exception('Display busy')

        if self._render_task:
            logger.info(f'render {self._render_task.done()}')

        def task():
            image = self._convert(data, (self.width, self.height))
            self._epd.display(self._epd.getbuffer(image))

        self._render_task = asyncio.create_task(asyncio.to_thread(task))
        await self._render_task

    async def cancel(self) -> None:
        if not self._render_task or self._render_task.done():
            return
        self._render_task.cancel()
        await self._render_task


    def _convert(self, data: BytesIO, outputSize: tuple[int, int]):
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
