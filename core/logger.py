# core/logger.py
import logging
from core.config import config

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(config.LOG_LEVEL)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
