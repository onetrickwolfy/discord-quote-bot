import nextcord
from nextcord.ext import commands

TESTING_GUILD_ID = ''


class Test(commands.Cog):
    """Tests & Beta Commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID],
                            description="Test command")
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("pong")


def setup(bot):
    bot.add_cog(Test(bot))
