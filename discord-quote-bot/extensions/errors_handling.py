import asyncio
from time import sleep
import hikari
import lightbulb
import logging


plugin = lightbulb.Plugin("Error-Handing")


# -----------------------------------------------------


@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:

    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.", delete_after=10)
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception


    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You are not the owner of this bot.", reply=True, delete_after=5)
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.", reply=True, delete_after=5)
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(f"You need to be an administrator in order to run this command.", reply=True, delete_after=5)
    else:
        logging.warning(exception)


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
