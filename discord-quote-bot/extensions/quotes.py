import hikari
import lightbulb
from nextcord import Interaction

plugin = lightbulb.Plugin("Quote-Maker")

# TODO: @lightbulb.add_cooldown(15.0, 1, lightbulb.TheRightBuckeit) later


# -----------------------------------------------------


# TODO: Implement the check (author must not be @everyone or @here)
@lightbulb.Check
def author_check(ctx: lightbulb.Context) -> bool:
    return True


# -----------------------------------------------------


@plugin.command
@lightbulb.command("quote", "Click to quote this message.")
@lightbulb.implements(lightbulb.MessageCommand)
async def make_quote(ctx: lightbulb.Context) -> None:
    await ctx.respond('test')


@plugin.command
@lightbulb.add_checks(author_check)
@lightbulb.option('author', 'The author of the quote',
                  required=True, default='anoymous-wolf', autocomplete=True)
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_this", "Generates a quote when invoked.")
@lightbulb.implements(lightbulb.SlashCommand)
async def make_quote_cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond('test')


@make_quote_cmd.autocomplete("author")
async def foo_cmd_autocomplete(option, interaction):
    # extract  in ctx.get_guild().get_members().values():
    return ['test1', 'test2']


@plugin.command
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_me", "Generates a quote when invoked.")
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_me_cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond('pong! uwu')


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
