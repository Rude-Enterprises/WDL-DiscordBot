from discord.ext import commands
import libraries as lb
import pandas as pd
import numpy as np
import bs4 as bs
import urllib.request
import datetime
import asyncio
import re
import sys
import os
from pytime import pytime

initial_extensions = ["misc", "stats"]

bot = commands.Bot(command_prefix="!", description="Hello I am a bot ! beepboop.")
bot.remove_command("help")

sauce = urllib.request.urlopen("http://doomleague.org/").read()
soup = bs.BeautifulSoup(sauce, "lxml")
div = soup.div
tday = datetime.datetime.today()

print(tday)

#REGEX FOR GAMETIMES ON WDL.ORG
rege_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
rege_test = r"Gametime:"

#FINDS ALL GAMETIME STRINGS FROM WDL.ORG
game_times = soup.find_all(text=re.compile(rege_str))

print(game_times)

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

print(all_rounds.axes)


player_set = set()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def game_time():
    pass

@bot.event
async def on_message(message):
    players_for_priv = 6
    seasons = [1, 2, 3, 4, 5, 6, 7]
    message_split = message.content.split()
    message_lower = message.content.lower()
    message_upper = message.content.upper()
    message_lower_split = message_lower.split()
    message_upper_split = message_upper.split()
    first_message_string = str(message_upper_split[0])
    first_message_slice = first_message_string[1:]
    first_message_slice_upper = first_message_slice.upper()

    if message_split[0] == "!add":
        player_set.add(message.author)
        player_len = len(player_set)
        await bot.send_message(message.channel, "({}/{}) added, {} more needed for Priv CTF.".format(
            player_len, players_for_priv, (players_for_priv - player_len)))

        if player_len == 6:
            await bot.send_message(message.channel, """{} your game is ready!\
            Join the WDL priv server, password = season4""".format(
            ", ".join([x.mention for x in player_set])))
            while player_set:
                player_set.pop()

        await asyncio.sleep(3600)
        try:
            player_set.remove(message.author)
            await bot.send_message(message.channel, "{} has been auto-removed from privlist".format(message.author))
        except KeyError:
            pass



    if message_lower == "!remove":
        player_set.remove(message.author)
        player_len = len(player_set)
        await bot.send_message(message.channel, """You have been removed from the list.\
 {}/{} added. {} needed for a game.""".format(
                        player_len, players_for_priv, (players_for_priv - player_len)))

    if message_lower == "!who":
        player_string = ", ".join(str(any) for any in player_set)
        if not player_set:
            await bot.send_message(message.channel, "None added!")
        if player_set:
            await bot.send_message(message.channel, "Players added: {}".format(player_string))

#!<player> <stat>
    if message.channel.id != "281128620146032641":
        return

    elif message_lower_split[0] in lb.player_dict and message_lower_split[1] in lb.stat_dict:
        player_stat = player_totals.ix[lb.player_dict[message_lower_split[0]], lb.stat_dict[message_lower_split[1]]]
        player_stat_round = round(player_stat, 2)
        await bot.send_message(message.channel, "```{} lifetime {}: {} ```".format(
            lb.player_dict[message_lower_split[0]], lb.stat_dict[message_lower_split[1]], player_stat_round))

#!<team> <number> <stat>
    elif message_lower_split[0] in lb.team_dict_two and len(message_lower_split) == 3:
        team_dict_inv_key = (first_message_slice + " " + str(message_lower_split[1]))
        if team_dict_inv_key not in lb.team_dict_inverse:
            await bot.send_message(message.channel, "No team {} found for Season {}".format(first_message_slice_upper,
                                                                                         message_split[1]))
        else:
            team_stat = team_stats.loc[lb.team_dict_inverse[team_dict_inv_key], lb.stat_dict[message_lower_split[2]]]
            team_stat_round = round(team_stat, 2)
            await bot.send_message(message.channel, "{} Season {} {}: {}".format(lb.team_dict_two[message_lower_split[0]],
                                                        message_split[1], lb.stat_dict[message_lower_split[2]], team_stat_round))

    elif message_lower_split[0] in lb.team_dict_two and len(message_lower_split) == 2:
        team_dict_inv_key = (first_message_slice + " " + str(message_lower_split[1]))
        if team_dict_inv_key not in lb.team_dict_inverse:
            await bot.send_message(message.channel, "No team {} found for Season {}".format(first_message_slice_upper,
                                                                                         message_split[1]))
        else:
            pass

    await bot.process_commands(message)



if __name__ == '__main__':

    sys.path.insert(1, os.getcwd() + "/cogs/")  # this allows the cogs in the cogs folder to be loaded

    for extension in initial_extensions:
        bot.load_extension(extension)  # This adds the cogs listed in initial_extensions to the bot

    bot.run("USER", "PASS")