from typing import List

from aiogram import Router
from aiogram.types import Message, BotCommand
from aiogram.filters import Command

commands = [
    BotCommand(command='kadinsky', description='kadinsky text2image'),
    BotCommand(command='help', description='show help')
]

router = Router()

@router.message(Command('help'))
async def handler_command_help(message: Message):
    help_message = 'commands:\n'
    help_message += ''.join(
        f'/{command.command} - {command.description}\n' for command in commands
    )
    help_message += '\n'
    help_message += 'send an image to render it on display\n'

    await message.answer(help_message)

def setup_router() -> Router:
    from . import kadinsky, photo

    main_router = Router()
    main_router.include_router(kadinsky.router)
    main_router.include_router(photo.router)
    main_router.include_router(router)

    return main_router

def setup_commands() -> List[BotCommand]:
    return commands
