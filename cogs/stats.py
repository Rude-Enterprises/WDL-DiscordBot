import random
from discord.ext import commands
import libraries as lb

lb.all_time_playoff.name = "All time Playoffs"
lb.season7.name = "Season 7"
lb.season6.name = "Season 6"
lb.season5.name = "Season 5"
lb.season4.name = "Season 4"
lb.season3.name = "Season 3"
lb.season2.name = "Season 2"
lb.season1.name = "Season 1"
lb.team_stats.name = "Team Stats"

pandas_sheets = (lb.all_time_playoff,
                 lb.season7,
                 lb.season6,
                 lb.season5,
                 lb.season4,
                 lb.season3,
                 lb.season2,
                 lb.season1,
                 lb.team_stats
                )


class Stats():
    """Stats holds all statistical analysis commands that can be used in Discord Chat."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lifetime(self, player: str):
        """!lifeime <player> - returns an overview of a players key lifetime stats."""
        player_lower = player.lower()
        try:

            rating = round(lb.player_totals.ix[player_lower, "rat"], 2)
            frags = lb.player_totals.ix[player_lower, "frags"]
            kdr = round(lb.player_totals.ix[player_lower, "kdr"], 2)
            damage = lb.player_totals.ix[player_lower, "dmg"]
            defenses = lb.player_totals.ix[player_lower, "def"]
            captures = lb.player_totals.ix[player_lower, "caps"]
            pcaptures = lb.player_totals.ix[player_lower, "pcaps"]

            await self.bot.say("```{} lifetime stats: \n\nRAT - {}\nFrags - {}\nK/D - {}\n"
                               "Damage - {}\nDefenses - {}\nCaptures - {}\nPCaptures - {}```".format(
                                player.capitalize(), rating, frags, kdr, damage, defenses, captures, pcaptures))

        except KeyError:
            await self.bot.say("{} doesnt exist . . . ".format(player))

    @commands.command()
    async def team(self, teamname: str, season):
        team_key = teamname.upper() + " " + str(season)

        if team_key in lb.team_dict_inverse:
            rating = round(lb.team_stats.ix[lb.team_dict_inverse[team_key], "rat"], 2)
            frags = lb.team_stats.ix[lb.team_dict_inverse[team_key], "frags"]
            kdr = round(lb.team_stats.ix[lb.team_dict_inverse[team_key], "kdr"], 2)
            wins = round(lb.team_stats.ix[lb.team_dict_inverse[team_key], "win%"], 2)
            points = lb.team_stats.ix[lb.team_dict_inverse[team_key], "points"]
            await self.bot.say("```{} Season {}\n\nRat - {}\nFrags - {}\nKDR - {}\nPoints - {}\nWin % - {}```".format(
                                teamname.upper(), season, rating, frags, kdr, points, wins))
        else:
            await self.bot.say("invalid arguments . . .")

    @commands.command()
    async def randstat(self):
        """!randstat - returns a random stat."""
        random_sheet = pandas_sheets[random.randint(0, 8)]
        index_length = len(random_sheet.index)
        column_length = len(random_sheet.columns)
        player_or_team_id = random_sheet.index[random.randint(1, (index_length - 1))]
        stat_name = random_sheet.columns[random.randint(0, (column_length - 1))]

        if random_sheet.name == "Team Stats":
            random_team_stat = random_sheet.loc[player_or_team_id, stat_name]
            team_str = str(lb.team_dict[player_or_team_id])
            team_str_season = team_str[4]
            team_str_3char = team_str[:3]
            team_str_3char_exc = "!" + team_str_3char
            team_str_final = team_str_3char_exc.lower()
            await self.bot.say("```Season {}\n{} had {} {}```".format(team_str_season,
                                                                      lb.team_dict_two[team_str_final],
                                                                      random_team_stat, stat_name))
        else:
            random_stat = random_sheet.loc[player_or_team_id, stat_name]
            player_capitalize = ""
            if type(player_or_team_id) == str:
                player_capitalize += player_or_team_id.capitalize()
            else:
                pass
            await self.bot.say("```{}\n{} had {} {}```".format(random_sheet.name,
                                                               player_capitalize,
                                                               random_stat,
                                                               stat_name))

    @commands.command()
    async def top(self, num: int, stat_name: str):
        """!top num statname - returns the top x performances of the selected stat."""
        try:
            stat = stat_name.lower()
            rounded_sheet = lb.all_rounds.round(decimals=2)
            # top_sheet = all_rounds.nlargest(num, stat)
            # stat = lb.stat_dict[statname.lower()]
            top_sheet = rounded_sheet.sort_values(stat, ascending=False)
            top_sheet = top_sheet.drop_duplicates(subset="nick", keep="first").head(num)[["nick", stat, "sid"]]
            top_sheet = top_sheet.to_string(index=False, justify="left")
            # top_sheet_rounded = top_sheet.round(decimals=2)
            await self.bot.say("```{}```".format(top_sheet))
        except KeyError:
            pass

    @commands.command()
    async def least(self, num: int, stat_name: str):
        """!least num statname - returns the bottom x performances of the selected stat."""
        try:
            stat = stat_name.lower()
            rounded_sheet = lb.all_rounds.round(decimals=2)
            least_sheet = rounded_sheet.sort_values(stat)
            least_sheet = least_sheet.drop_duplicates(subset="nick", keep="first").head(num)[["nick", stat, "sid"]]
            least_sheet = least_sheet.to_string(index=False, justify="left")
            await self.bot.say("```{}```".format(least_sheet))
        except KeyError:
            pass

    @commands.command()
    async def avg(self, stat_name: str):
        """!avg statname - returns the all-time average of the selected stat."""
        try:
            stat = stat_name.lower()
            stat_mean = lb.all_rounds[stat].mean()
            stat_mean_round = round(stat_mean, 2)
            await self.bot.say("All time average {} per round: {}".format(stat.capitalize(), stat_mean_round))

        except KeyError:
            pass

    @commands.command()
    async def total(self, stat_name: str):
        """The sum of a stat through every round"""
        try:
            stat = stat_name.lower()
            stat_sum = lb.all_rounds[stat].sum()
            await self.bot.say("Total {}: {}".format(stat.capitalize(), int(stat_sum)))
        except KeyError:
            pass

    @commands.command()
    async def map(self, num: float):
        """!map num - returns info and statistics for the selected map."""
        if num not in lb.map_data.index:
            num_int = int(num)
            await self.bot.say("```Map {} has not been played in the WDL :(```".format(num_int))

        elif num in lb.map_data.index:
            map_name = lb.map_data.loc[num, "Map Name"]
            map_wad = lb.map_data.loc[num, "Source Wad"]
            map_rat = lb.map_data.loc[num, "RAT"]
            map_rat_round = round(map_rat, 2)
            map_frags = lb.map_data.loc[num, "FRG"]
            map_frags_round = round(map_frags, 2)
            map_games = lb.map_data.loc[num, "GP"]
            map_points_pergame = lb.map_data.loc[num, "POINTS"]
            map_points_round = round(map_points_pergame, 2)
            await self.bot.say("**{}** from {} \n\n{} games taken place \nAvg Frags per player - {}\n"
                    "Avg Points per game - {}\nAvg RAT - {}".format(map_name,
                                                                    map_wad,
                                                                    map_games,
                                                                    map_frags_round,
                                                                    map_points_round,
                                                                    map_rat_round))

def setup(bot):
    bot.add_cog(Stats(bot))
