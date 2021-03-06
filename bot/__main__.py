import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiohttp import ClientSession, ClientError

from .api import QuestionnaireAPI
from .bot.handlers import register_questionnaire_handlers
from .bot.keyboards import QuestionKeyboardMarkupFactory
from .bot.middlewares import DataMiddleware
from .config import setup_args_parser, clear_env_vars
from .logger import setup_logger


async def main():
    args_parser = setup_args_parser()
    args = args_parser.parse_args()
    clear_env_vars()

    logger = setup_logger()

    api_session = ClientSession()
    questionnaire_api = QuestionnaireAPI(api_url=args.api_url,
                                         session=api_session)
    try:
        await questionnaire_api.retrieve_questionnaire()
    except (ClientError, asyncio.TimeoutError) as err:
        logger.exception(err)
        await api_session.close()
        sys.exit(1)

    bot = Bot(args.bot_token, parse_mode='HTML')
    storage = RedisStorage2(host=args.redis_ip, port=args.redis_port,
                            db=args.redis_db)
    dp = Dispatcher(bot, storage=storage)

    question_keyboard_markup_factory = QuestionKeyboardMarkupFactory()
    data_middleware = DataMiddleware(questionnaire_api,
                                     question_keyboard_markup_factory)
    dp.setup_middleware(data_middleware)
    register_questionnaire_handlers(dp, question_keyboard_markup_factory)

    logger.info('starting bot')
    try:
        await dp.start_polling()
    finally:
        logger.info('stopping bot')
        await dp.storage.close()
        await dp.storage.wait_closed()
        await dp.bot.session.close()
        await api_session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
