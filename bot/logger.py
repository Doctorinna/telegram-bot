import logging


def setup_logger() -> logging.Logger:
    logger = logging.getLogger('bot')
    logger.setLevel(logging.INFO)

    logger_handler = logging.FileHandler('bot.log', mode='a')
    logger_handler.setLevel(logging.INFO)

    logger_formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s')

    logger_handler.setFormatter(logger_formatter)

    logger.addHandler(logger_handler)
    return logger
