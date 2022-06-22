import logging
from settings import LOGGING_LEVEL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def info(msg):
    if LOGGING_LEVEL == 'VERBOSE':
        logging.info(msg)


def error(msg):
    if LOGGING_LEVEL in ['VERBOSE', 'ERRORS']:
        logging.error(msg)
