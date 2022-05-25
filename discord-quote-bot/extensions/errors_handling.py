import hikari
import lightbulb
import logging


plugin = lightbulb.Plugin("Error-Handing")

# -----------------------------------------------------


class CharacterLimitException(lightbulb.LightbulbError):
    """Raised when a character limit has been reached"""

    def __init__(self, limit):
        super().__init__()
        self.limit = limit


class NoChannelAttributed(lightbulb.LightbulbError):
    """The bot cannot process the quote as it won't be transmited in any channel"""


class MissingParameterException(lightbulb.LightbulbError):
    """A parametter is missing"""

    def __init__(self, *parameters):
        super().__init__()
        self.parameters = [*parameters]

    @property
    def parameter_string(self):
        list = ''
        for param in self.parameters:
            list += ', ' + param
        return list[2:]


# -----------------------------------------------------


@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:

    errors = [
        lightbulb.CommandInvocationError,
        lightbulb.MessageCommandErrorEvent,
        lightbulb.UserCommandErrorEvent
    ]

    if any([isinstance(event.exception, error) for error in errors]):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.", delete_after=10)
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond(f"You are not the owner of this bot.", reply=True, delete_after=5)
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.", reply=True, delete_after=5)
    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(f"You need the {exception.missing_perms} permission in order to run this command.", reply=True, delete_after=5)
    elif isinstance(exception, CharacterLimitException):
        await event.context.respond(f'This quote is way too long! It has to be inferior to {exception.limit} characters.', reply=True, delete_after=5)
    elif isinstance(exception, NoChannelAttributed):
        await event.context.respond(f'The bot could not respond in any channel. Check your settings: /settings', reply=True, delete_after=5)
    elif isinstance(exception, MissingParameterException):
        await event.context.respond(f'One or more parameters are missing: {exception.parameter_string}', reply=True, delete_after=5)
    else:
        logging.warning(exception)


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
