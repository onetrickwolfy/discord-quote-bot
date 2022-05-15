from utils import *

from nextcord.ext import commands
from os import listdir, getenv
from yaml import safe_load
import logging
import cogs


# LOADING THE CONFIGURATION FILE
with open('config.yaml', 'r') as file:
    conf = safe_load(file)

logger = conf['logger']

token = getenv('discord-token') if getenv('discord-token') else conf['token']


# SETTING UP THE LOGGER
init_logger(logger)


# DISCORD BOT SET-UP
client = commands.Bot()

extentions = ['cogs.test']

[client.load_extension(extention) for extention in extentions]

client.run(token)
