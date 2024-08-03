import logging

from aiogram import Router, F, Bot
from aiogram.types import Message

from app.convert import convert

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot, epd):
    photo = message.photo[-1]
    logger.info(f'file_id={photo.file_id}, {photo.width}x{photo.height}')
    await message.answer('Rendering on display')
    image = convert(await bot.download(photo), (epd.width, epd.height))
    epd.display(epd.getbuffer(image))
    await message.answer('Rendered')
