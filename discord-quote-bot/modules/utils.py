"""Provide a few utilities"""

from yaml import safe_load


def get_config():
    """Return the configuration as a dictionary."""

    with open('config.yaml', 'r') as file:
        return safe_load(file)
