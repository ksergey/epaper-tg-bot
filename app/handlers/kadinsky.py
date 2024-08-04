import logging

from io import BytesIO

from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command, CommandObject

from app.display import Display
from app.text2image import Text2Image

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command('kadinsky'))
async def handler_command_kadinsky(message: Message, command: CommandObject, text2image: Text2Image, display: Display):
    notification_message = await message.answer('\N{SLEEPING SYMBOL}...')
    try:
        prompt = command.args
        if not prompt:
            prompt = 'Огромные грибы, румянец, детальная прорисовка'
        images = await text2image.generate(prompt)
        for image in images:
            await message.reply_photo(BufferedInputFile(image, 'kadinsky.jpg'))

        await message.answer('Rendering on display')
        await display.render(BytesIO(images[0]))
        # image = convert(BytesIO(images[0]), (epd.width, epd.height))
        # epd.display(epd.getbuffer(image))
        await message.answer('Rendered')

    except Exception as ex:
        await message.reply(f'\N{Heavy Ballot X} error: {ex}')
        logger.exception(f'exception during process message {message}')
    finally:
        await notification_message.delete()
