import hikari
import lightbulb

test_plugin = lightbulb.Plugin("Test")


@test_plugin.command
@lightbulb.command("ping", "Simple ping command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond('pong! uwu')


@test_plugin.command
@lightbulb.command("pong", "Simple pong command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond('ping! owo')


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(test_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(test_plugin)
