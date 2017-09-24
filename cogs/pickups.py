import asyncio
from discord.ext import commands

player_set = set()
players_for_priv = 6

class Pickups():
    """Pickups - all commands related to Pickup-Game (PUG) Management."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, ignore_extra=False)
    async def add(self, ctx):
        """!add - adds the author (you) to the pickup list.
         Notifying others you are willing to play."""

        player_set.add(ctx.message.author)

        if len(player_set) == players_for_priv:
            player_mentions = ", ".join([all.mention for all in player_set])
            await self.bot.say("{} your game is ready! Odamex 74.91.112.85:10673".format(player_mentions))
            while player_set:
                player_set.pop()
        else:
            await self.bot.say("*CTF*({}/{}) added.".format(len(player_set), players_for_priv))
        await asyncio.sleep(3600)
        try:
            player_set.remove(ctx.message.author)
            await self.bot.say("*CTF*({}/{})".format(len(player_set), players_for_priv))
        except KeyError:
            pass

    @commands.command(pass_context=True)
    async def remove(self, ctx):
        """!remove - removes the author (you) from the pickup queue"""

        player_set.remove(ctx.message.author)

        await self.bot.say("*CTF*({}/{})".format(len(player_set), players_for_priv))

    @commands.command(pass_context=True)
    async def who(self):
        """!who - tells who is currently !added."""

        player_string = ", ".join(str(any) for any in player_set)

        if not player_set:
            await self.bot.say("None added!")
        elif player_set:
            await self.bot.say("Players added: {}".format(player_string))
        else:
            pass

def setup(bot):
    bot.add_cog(Pickups(bot))
