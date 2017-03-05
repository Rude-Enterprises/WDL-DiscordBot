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
        team_str = r"([\w]+)+\s\[...\]"
        sauce = urllib.request.urlopen("http://doomleague.org/").read()
        soup = bs.BeautifulSoup(sauce, "lxml")
        game_times = soup.find_all(text=re.compile(gametime_str))
        matchups = soup.find_all(text=re.compile(team_str))
        date_objects = []
        tday = datetime.today()

        for any in game_times:
            date_objects.append(datetime.strptime(any, "Gametime: %A, %b %d @ %I:%M%p EST"))
        for any in date_objects:
            if any.day == tday.day and any.month == tday.month:
                if any == date_objects[0]:
                    await self.bot.say("{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[0], matchups[1],
                                                                        any.month, any.day, any.hour, any.minute))
                elif any == date_objects[1]:
                    await self.bot.say(
                                           "{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[2], matchups[3],
                                                                        any.month, any.day, any.hour, any.minute))
                elif any == date_objects[2]:
                    await self.bot.say(
                                           "{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[4], matchups[5],
                                                                        any.month, any.day, any.hour, any.minute))
                elif any == date_objects[3]:
                    await self.bot.say(
                                           "{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[6], matchups[7],
                                                                        any.month, any.day, any.hour, any.minute))
                elif any == date_objects[4]:
                    await self.bot.say(
                                           "{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[8], matchups[9],
                                                                        any.month, any.day, any.hour, any.minute))
                elif any == date_objects[5]:
                    await self.bot.say(
                                           "{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[10], matchups[11],
                                                                        any.month, any.day, any.hour, any.minute))
                elif any == date_objects[6]:
                    await self.bot.say(
                                           "{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[12], matchups[13],
                                                                        any.month, any.day, any.hour, any.minute))
                elif any == date_objects[7]:
                    await self.bot.say(
                                           "{} vs {} today, {}/{}- at {}:{} EST!".format(matchups[14], matchups[15],
                                                                        any.month, any.day, any.hour, any.minute))
                else:
                    pass
            else:
                pass

def setup(bot):
    bot.add_cog(Web(bot))
