from discord.ext import commands
import bs4 as bs
import urllib.request
import re
import pandas as pd

class Web():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def standings(self):
        wdl_standings = pd.read_html("http://doomleague.org", index_col=0)
        standings_table = wdl_standings[0][["PTS", "PF", "PA"]]
        await self.bot.say("```WDL Season 7 Standings\n\n{}```".format(str(standings_table)))

    @commands.command()
    async def gameday(self):
        rege_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
        sauce = urllib.request.urlopen("http://doomleague.org/").read()
        soup = bs.BeautifulSoup(sauce, "lxml")
        game_times = soup.find_all(text=re.compile(rege_str))
        await self.bot.say(game_times[:4])

def setup(bot):
    bot.add_cog(Web(bot))
