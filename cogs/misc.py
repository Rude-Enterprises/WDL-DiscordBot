from discord.ext import commands

class Misc:
    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command()  # in cogs you use @commands.command instead of @bot.command
    async def more(self):  # commands have to be inside the cog class
        await self.bot.say("More cool stats can be found here: http://doomleague.org/forums/index.php?board=8.0")  # Use self.bot inside cogs

    @commands.command()
    async def help(self):
        help_text = """Hello I am a bot. beep boop
                                  \nCheck my FAQ: https://github.com/Rude-Enterprises/WDL-DiscordBot/blob/master/commands.md"""
        await self.bot.say(help_text)


def setup(bot):
    bot.add_cog(Misc(bot))