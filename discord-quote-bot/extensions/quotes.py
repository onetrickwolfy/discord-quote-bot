from secrets import token_hex
import hikari
import lightbulb
from tinydb import Query
from utils import build_image
from urllib.parse import urlparse
from io import BytesIO
import asyncio
from .errors_handling import CharacterLimitException
from .errors_handling import NoChannelAttributed
from .errors_handling import MissingParameterException
from utils import guilds_settings
import concurrent.futures


import typing

plugin = lightbulb.Plugin("Quote-Maker")


# -----------------------------------------------------


async def handle_response(
    ctx: lightbulb.Context,
    username: typing.Union[hikari.Member, str],
    quote: str,
    pfp=None
) -> None:

    if not quote:
        raise MissingParameterException('Quote')
    if len(quote) > 420:
        raise CharacterLimitException(420)

    guild = Query()
    param = guilds_settings.search(guild.guild_id == ctx.guild_id)[0]

    if not param.get('global') and not param.get('hall_of_fame'):
        raise NoChannelAttributed

    if pfp:
        avatar = BytesIO()
        async with pfp.stream() as stream:
            async for chunk in stream:
                avatar.write(chunk)
    else:
        avatar = 'assets/default.png'

    loop = ctx.bot.d.loop
    result = await loop.run_in_executor(ctx.bot.d.process_pool, build_image, username, quote, avatar)

    if channel_id := param.get('hall_of_fame'):
        await ctx.bot.rest.create_message(
            channel_id,
            f'A new quote was submitted by {ctx.author.mention}',
            attachment=result
        )

    if param.get('global'):
        await ctx.respond('Here is your quote!', attachment=result)
    else:
        channel = ctx.get_guild().get_channel(channel_id).mention
        await ctx.respond(f'You quote was sent straight to {channel}', reply=False)


# -----------------------------------------------------


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(
    "quote_this",
    "Click to quote this message.",
    auto_defer=True
)
@lightbulb.implements(lightbulb.MessageCommand)
async def quote_this_cmd(
    ctx: lightbulb.Context
) -> None:

    target = ctx.options.target
    avatar = target.author.avatar_url
    username = f"{target.author.username}#{target.author.discriminator}"
    quote = target.content

    await handle_response(ctx, username, quote, avatar)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'author',
    'The author of the quote',
    hikari.Member,
    required=True
)
@lightbulb.option(
    'quote',
    'The text you would like to quote',
    required=True
)
@lightbulb.command(
    "quote_user",
    "Generates a quote when invoked.",
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_user_cmd(
    ctx: lightbulb.Context,
    quote,
    author
) -> None:

    username = f"{author.username}#{author.discriminator}"
    avatar = author.avatar_url

    await handle_response(ctx, username, quote, avatar)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'quote',
    'The text you would like to quote',
    required=True
)
@lightbulb.command(
    "quote_me",
    "Generates a quote when invoked.",
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_me_cmd(
    ctx: lightbulb.Context,
    quote: str
) -> None:

    author = ctx.author
    username = f"{author.username}#{author.discriminator}"
    avatar = ctx.author.avatar_url

    await handle_response(ctx, username, quote, avatar)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'quote',
    'The text you would like to quote',
    required=True
)
@lightbulb.option(
    'author',
    'The author of the quote',
    default='anonymous-wolf'
)
@lightbulb.command(
    "quote_anon",
    "Generates a quote when invoked.",
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_anon_cmd(
    ctx: lightbulb.Context,
    quote: str, author:
        typing.Optional[str] = None
) -> None:

    await handle_response(ctx, author, quote)


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
