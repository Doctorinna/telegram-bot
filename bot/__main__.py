import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiohttp import ClientSession

from .api import QuestionnaireAPI
from .config import setup_args_parser, clear_env_vars
from .logger import setup_logger


async def main():
    args_parser = setup_args_parser()
    args = args_parser.parse_args()
    clear_env_vars()

    logger = setup_logger()

    bot = Bot(args.bot_token, parse_mode='HTML')
    storage = RedisStorage2(host=args.redis_ip,
                            port=args.redis_port,
                            db=args.redis_db)
    dp = Dispatcher(bot, storage=storage)

    questionnaire_api_session = ClientSession()
    questionnaire_api = QuestionnaireAPI(api_url=args.api_url,
                                         session=questionnaire_api_session)
    await questionnaire_api.retrieve_questionnaire()

    logger.info('starting bot')
    try:
        await dp.start_polling()
    finally:
        logger.info('stopping bot')
        await dp.storage.close()
        await dp.storage.wait_closed()
        await dp.bot.session.close()
        await questionnaire_api_session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

