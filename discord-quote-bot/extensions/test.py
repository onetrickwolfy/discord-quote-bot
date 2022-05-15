import hikari
import lightbulb

info_plugin = lightbulb.Plugin("Test")


@info_plugin.command
@lightbulb.command("ping", "Simple ping command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond('pong! uwu')


@info_plugin.command
@lightbulb.command("pong", "Simple pong command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond('ping! owo')


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)
