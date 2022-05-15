from utils import *
import logging

from os import listdir, getenv, name
import hikari
import lightbulb
from yaml import safe_load


# LOADING THE CONFIGURATION FILE
with open('config.yaml', 'r') as file:
    conf = safe_load(file)

logger = conf['logger']

token = getenv('discord-token') or conf['token']


# SETTING UP THE LOGGER
init_logger(logger)


# SETTING UP THE DISCORD BOT
token = getenv('discord-token') or conf['token']

default_enabled_guilds = (964818125503750174)

bot = lightbulb.BotApp(token=token, prefix=">")

bot.load_extensions_from("./extensions/", must_exist=True)

if __name__ == "__main__":
    if name != "nt":
        import uvloop
        uvloop.install()
        
bot.run(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(
        name="all of you, cuties!",
        type=hikari.ActivityType.LISTENING
    )
)