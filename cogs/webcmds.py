from discord.ext import commands
import bs4 as bs
import urllib.request
from datetime import datetime
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
        for any in game_times:
            date_objects = []
            date_objects.append(datetime.datetime.strptime(any, "Gametime: %A, %b %d @ %I:%M%p %Z"))

        await self.bot.say(game_times[:4])

    @commands.command()
    async def gametime(self):
        rege_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
        sauce = urllib.request.urlopen("http://doomleague.org/").read()
        soup = bs.BeautifulSoup(sauce, "lxml")
        game_times = soup.find_all(text=re.compile(rege_str))
        date_objects = []
        tday = datetime.today()

        for any in game_times:
            date_objects.append(datetime.strptime(any, "Gametime: %A, %b %d @ %I:%M%p EST"))
        for any in date_objects:
            if any.day == tday.day and any.month == tday.month:
                await self.bot.say("game on the {}".format(tday.day))
            else:
                pass

def setup(bot):
    bot.add_cog(Web(bot))
