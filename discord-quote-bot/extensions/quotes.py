import hikari
import lightbulb
import typing

plugin = lightbulb.Plugin("Quote-Maker")


# -----------------------------------------------------


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command("quote_this", "Click to quote this message.")
@lightbulb.implements(lightbulb.MessageCommand)
async def quote_this_cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.event.content)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option('author', 'The author of the quote', hikari.Member, required=True)
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_user", "Generates a quote when invoked.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_user_cmd(ctx: lightbulb.Context, quote: str, author: hikari.Member) -> None:
    await ctx.respond('test')


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_me", "Generates a quote when invoked.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_me_cmd(ctx: lightbulb.Context, quote: str) -> None:
    await ctx.respond('pong! uwu')


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.option('author', 'The author of the quote', default='anonymous-wolf')
@lightbulb.command("quote_anon", "Generates a quote when invoked.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_anon_cmd(ctx: lightbulb.Context, quote: str, author: typing.Optional[str] = None) -> None:
    await ctx.respond('pong! uwu')


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
