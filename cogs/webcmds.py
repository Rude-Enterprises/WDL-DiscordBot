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
        await self.bot.say("```WDL Season 7 Standings{}```".format(str(standings_table)))

    @commands.command()
    async def gameday(self):
        rege_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
        sauce = urllib.request.urlopen("http://doomleague.org/").read()
        soup = bs.BeautifulSoup(sauce, "lxml")
        game_times = soup.find_all(text=re.compile(rege_str))
        for any in game_times:
            date_objects = []
            date_objects.append(datetime.strptime(any, "Gametime: %A, %b %d @ %I:%M%p %Z"))

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

    @commands.command()
    async def today(self):
        gametime_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
        playoff_gametime_re = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEDT"
        team_str = r"([\w]+)+\s\[...\]"
        playoff_team_re = r"#[0-9]\s[\w\s]+\s\[...\]\s\(MAP[0-9]+\)"
        sauce = urllib.request.urlopen("http://doomleague.org/").read()
        soup = bs.BeautifulSoup(sauce, "lxml")
        game_times = soup.find_all(text=re.compile(gametime_str))
        game_times_playoffs = soup.find_all(text=re.compile(playoff_gametime_re))
        del game_times_playoffs[-1]
        matchups = soup.find_all(text=re.compile(team_str))
        playoff_matchups = soup.find_all(text=re.compile(playoff_team_re))
        date_objects = []
        date_objects_playoffs = []
        tday = datetime.today()

        for any in game_times:
            date_objects.append(datetime.strptime(any, "Gametime: %A, %b %d @ %I:%M%p EST"))

        for any in game_times_playoffs:
            date_objects_playoffs.append(datetime.strptime(any, "Gametime: %A, %b %d @ %I:%M%p EDT"))

        for any in date_objects:
            if any.day == tday.day and any.month == tday.month:
                await self.bot.say("**{} vs {}** - today {}/{} at {}:{} EST!".format(matchups[(date_objects.index(any) * 2)],
                                matchups[(date_objects.index(any) * 2) + 1], any.month, any.day, any.hour, any.minute))
            else:
                pass

        for any in date_objects_playoffs:
            if any.day == tday.day and any.month == tday.month and tday.hour < any.hour:
                await self.bot.say("**{} @ {}** - today {}/{} at {}:{} EST!".format(playoff_matchups[(date_objects_playoffs.index(any) * 2)],
                                    playoff_matchups[(date_objects_playoffs.index(any) * 2) + 1], any.month, any.day, any.hour, any.minute))
            else:
                pass

def setup(bot):
    bot.add_cog(Web(bot))
