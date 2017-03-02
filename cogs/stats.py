from discord.ext import commands
import pandas as pd
import random
import libraries as lb
import wdlBot as wdl
import re

wdl.all_time_playoff.name = "All time Playoffs"
wdl.season7.name = "Season 7"
wdl.season6.name = "Season 6"
wdl.season5.name = "Season 5"
wdl.season4.name = "Season 4"
wdl.season3.name = "Season 3"
wdl.season2.name = "Season 2"
wdl.season1.name = "Season 1"
wdl.team_stats.name = "Team Stats"

sheet_set = (wdl.all_time_playoff,
             wdl.season7,
             wdl.season6,
             wdl.season5,
             wdl.season4,
             wdl.season3,
             wdl.season2,
             wdl.season1,
             wdl.team_stats
             )



class Stats():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randstat(self):
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
            await self.bot.say("```Season {}\n{} had {} {}```".format(team_str_season,
                                                                 lb.team_dict_two[team_str_final], random_team_stat,
                                                                 stat_name))
        else:
            random_stat = randsheet.loc[player_or_team_id, stat_name]
            await self.bot.say("```{}\n{} had {} {}```".format(randsheet.name,
                                                          player_or_team_id, random_stat, stat_name))

    @commands.command()
    async def top(self, num: int, statname: str):
        stat = lb.stat_dict[statname.lower()]
        rounded_sheet = wdl.all_rounds.round(decimals=2)
        # top_sheet = all_rounds.nlargest(num, stat)
        # stat = lb.stat_dict[statname.lower()]
        top_sheet = rounded_sheet.sort_values(stat, ascending=False).head(num)[[stat]]
        # top_sheet_rounded = top_sheet.round(decimals=2)
        await self.bot.say("""```Single Round Performances\ntop {} {} all time: \n \n {}```""".format(
                                                                                            num, stat, top_sheet))

    @commands.command(name="bot")
    async def _bottom(self, num: int, statname: str):
        stat = lb.stat_dict[statname.lower()]
        rounded_sheet = wdl.all_rounds.round(decimals=2)
        rounded_sheet_dropna = rounded_sheet.dropna(axis=0, how="any")
        bot_sheet = rounded_sheet_dropna.sort_values(stat).head(num)[[stat]]
        await self.bot.say("""```Single Round Performances\nbottom {} {} all time: \n \n {}```""".format(
                                                                                            num, stat, bot_sheet))

    @commands.command()
    async def map(self, num: float):
        if num not in wdl.map_data.index:
            num_int = int(num)
            await self.bot.say("```Map {} has not been played in the WDL :(```".format(num_int))

        map_name = wdl.map_data.loc[num, "Map Name"]
        map_wad = wdl.map_data.loc[num, "Source Wad"]
        map_rat = wdl.map_data.loc[num, "RAT"]
        map_rat_round = round(map_rat, 2)
        map_frags = wdl.map_data.loc[num, "FRG"]
        map_frags_round = round(map_frags, 2)
        map_games = wdl.map_data.loc[num, "GP"]
        map_points_pergame = wdl.map_data.loc[num, "POINTS"]
        map_points_round = round(map_points_pergame, 2)

        if num in wdl.map_data.index:
            await self.bot.say("""**{}** from {} \n\n{} games taken place \nAverage RAT - {}\
    \nAvg Frags per player - {} \nAvg Points per game - {}""".format(map_name,
                                                                     map_wad, map_games, map_rat_round, map_frags_round,
                                                                     map_points_round))

def setup(bot):
    bot.add_cog(Stats(bot))


