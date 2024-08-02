import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from app.kadinsky import Kadinsky

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command('kadinsky'))
async def handler_command_kadinsky(message: Message, command: CommandObject, kadinsky: Kadinsky):
    notification_message = await message.answer('\N{SLEEPING SYMBOL}...')
    try:
        script = command.args or ''
        if script == '':
            raise RuntimeError('empty query')

    except Exception as ex:
        await message.reply(f'\N{Heavy Ballot X} error: {ex}')
        logger.exception(f'exception during process message {message}')
    finally:
        await notification_message.delete()
