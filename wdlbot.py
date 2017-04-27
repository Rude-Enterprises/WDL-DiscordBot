import re
import sys
import os
import asyncio
from datetime import datetime
from discord.ext import commands
import libraries as lb
import cfg
import pandas as pd
import bs4 as bs
import aiohttp
import discord

initial_extensions = ["misc", "stats", "webcmds", "pickups"]

bot = commands.Bot(command_prefix="!", description="Hello I am a bot ! beepboop.")
bot.remove_command("help")

#I FORGET WHY THIS IS HERE LOL
pd.set_option('display.multi_sparse', True)

#all sheets to be used from Jwarrier's wdlstatsv4 read with Pandas
workbook = pd.ExcelFile("C:/Users/Jesse/PycharmProjects/pandas/WDLSTATSv4.xlsx")
player_totals = pd.read_excel(workbook, "PT Player Totals")
player_avg = pd.read_excel(workbook, "PT PlayerAVG")
all_time_playoff = pd.read_excel(workbook, "ALL TIME Playoffs", skiprows=[0], index_col=[0])
season7 = pd.read_excel(workbook, "Season 7", skiprows=[0], index_col=[0])
season6 = pd.read_excel(workbook, "Season 6", skiprows=[0], index_col=[0])
season5 = pd.read_excel(workbook, "Season 5", skiprows=[0], index_col=[0])
season4 = pd.read_excel(workbook, "Season 4", skiprows=[0], index_col=[0])
season3 = pd.read_excel(workbook, "Season 3", skiprows=[0], index_col=[0])
season2 = pd.read_excel(workbook, "Season 2", skiprows=[0], index_col=[0])
season1 = pd.read_excel(workbook, "Season 1", skiprows=[0], index_col=[0])
team_stats = pd.read_excel(workbook, "Team Stats", skiprows=[0], index_col=[1])
player_by_season = pd.read_excel(workbook, "Player By Season")
all_rounds = pd.read_excel(workbook, "All Rounds", index_col=[0])
map_data = pd.read_excel(workbook, "Map Data", index_col=[11])
map_rat_player = pd.read_excel(workbook, "Map RAT by Player", index_col=[1])
map_rat_team = pd.read_excel(workbook, "Map RAT by Team", index_col=[0])


http = aiohttp.ClientSession()

async def gametime_checker():
    """Background Process to alert the channel if there is a game today. Runs every 12 hours"""
    await bot.wait_until_ready()
    counter = 0
    channel = discord.Object(id="157946982567116800")
    while not bot.is_closed:
        counter += 1

        #regexs for gametime_checker
        gametime_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
        playoff_gametime_re = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEDT"
        playoff_team_re = r"#[0-9]\s[\w\s]+\s\[...\]\s\(MAP[0-9]+\)"
        team_str = r"([\w]+)+\s\[...\]"

        #BeautifulSoup stuff used for gametime_checker, need to convert to aiohttp at some point
        resp = await http.get("http://doomleague.org/")
        sauce = await resp.text()
        soup = bs.BeautifulSoup(sauce, "lxml")
        game_times = soup.find_all(text=re.compile(gametime_str))
        game_times_playoffs = soup.find_all(text=re.compile(playoff_gametime_re))
        del game_times_playoffs[-1]

        #lists of all found gametime regexs, regular season, and playoffs
        matchups = soup.find_all(text=re.compile(team_str))
        playoff_matchups = soup.find_all(text=re.compile(playoff_team_re))

        #gametime regex's converted to datetime objects and put in these lists
        date_objects = []
        date_obj_playoffs = []
        tday = datetime.today()

        #gametime regex's converted to datetime objects
        for regexs in game_times:
            date_objects.append(datetime.strptime(regexs, "Gametime: %A, %b %d @ %I:%M%p EST"))

        for regexs in game_times_playoffs:
            date_obj_playoffs.append(datetime.strptime(regexs, "Gametime: %A, %b %d @ %I:%M%p EDT"))

        #checking if there is a game today
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

        #checking if there is a playoff game today
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

    await http.close()

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    print("Onward and Upward")
    print("------")


@bot.event
async def on_message(message):
    """Here are commands relating to !players and !teams. on_message lets us analyze the Discord
    message content to infer the command rather than writing 100+ @command.commands."""

    message_split = message.content.split()
    message_lower = message.content.lower()
    message_upper = message.content.upper()
    message_lower_split = message_lower.split()
    message_upper_split = message_upper.split()
    first_message_string = str(message_upper_split[0])
    first_message_slice = first_message_string[1:]
    first_message_slice_upper = first_message_slice.upper()

    #bot will only work in WDL, Odamex, and testing channels
    if (message.channel.id != cfg.wdl_stats_channelid and
            message.channel.id != cfg.odamex_general_channelid and
            message.channel.id != cfg.bot_test_channelid):
        return

    ##!<player> <stat>
    elif message_lower_split[0] in lb.player_dict and message_lower_split[1] in lb.stat_dict:
        player_stat = player_totals.ix[lb.player_dict[message_lower_split[0]],
                                       lb.stat_dict[message_lower_split[1]]]
        player_stat_round = round(player_stat, 2)
        await bot.send_message(message.channel, "```{} lifetime {}: {} ```".format(
            lb.player_dict[message_lower_split[0]], lb.stat_dict[message_lower_split[1]],
            player_stat_round))

    #!<team> <number> <stat>
    elif message_lower_split[0] in lb.team_dict_two and len(message_lower_split) == 3:
        team_dict_inv_key = (first_message_slice + " " + str(message_lower_split[1]))
        if team_dict_inv_key not in lb.team_dict_inverse:
            await bot.send_message(message.channel, "No team {} found for Season {}".format(first_message_slice_upper,
                                                                                            message_split[1]))
        else:
            team_stat = team_stats.loc[lb.team_dict_inverse[team_dict_inv_key],
                                       lb.stat_dict[message_lower_split[2]]]
            team_stat_round = round(team_stat, 2)
            await bot.send_message(message.channel, "{} Season {} {}: {}".format(lb.team_dict_two[message_lower_split[0]],
                                                                                 message_split[1],
                                                                                 lb.stat_dict[message_lower_split[2]],
                                                                                 team_stat_round))

    elif message_lower_split[0] in lb.team_dict_two and len(message_lower_split) == 2:
        team_dict_inv_key = (first_message_slice + " " + str(message_lower_split[1]))
        if team_dict_inv_key not in lb.team_dict_inverse:
            await bot.send_message(message.channel, "No team {} found for Season {}".format(first_message_slice_upper,
                                                                                            message_split[1]))
        else:
            pass

    await bot.process_commands(message)


if __name__ == "__main__":

    sys.path.insert(1, os.getcwd() + "/cogs/")  # this allows the cogs in the cogs folder to be loaded

    for extension in initial_extensions:
        bot.load_extension(extension)  # This adds the cogs listed in initial_extensions to the bot

    bot.loop.create_task(gametime_checker())
    bot.run(cfg.TOKEN)
