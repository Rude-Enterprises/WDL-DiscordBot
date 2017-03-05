from discord.ext import commands
import asyncio
import wdlBot as wdl

class Pickups():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, ignore_extra=False)
    async def add(self, ctx):
        wdl.player_set.add(ctx.message.author)
        await self.bot.say("({}/{}) added, {} more needed for Priv CTF.".format(
                len(wdl.player_set), wdl.players_for_priv, (wdl.players_for_priv - len(wdl.player_set))))

        if len(wdl.player_set) == 1:
            await self.bot.say("""{} your game is ready! Join the WDL priv-CTF server: password = season4""".format(
                                                             ", ".join([all.mention for all in wdl.player_set])))
            while wdl.player_set:
                wdl.player_set.pop()

        await asyncio.sleep(3600)
        try:
            wdl.player_set.remove(ctx.message.author)
            await self.bot.say("{} has been auto-removed from privlist".format(ctx.message.author))
        except KeyError:
            pass

    @commands.command(pass_context=True)
    async def remove(self, ctx):
        wdl.player_set.remove(ctx.message.author)
        await self.bot.say("""You have been removed from the list. {}/{} added. {} needed for a game.""".format(
                        len(wdl.player_set), wdl.players_for_priv, (wdl.players_for_priv - len(wdl.player_set))))

    @commands.command(pass_context=True)
    async def who(self, ctx):
        player_string = ", ".join(str(any) for any in wdl.player_set)
        if not wdl.player_set:
            await self.bot.say("None added!")
        if wdl.player_set:
            await self.bot.say("Players added: {}".format(player_string))

def setup(bot):
    bot.add_cog(Pickups(bot))
