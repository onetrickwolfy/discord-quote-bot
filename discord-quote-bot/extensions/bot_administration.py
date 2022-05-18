import hikari
import lightbulb

plugin = lightbulb.Plugin("Bot-Administration")


# -----------------------------------------------------


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("reload_extension", "reload extensions", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def reload_extension(ctx: lightbulb.Context):
    [ctx.bot.reload_extensions(ext) for ext in ctx.bot.extensions]
    await ctx.respond("Reloaded all extensions successfully. ;p", reply=False)


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("sync_application_commands",
                   "sync the accplication commands", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def sync_application_commands(ctx: lightbulb.Context):
    await ctx.bot.sync_application_commands()
    await ctx.respond("Synced application commands", reply=False)


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("get_latency", "send the current latency", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def get_latency(ctx: lightbulb.Context):
    await ctx.respond(ctx.bot.heartbeat_latency, reply=False)


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("purge_commands", "purge the commands", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def purge_commands(ctx: lightbulb.Context):
    await ctx.bot.purge_application_commands(global_commands=True)
    await ctx.respond("Purged application commands", reply=False)


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
