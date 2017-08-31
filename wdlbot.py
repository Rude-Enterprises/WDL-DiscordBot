import sys
import os
from discord.ext import commands
import libraries as lb
import cfg
import pandas as pd
import discord
from cogs import process

initial_extensions = ["misc", "stats", "webcmds", "pickups"]

bot = commands.Bot(command_prefix="!", description="Hello I am a bot ! beepboop.")
bot.remove_command("help")

#all sheets to be used from Jwarrier's wdlstatsv4 read with Pandas
workbook = pd.ExcelFile("C:/Users/Jesse/Desktop/WDLSTATSv4.xlsx")
player_totals = pd.read_excel(workbook, "PT Player Totals", names=lb.player_totals_column_names)
player_avg = pd.read_excel(workbook, "PT PlayerAVG")
all_time_playoff = pd.read_excel(workbook, "ALL TIME Playoffs", skiprows=[0], names=lb.alltime_playoff_column_names)
season7 = pd.read_excel(workbook, "Season 7", skiprows=[0], names=lb.season_column_names)
season6 = pd.read_excel(workbook, "Season 6", skiprows=[0], names=lb.season_column_names)
season5 = pd.read_excel(workbook, "Season 5", skiprows=[0], names=lb.season_column_names)
season4 = pd.read_excel(workbook, "Season 4", skiprows=[0], names=lb.season_column_names)
season3 = pd.read_excel(workbook, "Season 3", skiprows=[0], names=lb.season_column_names)
season2 = pd.read_excel(workbook, "Season 2", skiprows=[0], names=lb.season_column_names)
season1 = pd.read_excel(workbook, "Season 1", skiprows=[0], names=lb.season_column_names)
team_stats = pd.read_excel(workbook, "Team Stats", skiprows=[0], index_col=[1], names=lb.team_stats_column_names)
all_rounds = pd.read_excel(workbook, "All Rounds", names=lb.all_rounds_column_names, parse_cols=20)
map_data = pd.read_excel(workbook, "Map Data", index_col=[11])
map_rat_player = pd.read_excel(workbook, "Map RAT by Player", index_col=[1])
map_rat_team = pd.read_excel(workbook, "Map RAT by Team", index_col=[0])

def rename_dataframe_index_player(dataframe):
    dataframe = dataframe.dropna()
    dataframe = dataframe.reset_index().dropna().set_index("nick")
    dataframe = dataframe.rename(lambda x: x.lower())
    dataframe = dataframe.drop(["index"], axis=1)
    return dataframe

player_totals = rename_dataframe_index_player(player_totals)
season7 = rename_dataframe_index_player(season7)
season6 = rename_dataframe_index_player(season6)
season5 = rename_dataframe_index_player(season5)
season4 = rename_dataframe_index_player(season4)
season3 = rename_dataframe_index_player(season3)
season2 = rename_dataframe_index_player(season2)
season1 = rename_dataframe_index_player(season1)
all_rounds = all_rounds.dropna()
all_rounds = all_rounds.reset_index().dropna().set_index("nick")



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
    message_lower_split = message.content.lower().split()
    message_upper_split = message.content.upper().split()
    player_name = message_lower_split[0][1:]

    #bot will only work in WDL, Odamex, and testing channels
    if (message.channel.id != cfg.wdl_stats_channelid and
            message.channel.id != cfg.odamex_general_channelid and
            message.channel.id != cfg.bot_test_channelid):
        return

    #PLAYER LIFETIME STATS !<player> <stat>
    elif player_name in player_totals.index and message_lower_split[1] in player_totals.columns:

        try:
            player_stat = player_totals.ix[player_name, message_lower_split[1]]
            player_stat_round = round(player_stat, 2)
            await bot.send_message(message.channel, "```{} lifetime {}: {} ```".format(
                player_name.capitalize(), message_lower_split[1], player_stat_round))

        except discord.ext.commands.errors.CommandNotFound:
            pass

    #TEAM SEASON STATS  !<team> <number> <stat>
    elif message_lower_split[0] in lb.team_dict_two and len(message_lower_split) == 3:
        first_message_string = str(message_upper_split[0])
        team_acronym = first_message_string[1:]
        team_acronym_upper = team_acronym.upper()
        team_dict_inv_key = (team_acronym + " " + str(message_lower_split[1]))

        if team_dict_inv_key not in lb.team_dict_inverse:
            await bot.send_message(message.channel, "No team {} found for Season {}".format(team_acronym_upper,
                                                                                            message_split[1]))
        else:
            team_stat = team_stats.loc[lb.team_dict_inverse[team_dict_inv_key], message_lower_split[2]]
            team_stat_round = round(team_stat, 2)
            team_name = lb.team_dict_two[message_lower_split[0]]
            stat_name = message_lower_split[2].capitalize()
            await bot.send_message(message.channel, "{} Season {} {}: {}".format(team_name,
                                                                                 message_split[1],
                                                                                 stat_name,
                                                                                 team_stat_round))

    else:
        pass

    await bot.process_commands(message)


if __name__ == "__main__":

    sys.path.insert(1, os.getcwd() + "/cogs/")  # this allows the cogs in the cogs folder to be loaded

    for extension in initial_extensions:
        bot.load_extension(extension)  # This adds the cogs listed in initial_extensions to the bot

    bot.loop.create_task(process.gametime_checker())
    bot.run(cfg.TOKEN)
