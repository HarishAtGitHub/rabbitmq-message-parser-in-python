import logging
from logging.handlers import RotatingFileHandler

from config.configuration import *

MODE = 'a'
MAX_BYTES = 200000
BACKUP_COUNT = 10

def create_logger(name):
    # setup formatter
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    # setup handler
    handler = RotatingFileHandler(LOG_FILE, "a", MAX_BYTES, BACKUP_COUNT)
    handler.setFormatter(formatter)

    # add handler to logger
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)
    return logger

def getLogger():
    return logging.getLogger(LOGGER_NAME)