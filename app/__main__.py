import logging
import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.types import ReplyKeyboardRemove, BufferedInputFile, BotCommandScopeChat
from aiogram.enums import ParseMode

from app.args_reader import args
from app.config_reader import config
from app.handlers import setup_router, setup_commands
from app.text2image import Text2Image
from app.display import Display

logging.basicConfig(
    filename=args.logfile,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=args.loglevel
)

logger = logging.getLogger(__name__)

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_my_commands(commands=setup_commands(), scope=BotCommandScopeChat(chat_id=config.telegram.chat_id))
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.send_message(
    #     config.telegram.chat_id,
    #     f'\N{Black Right-Pointing Pointer} <i>bot going online</i>', reply_markup=ReplyKeyboardRemove()
    # )

async def on_shutdown(dispatcher: Dispatcher, bot: Bot, text2image: Text2Image):
    # await bot.send_message(config.telegram.chat_id, f'\N{Black Left-Pointing Pointer} <i>bot going offline</i>')
    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=config.telegram.chat_id))
    await text2image.close()

async def main():
    logger.info(f'config:\n{config}')

    text2image = Text2Image(
        api_key=config.kadinsky.key,
        secret_key=config.kadinsky.secret
    )

    # TODO: configure?
    display = Display('epd5in65f')

    # accept messages only from configured chat id
    router = setup_router()
    if type(config.telegram.chat_id) == list:
        router.message.filter(F.chat.id.in_(config.telegram.chat_id))
    else:
        router.message.filter(F.chat.id == config.telegram.chat_id)

    # pass kadinsky to dispatcher constructor
    # now "kadinsky: Kadinsky" could be arg for a handler
    dp = Dispatcher(text2image=text2image, display=display)
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(token=config.telegram.token, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('bot stopped!')
