from multiprocessing import context
from re import S
import hikari
import lightbulb
from utils import guilds_settings
from tinydb import Query

plugin = lightbulb.Plugin("Admin-Commands")
plugin.add_checks(
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)


# -----------------------------------------------------


@plugin.command
@lightbulb.command("set_as_hall_of_fame",
                   "Quotes generated with the bot will appear in this channel.")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_as_hall_of_fame(ctx: lightbulb.Context):
    
    guilds_settings.upsert(
        {
                'guild_id': ctx.guild_id,
                'hall_of_fame': ctx.channel_id
        },
        Query().guild_id == ctx.guild_id
    )
    
    await ctx.respond('This channel has been set has the hall of fame.')



@plugin.command
@lightbulb.option(
    'mode', 'Teleport/Mixed will send quotes in the hall of fame.',
    required=True, 
    choices=['global', 'teleport', 'mixed']
)
@lightbulb.command('set_mode', 'Select the mode for bot.', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def set_mode(ctx: lightbulb.Context, mode=str):
    
    row_id = guilds_settings.upsert(
        {
                'guild_id': ctx.guild_id,
                'mode': mode
        },
        Query().guild_id == ctx.guild_id
    )
    
    if not guilds_settings.get(doc_id=row_id).get('hall_of_fame'):
        await ctx.respond('Do not forget  to define a hall of fame.', reply=False)
    
    await ctx.respond(f'You mode has been changed to {mode}')


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
