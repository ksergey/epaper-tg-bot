from typing import List

from aiogram import Router
from aiogram.types import Message, BotCommand
from aiogram.filters import Command

commands = [
    BotCommand(command='help', description='show help'),
]

router = Router()

@router.message(Command('help'))
async def handler_command_help(message: Message):
    help_message = ''.join(
        f'/{command.command} - {command.description}\n' for command in commands
    )
    await message.answer(help_message)

def setup_router() -> Router:
    main_router = Router()

    return main_router

def setup_commands() -> List[BotCommand]:
    return commands
