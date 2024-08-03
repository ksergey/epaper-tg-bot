import logging

from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command, CommandObject

from PIL import Image, ImageEnhance
from io import BytesIO

from app.text2image import Text2Image

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command('kadinsky'))
async def handler_command_kadinsky(message: Message, command: CommandObject, text2image: Text2Image):
    notification_message = await message.answer('\N{SLEEPING SYMBOL}...')
    try:
        prompt = command.args
        if not prompt:
            prompt = 'Огромные грибы, румянец, детальная прорисовка'
        images = await text2image.generate(prompt)
        for image in images:
            await message.reply_photo(BufferedInputFile(image, 'kadinsky.jpg'))

    except Exception as ex:
        await message.reply(f'\N{Heavy Ballot X} error: {ex}')
        logger.exception(f'exception during process message {message}')
    finally:
        await notification_message.delete()
