from yaml import safe_load
from os import path, makedirs

# -----------------------------------------------------


def get_config() -> None:
    """Return the configuration file as a dict."""

    with open('config.yaml', 'r') as file:
        return safe_load(file)


def create_if_missing(folder: str) -> None:
    """Create folder if non-existent"""

    if not path.exists(folder):
        makedirs(folder)
