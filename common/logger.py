import logging
import sys

from common.config import LOGGER_FORMAT


def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(LOGGER_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
