from discord.ext import commands
import asyncio

player_set = set()
players_for_priv = 6

class Pickups():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, ignore_extra=False)
    async def add(self, ctx):
        player_set.add(ctx.message.author)
        if len(player_set) == players_for_priv:
            await self.bot.say("""{} your game is ready! Join the WDL priv-CTF server: password = season4""".format(
                ", ".join([all.mention for all in player_set])))
            while player_set:
                player_set.pop()

        else:
            await self.bot.say("({}/{}) added, {} more needed for Priv CTF.".format(
                len(player_set), players_for_priv, (players_for_priv - len(player_set))))

        await asyncio.sleep(3600)

        try:
            player_set.remove(ctx.message.author)
            await self.bot.say("{} has been auto-removed from privlist".format(ctx.message.author))

        except KeyError:
            pass

    @commands.command(pass_context=True)
    async def remove(self, ctx):
        player_set.remove(ctx.message.author)
        await self.bot.say("""You have been removed from the list. {}/{} added. {} needed for a game.""".format(
                        len(player_set), players_for_priv, (players_for_priv - len(player_set))))

    @commands.command(pass_context=True)
    async def who(self, ctx):
        player_string = ", ".join(str(any) for any in player_set)
        if not player_set:
            await self.bot.say("None added!")
        if player_set:
            await self.bot.say("Players added: {}".format(player_string))

def setup(bot):
    bot.add_cog(Pickups(bot))
