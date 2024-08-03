import logging
import math

from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command, CommandObject

from PIL import Image, ImageEnhance
from io import BytesIO

from app.text2image import Text2Image

logger = logging.getLogger(__name__)
router = Router()

# TODO: причесать

def convert(image, outputSize = (600, 448)):
    width, height = image.size
    if width < height:
        image = image.rotate(90, expand=1)
    width, height = image.size

    outputWidth, outputHeight = outputSize
    ratio = width / outputWidth
    tmpHeight = height / ratio

    image = image.resize((outputWidth, math.floor(tmpHeight)))
    difference = tmpHeight - outputHeight
    partVal = abs(difference) / 2
    bot = math.ceil(partVal)
    top = math.floor(partVal)
    if difference > 0:
        image = image.crop((0, top, outputWidth, tmpHeight - top))
    else:
        tempImage = Image.new(image.mode, outputSize, (255, 255, 255))
        tempImage.paste(image, (0, top))
        image = tempImage

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

    p_img = Image.new('P', (600, 448))
    p_img.putpalette(palettedata)

    return image.quantize(palette=p_img, dither=1)


@router.message(Command('kadinsky'))
async def handler_command_kadinsky(message: Message, command: CommandObject, text2image: Text2Image, epd):
    notification_message = await message.answer('\N{SLEEPING SYMBOL}...')
    try:
        prompt = command.args
        if not prompt:
            prompt = 'Огромные грибы, румянец, детальная прорисовка'
        images = await text2image.generate(prompt)
        for image in images:
            await message.reply_photo(BufferedInputFile(image, 'kadinsky.jpg'))

        await message.answer('Rendering on dislay')
        pimg = convert(Image.open(BytesIO(images[0])), (epd.width, epd.height))
        epd.display(epd.getbuffer(pimg))
        await message.answer('Rendered')

    except Exception as ex:
        await message.reply(f'\N{Heavy Ballot X} error: {ex}')
        logger.exception(f'exception during process message {message}')
    finally:
        await notification_message.delete()
