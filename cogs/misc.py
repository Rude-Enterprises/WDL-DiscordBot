from discord.ext import commands

class Misc:
    """Misc holds miscellaneous commands."""
    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command()  # in cogs you use @commands.command instead of @bot.command
    async def more(self):  # commands have to be inside the cog class
        """!more - press the link for more stats."""

        await self.bot.say("More cool stats can be found here:"
                           "http://doomleague.org/forums/index.php?board=8.0")

    @commands.command()
    async def help(self):
        """!help - links to wdlbot documentation."""

        await self.bot.say("""Hello I am a bot. beep boop"""
                           """\nCheck my FAQ: https://github.com/Rude-Enterprises/"""
                           """WDL-DiscordBot/blob/master/commands.md""")


def setup(bot):
    bot.add_cog(Misc(bot))
