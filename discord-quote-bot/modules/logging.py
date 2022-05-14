import logging
from os import path, makedirs


def create_logs_folder(log_folder):
    """Create log directory in case it does not exist."""

    if not path.exists(log_folder):
        makedirs(log_folder)


def init_logger(name, log_folder='logs', log_level=logging.DEBUG):
    """Set and return a logger."""

    create_logs_folder(log_folder)

    logger = logging.getLogger(name)

    logger.setLevel(log_level)

    files = logging.FileHandler(
        filename=f'{log_folder}/{name}.log',
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

    return logger
