import hikari
import lightbulb

plugin = lightbulb.Plugin("Quote-Maker")

# TODO: @lightbulb.add_cooldown(15.0, 1, lightbulb.TheRightBuckeit) later


# -----------------------------------------------------


# TODO: Implement the check (author must not be @everyone or @here)
@lightbulb.Check
def author_check(ctx: lightbulb.Context) -> bool:
    print(ctx.interaction.options.index)
    return True


# -----------------------------------------------------


@plugin.command
@lightbulb.command("quote_this", "Click to quote this message.")
@lightbulb.implements(lightbulb.MessageCommand)
async def quote_this_cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond('test')



@plugin.command
@lightbulb.add_checks(author_check)
@lightbulb.option('author', 'The author of the quote',
                  required=True, autocomplete=True)
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_user", "Generates a quote when invoked.")
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_user_cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond('test')


@quote_user_cmd.autocomplete("author")
async def quote_user_cmd_author_autocomplete(option, interaction):
    members = lightbulb.Context.get_guild(interaction).get_members().values()
    member_list = [f"{member.username}#{member.discriminator}" for member in members]
    return member_list



@plugin.command
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_me", "Generates a quote when invoked.")
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_me_cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond('pong! uwu')


@plugin.command
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.option('author', 'The author of the quote', default='anonymous-wolf')
@lightbulb.command("quote_anon", "Generates a quote when invoked.")
@lightbulb.implements(lightbulb.SlashCommand)
async def quote_anon_cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond('pong! uwu')


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
