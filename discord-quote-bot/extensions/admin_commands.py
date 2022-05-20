from multiprocessing import context
import hikari
import lightbulb

plugin = lightbulb.Plugin("Admin-Commands")
plugin.add_checks(
    lightbulb.guild_only, 
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)


# -----------------------------------------------------



@plugin.command
@lightbulb.command("set_as_hall_of_fame", "Quotes generated with the bot will appear in this channel.")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_as_hall_of_fame(ctx: lightbulb.Context):
    await ctx.respond('todo')

    
@plugin.command
@lightbulb.option(
    'mode', 'Global: Quotes will appear as replies. Teleport: \
     Quotes will appear in the hall of fame. Mixed: Global + Teleport', 
     required=True, choices=['global', 'teleport', 'mixed']
    )
@lightbulb.command('set_mode', 'Select the mode for bot.')
@lightbulb.implements(lightbulb.SlashCommand)
async def set_mode(ctx: lightbulb.Context):
    await ctx.respond('todo')



# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
