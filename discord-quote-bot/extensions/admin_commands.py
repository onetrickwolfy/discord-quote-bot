import hikari
import lightbulb

plugin = lightbulb.Plugin("Admin-Commands")


# -----------------------------------------------------


@plugin.command
@lightbulb.command("set_channel",
                   "Sets a channel for the quotes the be sent in.")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_channel(ctx: lightbulb.Context):
    await ctx.respond('todo')


@plugin.command
@lightbulb.command("toggle_global_response",
                   "Toggles & Untoggles the responses in the channel the bot was invocated in.")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_channel(ctx: lightbulb.Context):
    await ctx.respond('todo')


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
