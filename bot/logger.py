import logging


def setup_logger() -> logging.Logger:
    logger = logging.getLogger('bot')
    logger.setLevel(logging.INFO)

    logging_file_handler = logging.FileHandler('bot.log', mode='a')
    logging_file_handler.setLevel(logging.INFO)

    logging_stream_handler = logging.StreamHandler()
    logging_stream_handler.setLevel(logging.WARNING)

    logger_formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'
    )

    logging_file_handler.setFormatter(logger_formatter)
    logging_stream_handler.setFormatter(logger_formatter)

    logger.addHandler(logging_file_handler)
    logger.addHandler(logging_stream_handler)
    return logger
