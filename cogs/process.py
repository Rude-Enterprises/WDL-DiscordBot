import bs4 as bs
import discord
import re
import aiohttp
from datetime import datetime
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="!", description="Hello I am a bot ! beepboop.")

async def gametime_checker():
    """Background Process to alert the channel if there is a game today. Runs every 12 hours"""

    await bot.wait_until_ready()

    channel = discord.Object(id="157946982567116800")
    http = aiohttp.ClientSession()

    try:
        while not bot.is_closed:

            # regexs for gametime_checker
            gametime_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
            playoff_gametime_re = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEDT"
            playoff_team_re = r"#[0-9]\s[\w\s]+\s\[...\]\s\(MAP[0-9]+\)"
            team_str = r"([\w]+)+\s\[...\]"

            # Processing WDL.org with BS
            resp = await http.get("http://doomleague.org/")
            sauce = await resp.text()
            soup = bs.BeautifulSoup(sauce, "lxml")
            game_times = soup.find_all(text=re.compile(gametime_str))
            game_times_playoffs = soup.find_all(text=re.compile(playoff_gametime_re))
            del game_times_playoffs[-1]

            # lists of all found gametime regexs, regular season, and playoffs
            matchups = soup.find_all(text=re.compile(team_str))
            playoff_matchups = soup.find_all(text=re.compile(playoff_team_re))

            # gametime regex's converted to datetime objects and put in these lists
            date_objects = []
            date_obj_playoffs = []
            tday = datetime.today()

            # gametime regex's converted to datetime objects
            for regexs in game_times:
                date_objects.append(datetime.strptime(regexs, "Gametime: %A, %b %d @ %I:%M%p EST"))

            for regexs in game_times_playoffs:
                date_obj_playoffs.append(datetime.strptime(regexs, "Gametime: %A, %b %d @ %I:%M%p EDT"))

            # checking if there is a game today
            for obj in date_objects:
                if obj.day == tday.day and obj.month == tday.month and tday.hour < obj.hour:
                    await bot.send_message(channel, "**{} vs {}** - today {}/{} at {}:{} EST!".format(
                        matchups[(date_objects.index(obj) * 2)],
                        matchups[(date_objects.index(obj) * 2) + 1],
                        obj.month,
                        obj.day,
                        obj.hour,
                        obj.minute))
                else:
                    pass

            # checking if there is a playoff game today
            for obj in date_obj_playoffs:
                if obj.day == tday.day and obj.month == tday.month and tday.hour < obj.hour:
                    await bot.send_message(channel, "**{} @ {}** - today {}/{} at {}:{} EST!".format(
                        playoff_matchups[(date_obj_playoffs.index(obj) * 2)],
                        playoff_matchups[(date_obj_playoffs.index(obj) * 2) + 1],
                        obj.month,
                        obj.day,
                        obj.hour,
                        obj.minute))
                else:
                    pass

            # task runs every 12 hours
            await asyncio.sleep(43200)

    # if task is cancelled
    finally:
        await http.close()



async def new_homepage_post():
    """Background Process to alert the channel if there is a game today. Runs every 12 hours"""

    await bot.wait_until_ready()

    channel = discord.Object(id="157946982567116800")
    http = aiohttp.ClientSession()

    try:
        while not bot.is_closed:

            # Processing WDL.org with BS
            resp = await http.get("http://doomleague.org/")
            sauce = await resp.text()
            soup = bs.BeautifulSoup(sauce, "lxml")
            print(soup.text)


            # task runs every 12 hours
            await asyncio.sleep(43200)

    # if task is cancelled
    finally:
        await http.close()


