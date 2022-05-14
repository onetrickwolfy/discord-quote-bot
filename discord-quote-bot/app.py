"""Glue the app together."""


from utils import *
from yaml import safe_load
import logging


# Grabbing config
with open('config.yaml', 'r') as file:
    conf =  safe_load(file)
logger = conf['logger']


# Setting-up logger
init_logger(logger)
