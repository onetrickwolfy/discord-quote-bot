from secrets import token_hex
import hikari
import lightbulb
from tinydb import Query
from utils import build_image
from urllib.parse import urlparse
from io import BytesIO
import datetime
from .errors_handling import CharacterLimitException
from .errors_handling import NoChannelAttributed
from .errors_handling import MissingParameterException
from utils import guilds_settings
import typing


plugin = lightbulb.Plugin("Quote-Maker")
plugin.add_checks(lightbulb.guild_only)


# -----------------------------------------------------


def veriy_field(quote: str, username: str) -> None:
    """Make sure the field have appropriate lengh"""

    if not quote:
        raise MissingParameterException('quote')

    if len(quote) > 420:
        raise CharacterLimitException(420, 'quote')

    if len(username) > 38:
        raise CharacterLimitException(38, 'username')


def get_parameters_and_check_availibity(
    ctx: lightbulb.context
) -> typing.Union[None, typing.Tuple]:
    """
    Ensure there's a channel to send the response in.
    Return the global parameter, and the hall of fame id.
    """

    guild = Query()
    param = guilds_settings.search(guild.guild_id == ctx.guild_id)[0]

    if not param.get('global') and not param.get('hall_of_fame'):
        raise NoChannelAttributed

    return param.get('global'), param.get('hall_of_fame')


async def handle_response_image(
    ctx: lightbulb.Context,
    username: typing.Union[hikari.Member, str],
    quote: str,
    pfp=None
) -> None:

    veriy_field(quote, username)

    global_response, channel_id = get_parameters_and_check_availibity(ctx)

    if not pfp:
        pfp = ctx.bot.application.icon_url

    avatar = BytesIO()
    async with pfp.stream() as stream:
        async for chunk in stream:
            avatar.write(chunk)

    loop = ctx.bot.d.loop
    result = await loop.run_in_executor(ctx.bot.d.process_pool, build_image, username, quote, avatar)

    if channel_id:
        await ctx.bot.rest.create_message(
            channel_id,
            f'A new quote was submitted by {ctx.author.mention}',
            attachment=result
        )

    if global_response:
        await ctx.respond('Here is your quote!', attachment=result)
    else:
        channel = ctx.get_guild().get_channel(channel_id).mention
        await ctx.respond(f'You quote was sent straight to {channel}', reply=False)


async def handle_response_embed(
    ctx: lightbulb.Context,
    username: typing.Union[hikari.Member, str],
    quote: str,
    pfp=None
) -> None:

    veriy_field(quote, username)

    global_response, channel_id = get_parameters_and_check_availibity(ctx)

    embed = hikari.Embed()

    embed = hikari.Embed(
        title=f'{username} once said...',
        description=quote,
        color=hikari.Color.from_hex_code(f"#{token_hex(3)}")
    )

    embed.set_thumbnail(pfp)

    embed.timestamp = datetime.datetime.now(tz=datetime.timezone.utc)

    embed.set_footer(
        f'Generated by {ctx.author.username}#{ctx.author.discriminator}'
    )

    if channel_id:
        await ctx.bot.rest.create_message(channel_id, embed)

    if global_response:
        await ctx.respond(embed)
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

    await handle_response_image(ctx, username, quote, avatar)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(
    "embed_this",
    "Click to embed this message.",
    auto_defer=True
)
@lightbulb.implements(lightbulb.MessageCommand)
async def embed_this_cmd(
    ctx: lightbulb.Context
) -> None:

    target = ctx.options.target
    avatar = target.author.avatar_url
    username = f"{target.author.username}#{target.author.discriminator}"
    quote = target.content

    await handle_response_embed(ctx, username, quote, avatar)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'type',
    'The bot can either generate an image, or send an embed.',
    choices=['image', 'embed']
)
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
    quote: str,
    author: str,
    type: str
) -> None:

    username = f"{author.username}#{author.discriminator}"
    avatar = author.avatar_url

    if type == 'image':
        await handle_response_image(ctx, username, quote, avatar)
    else:
        await handle_response_embed(ctx, username, quote, avatar)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'type',
    'The bot can either generate an image, or send an embed.',
    choices=['image', 'embed']
)
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
    quote: str,
    type: str
) -> None:

    author = ctx.author
    username = f"{author.username}#{author.discriminator}"
    avatar = ctx.author.avatar_url

    if type == 'image':
        await handle_response_image(ctx, username, quote, avatar)
    else:
        await handle_response_embed(ctx, username, quote, avatar)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'type',
    'The bot can either generate an image, or send an embed.',
    choices=['image', 'embed']
)
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
    type: str,
    quote: str, author:
        typing.Optional[str] = None,
) -> None:

    if type == 'image':
        await handle_response_image(ctx, author, quote, ctx.bot.application.icon_url)
    else:
        await handle_response_embed(ctx, author, quote, ctx.bot.application.icon_url)


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
