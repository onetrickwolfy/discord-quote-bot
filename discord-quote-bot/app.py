from utils import *
import logging
from os import listdir, getenv, name as os_name
import hikari
from hikari import Intents
import lightbulb
from utils import get_config
from utils import guilds_settings
from tinydb import Query


# LOADING THE CONFIGURATION FILE
# -----------------------------------------------------
conf = get_config()

logger = conf['logger']

token = getenv('discord-token') or conf['token']


# SETTING UP LOGGING
# -----------------------------------------------------
init_logger(logger)

# SETTING UP THE DISCORD BOT
# -----------------------------------------------------
default_enabled_guilds = (964818125503750174)

bot = lightbulb.BotApp(
    token=token,
    prefix='>',
    intents=Intents.ALL,
    delete_unbound_commands=True,
    default_enabled_guilds=default_enabled_guilds
)

bot.load_extensions_from("./extensions/", must_exist=True)


@bot.listen()
async def on_guild_join(event: hikari.GuildJoinEvent) -> None:
    guilds_settings.upsert(
        {
            'guild_id': event.guild_id,
            'global': True,
            'hall_of_fame': None
        },
        Query().guild_id == event.guild_id
    )


@bot.listen()
async def on_guild_leave(event: hikari.GuildLeaveEvent) -> None:
    guilds_settings.remove(Query().guild_id == event.guild_id)


if __name__ == "__main__":
    if os_name != "nt":
        import uvloop  # type: ignore (uvloop does not exist on windows.)
        uvloop.install()

bot.run(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(
        name="all of you, cuties!",
        type=hikari.ActivityType.LISTENING
    )
)
