import sys
import os
from discord.ext import commands
import libraries as lb
import cfg
import discord
from cogs import process

initial_extensions = ["misc", "stats", "webcmds", "pickups"]

bot = commands.Bot(command_prefix="!", description="Hello I am a bot ! beepboop.")
bot.remove_command("help")

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
    """Here are commands relating to !players and !teams."""

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
    elif player_name in lb.player_totals.index and message_lower_split[1] in lb.player_totals.columns:

        try:
            player_stat = lb.player_totals.ix[player_name, message_lower_split[1]]
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
            team_stat = lb.team_stats.loc[lb.team_dict_inverse[team_dict_inv_key], message_lower_split[2]]
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
