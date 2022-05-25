from multiprocessing import context
import hikari
import lightbulb
from utils import guilds_settings
from tinydb import Query
from tinydb.operations import delete
from utils import get_config

plugin = lightbulb.Plugin("Admin-Commands")
plugin.add_checks(
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)

conf = get_config()


# -----------------------------------------------------


@plugin.command
@lightbulb.command('hall_of_fame',
                   'If set, quotes will be sent in the hall of fame.')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def hall_of_fame_grp(ctx: lightbulb.Context):
    pass


@hall_of_fame_grp.child
@lightbulb.command('set', 'Sets a channel as the hall of fame')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toggle_scmd(ctx: lightbulb.Context):
    guilds_settings.upsert(
        {
            'guild_id': ctx.guild_id,
            'hall_of_fame': ctx.channel_id
        },
        Query().guild_id == ctx.guild_id
    )

    await ctx.respond('This channel has been set as the hall of fame.')


@hall_of_fame_grp.child
@lightbulb.command('unset', 'Unsets the hall of fame.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toggle_scmd(ctx: lightbulb.Context):
    guilds_settings.upsert(
        {
            'guild_id': ctx.guild_id,
            'hall_of_fame': None
        },
        Query().guild_id == ctx.guild_id
    )

    await ctx.respond('The hall of fame has been unset.')


# -----------------------------------------------------


@plugin.command
@lightbulb.command('global_mode', 'Enables and disables the global mode.')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def global_mode_grp(ctx: lightbulb.context):
    pass


@global_mode_grp. child
@lightbulb.command('enable',
                   'The bot will reply in the channel it was invocated in.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def enable_scmd(ctx: lightbulb.Context):
    guilds_settings.upsert(
        {
            'guild_id': ctx.guild_id,
            'global': True
        },
        Query().guild_id == ctx.guild_id
    )

    await ctx.respond('Global mode has been activated.')


@global_mode_grp. child
@lightbulb.command('disable',
                   'The bot will only reply in the hall of fame, if set.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def disable_scmd(ctx: lightbulb.Context):
    row_id = guilds_settings.upsert(
        {
            'guild_id': ctx.guild_id,
            'global': False
        },
        Query().guild_id == ctx.guild_id
    )

    await ctx.respond('Global mode has been disabled.')

    if not guilds_settings.get(doc_id=row_id[0]).get('hall_of_fame'):
        await ctx.respond('Do not forget to define the hall of fame.', reply=False)


# -----------------------------------------------------

@plugin.command
@lightbulb.command('settings', 'Display the current settings')
@lightbulb.implements(lightbulb.SlashCommand)
async def display_settings(ctx: lightbulb.context):
    guild = guilds_settings.get(Query().guild_id == ctx.guild_id)

    await ctx.respond('\n'.join([
        f"Guild Id: {guild['guild_id']}",
        f"Global mode: {'Enabled' if (guild['global']) else 'Disabled'}",
        f"Hall of fame: {guild['hall_of_fame'] if (guild['hall_of_fame']) else 'Unset'}"
    ])
    )

# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
