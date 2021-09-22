import asyncio

from aiogram import Bot, Dispatcher

from .config import setup_args_parser, clear_env_vars
from .logger import setup_logger


async def main():
    args_parser = setup_args_parser()
    args = args_parser.parse_args()
    clear_env_vars()

    logger = setup_logger()

    bot = Bot(args.bot_token, parse_mode='HTML')
    dp = Dispatcher(bot)

    logger.info('starting bot')
    try:
        await dp.start_polling()
    finally:
        logger.info('stopping bot')
        await dp.storage.close()
        await dp.storage.wait_closed()
        await dp.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

