import aiohttp
import asyncio
import bs4 as bs
from datetime import datetime
import discord
import re

class Process():
    def __init__(self, bot):
        self.bot = bot
        self.task = bot.loop.create_task(self.gametime_checker())

    async def gametime_checker(self):
        """Background Process to alert the channel if there is a game today. Runs every 12 hours"""

        channel = discord.Object(id="157946982567116800")
        http = aiohttp.ClientSession()

        # regexs for gametime_checker
        gametime_str = r"Gametime:\s[\w]+(,\s|\s)[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9](|PM)\sEST"
        playoff_gametime_re = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEDT"
        playoff_team_re = r"#[0-9]\s[\w\s]+\s\[...\]\s\(MAP[0-9]+\)"
        team_str = r"(([\w]+)|[Damn!]){1,3}\s\[...\]"

        try:
            while not self.bot.is_closed:

                # Processing WDL.org with BS
                resp = await http.get("http://doomleague.org/")
                sauce = await resp.text()
                soup = bs.BeautifulSoup(sauce, "lxml")
                game_times = soup.find_all(text=re.compile(gametime_str))
                game_times_playoffs = soup.find_all(text=re.compile(playoff_gametime_re))


                print(game_times)
                for i in range(0, len(game_times)):
                    temp_list = game_times[i].split()
                    if "," not in game_times[i]:
                        temp_list[1] = temp_list[1] + ","
                    if "PM" not in game_times[i]:
                        temp_list[5] = temp_list[5] + "PM"
                    game_times[i] = " ".join(temp_list)

                print(game_times)
                # lists of all found gametime regexs, regular season, and playoffs
                matchups = soup.find_all(text=re.compile(team_str))
                playoff_matchups = soup.find_all(text=re.compile(playoff_team_re))

                # containers for datetimes of gametimes
                date_objects = []
                date_obj_playoffs = []


                # gametime regex's converted to datetime objects
                for regexs in game_times:
                    date_objects.append(datetime.strptime(regexs, "Gametime: %A, %b %d @ %I:%M%p EST"))
                print(date_objects)
                for regexs in game_times_playoffs:
                    date_obj_playoffs.append(datetime.strptime(regexs, "Gametime: %A, %b %d @ %I:%M%p EDT"))

                tday = datetime.today()
                for obj in date_objects:
                    print("**{} vs {}** - today {}/{} at {:%I:%M%p} EST!".format(
                            matchups[(date_objects.index(obj) * 2)],
                            matchups[(date_objects.index(obj) * 2) + 1],
                            obj.month,
                            obj.day,
                            obj))
                #checking if there is a game today

                for obj in date_objects:
                    if obj.day == tday.day and obj.month == tday.month and tday.hour < obj.hour:
                        await self.bot.send_message(channel, "**{} vs {}** - today {}/{} at {:%I:%M%p} EST!".format(
                            matchups[(date_objects.index(obj) * 2)],
                            matchups[(date_objects.index(obj) * 2) + 1],
                            obj.month,
                            obj.day,
                            obj))
                    else:
                        pass

                # checking if there is a playoff game today
                for obj in date_obj_playoffs:
                    if obj.day == tday.day and obj.month == tday.month and tday.hour < obj.hour:
                        await self.bot.send_message(channel, "**{} @ {}** - today {}/{} at {:%I:%M%p} EST!".format(
                            playoff_matchups[(date_obj_playoffs.index(obj) * 2)],
                            playoff_matchups[(date_obj_playoffs.index(obj) * 2) + 1],
                            obj.month,
                            obj.day,
                            obj))
                    else:
                        pass


                # task runs every 12 hours
                await asyncio.sleep(43200)

        # if task is cancelled
        finally:
            await http.close()


def setup(bot):
    bot.add_cog(Process(bot))
