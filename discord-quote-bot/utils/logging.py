import logging
from os import path, makedirs


# -----------------------------------------------------


def create_if_missing(folder: str) -> None:
    """Create folder if non-existent"""

    if not path.exists(folder):
        makedirs(folder)


def init_logger(logger_conf: dict) -> None:
    """Initialise the logging system."""

    log_folder = logger_conf['folder']
    name = logger_conf['name']
    log_level = logger_conf['log_level']

    create_if_missing(log_folder)

    logger = logging.getLogger()

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
