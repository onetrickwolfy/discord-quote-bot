"""Glue the app together."""


from modules import *
import logging


# Grabbing config
conf = get_config()
logger = conf['logger']


# Setting-up logger
init_logger(logger)
