import logging
from os import path, makedirs
from time import time, strftime, gmtime
from utils import create_if_missing


# -----------------------------------------------------


def init_logger(logger_conf: dict) -> None:
    """Initialise the logging system."""

    log_folder = logger_conf['folder']
    name = logger_conf['name']
    log_level = logger_conf['log_level']

    create_if_missing(log_folder)

    logger = logging.getLogger()

    logger.setLevel(log_level)

    run_time = strftime("%d_%b_%Y.%Hh%M", gmtime(time()))
    files = logging.FileHandler(
        filename=f'{log_folder}/{name}_{run_time}.log',
        encoding='utf-8',
        mode='w'
    )

    files.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    )

    logger.addHandler(files)

    console = logging.StreamHandler()

    console.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    )

    logger.addHandler(console)
