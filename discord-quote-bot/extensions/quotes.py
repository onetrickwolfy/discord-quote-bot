import hikari
import lightbulb

plugin = lightbulb.Plugin("Quote-Maker")

# add @lightbulb.add_cooldown(15.0, 1,
# lightbulb.SlashCommandCompletionEvent) later


# TODO: Implement the check (author must not be @everyone or @here)
@lightbulb.Check
def check_author(ctx: lightbulb.Context) -> bool:
    return True


@plugin.command
@lightbulb.command("quote", "Click to quote this message.")
@lightbulb.implements(lightbulb.MessageCommand)
async def make_quote(ctx: lightbulb.Context) -> None:
    await ctx.respond('test')


@plugin.command
@lightbulb.command("test", "Click to quote this message.")
@lightbulb.implements(lightbulb.SlashCommand)
async def make_quote(ctx: lightbulb.Context) -> None:
    members = ctx.get_guild().get_members()

    for member in ctx.get_guild().get_members().values():
        # await ctx.bot.rest.create_message(ctx.channel_id, member.mention, user_mentions=True)
        # await ctx.respond( "@" + member.username + "#" + member.discriminator
        # + "  " + member.display_name)
        pass


@plugin.command
@lightbulb.add_checks(check_author)
@lightbulb.option('author', 'The author of the quote',
                  required=True, default='anoymous-wolf', choices=[])
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_this", "Generates a quote when invoked.")
@lightbulb.implements(lightbulb.SlashCommand)
async def make_quote(ctx: lightbulb.Context) -> None:
    await ctx.respond('test')


@plugin.command
@lightbulb.option('quote', 'The text you would like to quote', required=True)
@lightbulb.command("quote_me", "Generates a quote when invoked.")
@lightbulb.implements(lightbulb.SlashCommand)
async def make_quote(ctx: lightbulb.Context) -> None:
    await ctx.respond('pong! uwu')


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
