from utils import *
import logging

from os import listdir, getenv, name
import hikari
from hikari import Intents
import lightbulb
from yaml import safe_load


# LOADING THE CONFIGURATION FILE
# -----------------------------------------------------
with open('config.yaml', 'r') as file:
    conf = safe_load(file)

logger = conf['logger']

token = getenv('discord-token') or conf['token']


# SETTING UP THE LOGGER
# -----------------------------------------------------
init_logger(logger)


# SETTING UP THE DISCORD BOT
# -----------------------------------------------------
default_enabled_guilds = (964818125503750174)

bot = lightbulb.BotApp(
    token=token,
    intents=Intents.ALL,
    delete_unbound_commands=True,
    default_enabled_guilds=default_enabled_guilds,
    logs="WARNING",
)

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
