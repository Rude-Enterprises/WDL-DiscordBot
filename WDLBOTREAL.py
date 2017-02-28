import discord
import libraries as lb
from discord.ext import commands
import random
import pandas as pd
import numpy as np
import bs4 as bs
import urllib.request
import datetime
import asyncio
import re
from pytime import pytime


bot = commands.Bot(command_prefix="!", description="Hello I am a bot ! beepboop.")
bot.remove_command("help")


sauce = urllib.request.urlopen("http://doomleague.org/").read()
soup = bs.BeautifulSoup(sauce, "lxml")
div = soup.div
tday = datetime.datetime.today()

print(tday)

rege_str = r"Gametime:\s[\w]+,\s[\w]{3}\s[0-9]+\s@\s[0-9]+:[0-9][0-9]PM\sEST"
rege_test = r"Gametime:"

game_times = soup.find_all(text=re.compile(rege_str))

print(game_times)

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

all_time_playoff.name = "All time Playoffs"
season7.name = "Season 7"
season6.name = "Season 6"
season5.name = "Season 5"
season4.name = "Season 4"
season3.name = "Season 3"
season2.name = "Season 2"
season1.name = "Season 1"
team_stats.name = "Team Stats"

sheet_set = (all_time_playoff,
             season7,
             season6,
             season5,
             season4,
             season3,
             season2,
             season1,
             team_stats
             )

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

#WDL Bot FAQ
@bot.command()
async def help():
    help_text = """Hello I am a bot. beep boop
                          \nCheck my FAQ: https://www.dropbox.com/s/ioj7hnh42n2wdh8/WDLSTATFAQ.txt?dl=0"""
    await bot.say(help_text)
    
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


#Standings Table from WDL.org read with Pandas
@bot.command()
async def standings():
    wdl_standings = pd.read_html("http://doomleague.org", index_col=0)
    standings_table = wdl_standings[0][["PTS", "PF", "PA"]]
    await bot.say("```WDL Season 7 Standings\n\n{}```".format(str(standings_table)))

#wdl forums stats
@bot.command()
async def more():
    await bot.say("More cool stats can be found here: http://doomleague.org/forums/index.php?board=8.0")



@bot.command()
async def randstat():
    randsheet = sheet_set[random.randint(0, 8)]
    index_length = len(randsheet.index)
    col_length = len(randsheet.columns)
    player_or_team_id = randsheet.index[random.randint(1, (index_length - 1))]
    stat_name = randsheet.columns[random.randint(0, (col_length - 1))]

    if randsheet.name == "Team Stats":
        random_team_stat = randsheet.loc[player_or_team_id, stat_name]
        team_str = str(lb.team_dict[player_or_team_id])
        team_str_season = team_str[4]
        team_str_3char = team_str[:3]
        team_str_3char_exc = "!" + team_str_3char
        team_str_final = team_str_3char_exc.lower()
        await bot.say("```Season {}\n{} had {} {}```".format(team_str_season,
                        lb.team_dict_two[team_str_final], random_team_stat, stat_name))
    else:
        random_stat = randsheet.loc[player_or_team_id, stat_name]
        await bot.say("```{}\n{} had {} {}```".format(randsheet.name,
                        player_or_team_id, random_stat, stat_name))

@bot.command()
async def top(num: int, statname: str):
    stat = lb.stat_dict[statname.lower()]
    rounded_sheet = all_rounds.round(decimals=2)
    #top_sheet = all_rounds.nlargest(num, stat)
    #stat = lb.stat_dict[statname.lower()]
    top_sheet = rounded_sheet.sort_values(stat, ascending=False).head(num)[[stat]]
    #top_sheet_rounded = top_sheet.round(decimals=2)
    await bot.say("""```Single Round Performances\ntop {}\
 {} all time: \n \n {}```""".format(num, stat, top_sheet))

@bot.command()
async def map(num: float):
    if num not in map_data.index:
        num_int = int(num)
        await bot.say("```Map {} has not been played in the WDL :(```".format(num_int))

    map_name = map_data.loc[num, "Map Name"]
    map_wad = map_data.loc[num, "Source Wad"]
    map_rat = map_data.loc[num, "RAT"]
    map_rat_round = round(map_rat, 2)
    map_frags = map_data.loc[num, "FRG"]
    map_frags_round = round(map_frags, 2)
    map_games = map_data.loc[num, "GP"]
    map_points_pergame = map_data.loc[num, "POINTS"]
    map_points_round = round(map_points_pergame, 2)

    if num in map_data.index:
        await bot.say("""**{}** from {} \n\n{} games taken place \nAverage RAT - {}\
\nAvg Frags per player - {} \nAvg Points per game - {}""".format(map_name,
             map_wad, map_games, map_rat_round, map_frags_round, map_points_round))


bot.run("wolfeman312@gmail.com", "itchyshorts99")
